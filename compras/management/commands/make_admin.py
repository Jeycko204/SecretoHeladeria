
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Make a user an admin'

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username='root')
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS('Successfully made "root" an admin.'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User "root" does not exist.'))
