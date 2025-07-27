import os
import django
from datetime import datetime, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from events.models import Category, Participant, Event

# Clear existing data (optional)
Category.objects.all().delete()
Participant.objects.all().delete()
Event.objects.all().delete()

# Add Categories
categories = [
    {"name": "Education", "description": "Educational events like seminars and workshops."},
    {"name": "Health", "description": "Health-related events including checkups and awareness."},
    {"name": "Social", "description": "Social gatherings, meetups, and networking."},
]

category_objs = []
for cat in categories:
    obj = Category.objects.create(**cat)
    category_objs.append(obj)

# Add Participants
participants = []
for i in range(1, 6):
    participant = Participant.objects.create(
        name=f"Participant {i}",
        email=f"user{i}@example.com"
    )
    participants.append(participant)

# Add Events
for i in range(1, 6):
    event = Event.objects.create(
        name=f"Event {i}",
        description=f"This is the description for Event {i}.",
        date=datetime.now().date() + timedelta(days=i),
        time=datetime.now().time().replace(microsecond=0),
        location=f"Location {i}",
        category=random.choice(category_objs),
    )
    # Optional: Add participants if you have a ManyToMany
    # event.participants.set(random.sample(participants, k=random.randint(1, 3)))

print("✅ Database populated successfully.")
