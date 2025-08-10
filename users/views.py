# users/views.py
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from .forms import SignupForm
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # require activation
            user.save()
            # assign Participant group by default
            participant_group, _ = Group.objects.get_or_create(name="Participant")
            user.groups.add(participant_group)
            # send activation mail
            current_site = get_current_site(request)
            subject = "Activate your account"
            message = render_to_string("users/activation_email.html", {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            })
            send_mail(subject, message, None, [user.email])
            messages.success(request, "Account created. Check your email to activate.")
            return redirect("core:home")
    else:
        form = SignupForm()
    return render(request, "users/registration/signup.html", {"form": form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account activated! You can login now.")
        return redirect("login")
    else:
        messages.error(request, "Activation link invalid or expired.")
        return redirect("core:home")

@login_required
def profile(request):
    # Redirect users based on group
    u = request.user
    if u.is_superuser:
        return redirect('admin:index')
    if u.groups.filter(name='Organizer').exists():
        return redirect('events:dashboard')
    # Participant: show their RSVP list
    from events.models import RSVP
    rsvps = RSVP.objects.filter(user=u).select_related('event__category')
    return render(request, "users/profile.html", {"rsvps": rsvps})


igner = TimestampSigner()
User = get_user_model()

def activate_account(request, token):
    try:
        user_id = signer.unsign(token, max_age=60*60*24)  
        user = User.objects.get(pk=user_id)
        user.is_active = True
        user.save()
        return redirect('login')
    except (BadSignature, SignatureExpired, User.DoesNotExist):
        return redirect('users:activation_failed')
