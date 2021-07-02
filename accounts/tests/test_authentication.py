import uuid

from django.test import TestCase

from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token, User

EMAIL = "bob@loblaw.com"


class AuthenticationTest(TestCase):
    def test_returns_None_if_no_such_token(self):
        self.assertIsNone(PasswordlessAuthenticationBackend().authenticate(uuid.uuid4()))

    def test_returns_new_user(self):
        token = Token.objects.create(email=EMAIL)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        new_user = User.objects.get(email=EMAIL)
        self.assertEqual(user, new_user)

    def test_returns_existing_user(self):
        existing_user = User.objects.create(email=EMAIL)
        token = Token.objects.create(email=EMAIL)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        self.assertEqual(user, existing_user)

