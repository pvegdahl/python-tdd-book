from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect


EMAIL_SUBJECT = "Your login link for Superlists"
SUCCESS_MESSAGE = "Check your email, we've sent you a link you can use to log in."


def send_login_email(request):
    email = request.POST["email"]
    send_mail(
        subject=EMAIL_SUBJECT,
        message="Use this link to log in",
        from_email="noreply@superlists",
        recipient_list=[email],
    )
    messages.success(request, SUCCESS_MESSAGE)
    return redirect("/")


def login(request):
    return redirect("/")