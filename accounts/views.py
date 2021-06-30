from django.core.mail import send_mail
from django.shortcuts import render, redirect


def send_login_email(request):
    email = request.POST["email"]
    send_mail(
        subject="Your login link for Superlists",
        message="TBD",
        from_email="noreply@superlists",
        recipient_list=[email],
    )
    return redirect("/")
