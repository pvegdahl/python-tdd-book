import uuid
from unittest import mock
from unittest.mock import patch

from django.test import TestCase

from accounts.models import Token
from accounts.views import EMAIL_SUBJECT, SUCCESS_MESSAGE

EMAIL = "someone@somewhere.com"


class SendLoginEmailViewTest(TestCase):
    def test_redirects_to_home_page(self):
        response = self.client.post("/accounts/send_login_email", data={"email": EMAIL})
        self.assertRedirects(response, "/")

    @patch("accounts.views.send_mail")
    def test_sends_email_to_address_from_post(self, mock_send_mail):
        self.client.post("/accounts/send_login_email", data={"email": EMAIL})

        mock_send_mail.assert_called_once_with(
            subject=EMAIL_SUBJECT,
            message=mock.ANY,
            from_email="noreply@superlists",
            recipient_list=[EMAIL],
        )

    def test_adds_success_message(self):
        response = self.client.post(
            "/accounts/send_login_email", data={"email": EMAIL}, follow=True
        )

        message = list(response.context["messages"])[0]
        self.assertEqual(message.message, SUCCESS_MESSAGE)
        self.assertEqual(message.tags, "success")

    def test_creates_token_associated_with_email(self):
        self.client.post("/accounts/send_login_email", data={"email": EMAIL})
        self.assertEqual(Token.objects.first().email, EMAIL)

    @patch("accounts.views.send_mail")
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        self.client.post("/accounts/send_login_email", data={"email": EMAIL})

        # noinspection HttpUrlsUsage
        expected_url = (
            f"http://testserver/accounts/login?token={Token.objects.first().uid}"
        )
        self.assertIn(expected_url, mock_send_mail.call_args.kwargs["message"])


@patch("accounts.views.auth")
class LoginViewTest(TestCase):
    def setUp(self) -> None:
        self.uid = uuid.uuid4()

    def test_redirects_to_home_page(self, mock_auth):
        response = self.client.get(f"/accounts/login?token={self.uid}")
        self.assertRedirects(response, "/")

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        self.client.get(f"/accounts/login?token={self.uid}")
        mock_auth.authenticate.assert_called_once_with(uid=self.uid)

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        response = self.client.get(f"/accounts/login?token={self.uid}")
        mock_auth.login.assert_called_once_with(
            response.wsgi_request, mock_auth.authenticate.return_value
        )

    def test_does_not_log_in_if_user_is_not_authenticated(self, mock_auth):
        mock_auth.authenticate.return_value = None
        self.client.get(f"/accounts/login?token={self.uid}")
        mock_auth.login.assert_not_called()
