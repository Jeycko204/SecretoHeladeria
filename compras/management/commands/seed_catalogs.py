from django.core.management.base import BaseCommand
from compras.models import Categoria, Insumo

class Command(BaseCommand):
    help = 'Crea categorías e insumos base para pruebas'

    def handle(self, *args, **options):
        # 1. Categorías
        cat_lacteos, _ = Categoria.objects.get_or_create(nombre='Lácteos')
        cat_bebidas, _ = Categoria.objects.get_or_create(nombre='Bebidas')
        cat_frutas, _ = Categoria.objects.get_or_create(nombre='Frutas')
        
        self.stdout.write(f"Categorías: {cat_lacteos}, {cat_bebidas}, {cat_frutas}")

        # 2. Insumos
        insumos_data = [
            ('Leche Entera', 'LT', cat_lacteos),
            ('Yoghurt Natural', 'KG', cat_lacteos),
            ('Jugo de Naranja', 'LT', cat_bebidas),
            ('Bebida Cola', 'LT', cat_bebidas),
            ('Frutillas', 'KG', cat_frutas),
            ('Plátanos', 'KG', cat_frutas),
        ]

        for nombre, unidad, cat in insumos_data:
            insumo, created = Insumo.objects.get_or_create(
                nombre=nombre,
                defaults={'unidad_medida': unidad, 'categoria': cat}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Insumo creado: {nombre}'))
            else:
                self.stdout.write(f'Insumo ya existe: {nombre}')
