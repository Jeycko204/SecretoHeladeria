from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from compras.models import UserProfile

class Command(BaseCommand):
    help = 'Sets up initial users, groups and profiles for the application'

    def handle(self, *args, **kwargs):
        # Define configuration
        users_config = [
            {
                'username': 'bodega',
                'email': 'bodega@test.cl',
                'password': '123',
                'group': 'Inventario',
                'department': 'BODEGA'
            },
            {
                'username': 'finanzas',
                'email': 'finanzas@test.cl',
                'password': '123',
                'group': 'Finanzas',
                'department': 'FINANZAS'
            },
            {
                'username': 'compras',
                'email': 'compras@test.cl',
                'password': '123',
                'group': 'Compras', # Implied group for symmetry, fits the logical structure
                'department': 'COMPRAS'
            }
        ]

        for config in users_config:
            # 1. Create or Get User
            user, created = User.objects.get_or_create(username=config['username'])
            user.email = config['email']
            user.set_password(config['password'])
            user.save()
            
            action = "Created" if created else "Updated"
            self.stdout.write(f'{action} user: {user.username}')

            # 2. Create or Get Group and Assign
            group, _ = Group.objects.get_or_create(name=config['group'])
            user.groups.add(group)
            self.stdout.write(f'  Added to group: {group.name}')

            # 3. Create or Update UserProfile for Department
            # Check if profile exists
            if hasattr(user, 'profile'):
                profile = user.profile
            else:
                profile = UserProfile(user=user)
            
            profile.department = config['department']
            profile.save()
            self.stdout.write(f'  Set department to: {profile.department}')
            
        self.stdout.write(self.style.SUCCESS('Successfully configured users and permissions'))
