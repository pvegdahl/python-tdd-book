from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore
from django.core.management import BaseCommand, CommandParser

from accounts.models import User
from superlists import settings


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser):
        parser.add_argument("email")
        pass

    def handle(self, *args, **options):
        self.stdout.write(create_preauthenticated_session(options["email"]))


def create_preauthenticated_session(email: str):
    user, _ = User.objects.get_or_create(email=email)
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()
    return session.session_key
