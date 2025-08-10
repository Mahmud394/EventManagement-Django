import os
import django
import random
from datetime import datetime, timedelta, time

# Setup Django environment (adjust 'event_management' to your project name)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from events.models import Category, Event
from django.contrib.auth import get_user_model

User = get_user_model()

def populate():
    print("Populating database...")

    # Create Categories
    categories_data = [
        {'name': 'Conference', 'description': 'Professional conferences and meetings.'},
        {'name': 'Workshop', 'description': 'Hands-on training sessions.'},
        {'name': 'Webinar', 'description': 'Online seminars and presentations.'},
        {'name': 'Concert', 'description': 'Musical performances and concerts.'},
    ]

    categories = []
    for cat_data in categories_data:
        cat, created = Category.objects.get_or_create(name=cat_data['name'], defaults={'description': cat_data['description']})
        categories.append(cat)
        print(f"Category created: {cat.name}")

    # Create Users (Participants)
    users_data = [
        {'username': 'alice', 'email': 'alice@example.com', 'password': 'testpassword123', 'first_name': 'Alice', 'last_name': 'Smith'},
        {'username': 'bob', 'email': 'bob@example.com', 'password': 'testpassword123', 'first_name': 'Bob', 'last_name': 'Johnson'},
        {'username': 'charlie', 'email': 'charlie@example.com', 'password': 'testpassword123', 'first_name': 'Charlie', 'last_name': 'Lee'},
    ]

    users = []
    for udata in users_data:
        user, created = User.objects.get_or_create(username=udata['username'], defaults={
            'email': udata['email'],
            'first_name': udata['first_name'],
            'last_name': udata['last_name'],
            'is_active': True,
        })
        if created:
            user.set_password(udata['password'])
            user.save()
            print(f"User created: {user.username}")
        users.append(user)

    # Create Events
    base_date = datetime.now().date()
    for i in range(1, 6):
        event_name = f"Sample Event {i}"
        event_desc = f"This is a description for event {i}."
        event_date = base_date + timedelta(days=i)
        event_time = time(hour=10+i)
        event_location = f"Location {i}"
        category = random.choice(categories)

        event, created = Event.objects.get_or_create(
            name=event_name,
            defaults={
                'description': event_desc,
                'date': event_date,
                'time': event_time,
                'location': event_location,
                'category': category,
            }
        )
        if created:
            print(f"Event created: {event.name}")

        # Assign random participants to event
        participants = random.sample(users, k=random.randint(1, len(users)))
        event.participants.set(participants)  # Adjust if you use User model for participants
        event.save()
        print(f"Participants assigned to event '{event.name}': {[u.username for u in participants]}")

    print("Database population complete.")

if __name__ == '__main__':
    populate()
