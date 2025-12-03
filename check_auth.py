import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secreto_heladeria.settings')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

def debug_login():
    username = 'finanzas@test.com'
    password = 'password123'
    
    print(f"Attempting login for: {username} / {password}")
    
    # 1. Check User existence
    try:
        user = User.objects.get(email=username)
        print(f"User found: {user.username} (ID: {user.id})")
        print(f"  Email: {user.email}")
        print(f"  Is Active: {user.is_active}")
        print(f"  Is Staff: {user.is_staff}")
        print(f"  Is Superuser: {user.is_superuser}")
        print(f"  Password valid: {user.check_password(password)}")
    except User.DoesNotExist:
        print("User NOT found by email.")
        return

    # 2. Try authenticate
    user_auth = authenticate(username=username, password=password)
    if user_auth:
        print(f"Authentication SUCCESS! Backend: {user_auth.backend}")
    else:
        print("Authentication FAILED.")
        
        # Debug Backend
        from compras.backends import RutAuthBackend
        backend = RutAuthBackend()
        print("Testing RutAuthBackend directly...")
        res = backend.authenticate(None, username=username, password=password)
        print(f"RutAuthBackend result: {res}")

if __name__ == '__main__':
    debug_login()
