# events/signals.py
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import RSVP

@receiver(post_save, sender=RSVP)
def send_rsvp_email(sender, instance, created, **kwargs):
    if created:
        subject = f"RSVP Confirmation for {instance.event.name}"
        message = f"Hi {instance.user.get_full_name() or instance.user.username},\n\nYou have RSVP'd to {instance.event.name} on {instance.event.date}."
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.user.email])

# In apps.py or ready() import signals to register them
