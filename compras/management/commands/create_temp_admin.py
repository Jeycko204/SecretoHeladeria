
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create a temporary admin user'

    def handle(self, *args, **options):
        if not User.objects.filter(username='temp_admin').exists():
            User.objects.create_superuser('temp_admin', 'temp_admin@example.com', 'password')
            self.stdout.write(self.style.SUCCESS('Successfully created temporary admin user "temp_admin".'))
        else:
            self.stdout.write(self.style.WARNING('User "temp_admin" already exists.'))
