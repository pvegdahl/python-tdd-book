from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import Token

User = get_user_model()

EMAIL = "a@b.com"


class UserModelTest(TestCase):
    def test_user_is_valid_with_email_only(self):
        user = User(email=EMAIL)
        user.full_clean()  # Should not raise an exception

    def test_email_is_primary_key(self):
        self.assertEqual(User(email=EMAIL).pk, EMAIL)


class TokenModelTest(TestCase):
    def test_links_user_with_unique_auto_generated_uid(self):
        token_1 = Token.objects.create(email=EMAIL)
        token_2 = Token.objects.create(email=EMAIL)
        self.assertNotEqual(token_1.uid, token_2.uid)
