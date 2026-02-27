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
            
            # Rule: Severe delay (>= 180 mins)
            if delay_minutes >= 180:
                cards.append(Card(
                    type="severe_delay",
                    title="Severe Departure Delay",
                    message=f"Your flight {product.title} is severely delayed. High risk of missing connections.",
                    actions=[
                        {"label": "Reaccommodation options", "action_type": "view_rebooking"},
                        {"label": "Contact Agent", "action_type": "call_support"}
                    ]
                ))
            # Rule: Moderate Delay alert (>= 30 and < 180 mins)
            elif delay_minutes >= 30:
                cards.append(Card(
                    type="delay_alert",
                    title="Flight Delayed",
                    message=f"Your flight {product.title} is delayed by {delay_minutes} minutes.",
                    actions=[
                        {"label": "Wait in Lounge", "action_type": "view_lounges"},
                        {"label": "Rebook Alternate", "action_type": "view_flights"},
                        {"label": "Notify Hotel", "action_type": "notify_hotel"}
                    ]
                ))
            
            # Use original start time or delayed time for boarding checks depending on requirement
            # Here assuming start_time is scheduled time. We add delays to it for actual departure.
            actual_departure = product.start_time + timedelta(minutes=delay_minutes)
            time_until_departure = actual_departure - now

            # Rule: Tight Check-in / Leave Now (< 3h)
            if timedelta(0) < time_until_departure <= timedelta(hours=3):
                cards.append(Card(
                    type="commute_alert",
                    title="Urgent: Time to head to the airport",
                    message="You are within the tight check-in window. Leave immediately.",
                    actions=[
                        {"label": "Book Uber", "action_type": "book_ride"}, 
                        {"label": "Express Check In", "action_type": "open_checkin"}
                    ]
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
            # Logic needs full trip context, evaluating below.
            pass

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
                    title="Late Hotel Check-in Plan",
                    message=f"Due to your arrival time at {hotel.title}, you run the risk of missing normal check-in times.",
                    actions=[{"label": "Notify Front Desk", "action_type": "send_message"}]
                ))

    return cards
