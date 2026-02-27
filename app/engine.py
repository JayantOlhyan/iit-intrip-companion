from app.models import Trip, Card
from datetime import datetime
from datetime import timezone
from datetime import timedelta

def compute_nudges(trip: Trip) -> list[Card]:
    cards = []
    now = datetime.now(timezone.utc)
    
    for product in trip.products:
        if product.type == "flight":
            time_until_flight = product.start_time - now
            delay_minutes = product.meta.get("delay_minutes", 0)
            
            # Rule: Delay alert + options
            if delay_minutes >= 30:
                cards.append(Card(
                    type="delay_alert",
                    title="Flight Delayed",
                    message=f"Your flight {product.title} is delayed by {delay_minutes} minutes.",
                    actions=[{"label": "View Alternates", "action_type": "view_flights"}, {"label": "Lounge Access", "action_type": "view_lounges"}]
                ))
            
            # Use original start time or delayed time for boarding checks depending on requirement
            # Here assuming start_time is scheduled time. We add delays to it for actual departure.
            actual_departure = product.start_time + timedelta(minutes=delay_minutes)
            time_until_departure = actual_departure - now

            # Rule: Leave now / commute (< 3h)
            if timedelta(0) < time_until_departure <= timedelta(hours=3):
                cards.append(Card(
                    type="commute_alert",
                    title="Time to leave for the airport",
                    message="Traffic is light. Leave now to arrive 2 hours early.",
                    actions=[{"label": "Book Uber", "action_type": "book_ride"}, {"label": "Get Directions", "action_type": "view_map"}]
                ))
            # Rule: Check-in reminder (< 24h) but only if not already commuting
            elif timedelta(hours=3) < time_until_departure <= timedelta(hours=24):
                cards.append(Card(
                    type="checkin_reminder",
                    title="Check-in open",
                    message=f"Check-in is open for {product.title}.",
                    actions=[{"label": "Check In Now", "action_type": "open_checkin"}]
                ))
                
        if product.type == "hotel":
            # Just a simple heuristic for late check-in: if the flight arrives after 8 PM
            # and the hotel is on the same day. 
            pass  # Logic needs full trip context, evaluating below.

    # Late check-in guidance: Find flights arriving late and hotels starting same day
    flights = [p for p in trip.products if p.type == "flight"]
    hotels = [p for p in trip.products if p.type == "hotel"]
    
    for flight in flights:
        delay = flight.meta.get("delay_minutes", 0)
        arrival_time = flight.end_time + timedelta(minutes=delay)
        
        for hotel in hotels:
            # If arriving after 20:00 (8 PM) local to the flight arrival, warn hotel
            # (Using absolute UTC for simplicity in this example)
            if arrival_time > hotel.start_time and arrival_time.hour >= 20:
                cards.append(Card(
                    type="late_checkin",
                    title="Late Hotel Check-in",
                    message=f"You will arrive at {hotel.title} late. We can notify the front desk.",
                    actions=[{"label": "Notify Hotel", "action_type": "send_message"}]
                ))

    return cards
