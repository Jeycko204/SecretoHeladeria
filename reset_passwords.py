import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secreto_heladeria.settings')
django.setup()

from django.contrib.auth.models import User

def reset_passwords():
    users = ['finanzas', 'bodega', 'compras']
    password = 'password123'
    
    for username in users:
        try:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            print(f"Reset password for {username} to {password}")
        except User.DoesNotExist:
            print(f"User {username} not found")

if __name__ == '__main__':
    reset_passwords()
