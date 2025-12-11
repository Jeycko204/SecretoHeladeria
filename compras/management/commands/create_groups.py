from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Crea los grupos de usuarios por defecto (COMPRAS, FINANZAS, BODEGA)'

    def handle(self, *args, **options):
        grupos = ['COMPRAS', 'FINANZAS', 'BODEGA']
        for nombre in grupos:
            grupo, created = Group.objects.get_or_create(name=nombre)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Grupo "{nombre}" creado exitosamente'))
            else:
                self.stdout.write(self.style.WARNING(f'Grupo "{nombre}" ya existe'))
