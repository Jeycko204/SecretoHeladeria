from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from compras.models import UserProfile


class Command(BaseCommand):
    help = 'Create warehouse and finance workers with their profiles'

    def handle(self, *args, **kwargs):
        # Create warehouse worker
        try:
            warehouse_user, created = User.objects.get_or_create(
                username='bodega',
                defaults={
                    'email': 'bodega@secretoheladeria.cl',
                    'first_name': 'Trabajador',
                    'last_name': 'Bodega'
                }
            )
            
            if created:
                warehouse_user.set_password('bodega123')
                warehouse_user.save()
                
                # Create profile for warehouse worker
                UserProfile.objects.get_or_create(
                    user=warehouse_user,
                    defaults={'department': 'BODEGA'}
                )
                
                self.stdout.write(self.style.SUCCESS(f'✓ Usuario de bodega creado: {warehouse_user.username}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Usuario de bodega ya existe: {warehouse_user.username}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creando usuario de bodega: {e}'))

        # Create finance worker
        try:
            finance_user, created = User.objects.get_or_create(
                username='finanzas',
                defaults={
                    'email': 'finanzas@secretoheladeria.cl',
                    'first_name': 'Trabajador',
                    'last_name': 'Finanzas'
                }
            )
            
            if created:
                finance_user.set_password('finanzas123')
                finance_user.save()
                
                # Create profile for finance worker
                UserProfile.objects.get_or_create(
                    user=finance_user,
                    defaults={'department': 'FINANZAS'}
                )
                
                self.stdout.write(self.style.SUCCESS(f'✓ Usuario de finanzas creado: {finance_user.username}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Usuario de finanzas ya existe: {finance_user.username}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creando usuario de finanzas: {e}'))

        self.stdout.write(self.style.SUCCESS('\n=== RESUMEN ==='))
        self.stdout.write(self.style.SUCCESS('Credenciales de acceso:'))
        self.stdout.write(self.style.SUCCESS("- Bodega: username='bodega', password='bodega123'"))
        self.stdout.write(self.style.SUCCESS("- Finanzas: username='finanzas', password='finanzas123'"))
