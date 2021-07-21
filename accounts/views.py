import uuid

from django.contrib import messages, auth
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout as django_logout

from accounts.models import Token

EMAIL_SUBJECT = "Your login link for Superlists"
SUCCESS_MESSAGE = "Check your email, we've sent you a link you can use to log in."


def send_login_email(request):
    email = request.POST["email"]
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(reverse("login") + "?token=" + str(token.uid))
    send_mail(
        subject=EMAIL_SUBJECT,
        message=f"Use this link to log in\n\n{url}",
        from_email="noreply@superlists",
        recipient_list=[email],
    )
    messages.success(request, SUCCESS_MESSAGE)
    return redirect("/")


def login(request):
    user = auth.authenticate(uuid.UUID(request.GET.get("token")))
    if user:
        auth.login(request, user)
    return redirect("/")


def logout(request):
    django_logout(request)
    return redirect("/")
