from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.signing import TimestampSigner
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.conf import settings

User = get_user_model()
signer = TimestampSigner()


def send_activation_email(user):
    """
    Sends an account activation email with a signed token link (HTML version).
    """
    # Create signed token
    token = signer.sign(user.pk)
    activation_url = settings.SITE_URL + reverse('users:activate', args=[token])

    # Render HTML email
    html_content = render_to_string(
        'users/activation_email.html',
        {
            'user': user,
            'activation_url': activation_url,
            'year': timezone.now().year
        }
    )
    text_content = strip_tags(html_content)

    # Send email
    email = EmailMultiAlternatives(
        subject="Activate Your Account",
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()


@receiver(post_save, sender=User)
def send_activation_email_on_create(sender, instance, created, **kwargs):
    """
    Trigger activation email when a new user is created and is inactive.
    """
    if created and not instance.is_active and instance.email:
        send_activation_email(instance)
