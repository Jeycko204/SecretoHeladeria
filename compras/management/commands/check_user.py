from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Checks if a user exists and is active.'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='The username to check.')

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username']
        try:
            user = User.objects.get(username=username)
            if user.is_active:
                self.stdout.write(self.style.SUCCESS(f'User "{username}" exists and is active.'))
            else:
                self.stdout.write(self.style.WARNING(f'User "{username}" exists but is inactive.'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" does not exist.'))
