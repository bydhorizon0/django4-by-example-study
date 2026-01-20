from django.contrib.auth.models import User
from django.http import HttpRequest

from account.models import Profile


class EmailAuthBackend:
    """email을 이용한 인증"""

    def authenticate(self, request: HttpRequest, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id: str):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None


def create_profile(backend, user: User, *args, **kwargs):
    """
    Create user profile for social authentication
    :param backend:
    :param user:
    :param args:
    :param kwargs:
    :return:
    """
    Profile.objects.get_or_create(user=user)
