import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secreto_heladeria.settings')
django.setup()

from django.contrib.auth.models import User

def update_users():
    users_map = {
        'finanzas': 'finanzas@test.com',
        'bodega': 'bodega@test.com',
        'compras': 'compras@test.com'
    }

    for username, email in users_map.items():
        try:
            user = User.objects.get(username=username)
            user.email = email
            user.save()
            print(f"Updated {username} with email {email}")
        except User.DoesNotExist:
            print(f"User {username} not found")

if __name__ == '__main__':
    update_users()
