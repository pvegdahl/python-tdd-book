from uuid import UUID

from accounts.models import Token, User


class PasswordlessAuthenticationBackend:
    @staticmethod
    def authenticate(uid: UUID):
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except Token.DoesNotExist:
            return None
        except User.DoesNotExist:
            # noinspection PyUnboundLocalVariable
            return User.objects.create(email=token.email)

    @staticmethod
    def get_user(email: str) -> User:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
