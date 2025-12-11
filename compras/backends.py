import re
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class RutAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        user = None

        if '@' in username:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        elif re.match(r'^[0-9]+-?[0-9kK]$', username):
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        else:
            return None

        if user:
            if user.is_superuser or user.is_staff:
                return None

            if user.check_password(password):
                return user
        
        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
