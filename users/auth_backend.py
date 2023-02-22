from django.contrib.auth.backends import BaseBackend
from django.db.models import Q
from .models import UserAuth


class UserAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = UserAuth.objects.get(Q(username=username) | Q(phone_number=username))

            if user.check_password(password):
                return user
        except UserAuth.DoesNotExist:
            return None
        return None
    
    def get_user(self, user_id):
        try:
            return UserAuth.objects.get(pk=user_id)
        except UserAuth.DoesNotExist:
            return None