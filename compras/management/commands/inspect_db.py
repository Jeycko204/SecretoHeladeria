from django.core.management.base import BaseCommand
from compras.models import Proveedor, Categoria, Insumo

class Command(BaseCommand):
    help = 'Muestra el estado de la base de datos para depuración'

    def handle(self, *args, **options):
        self.stdout.write("=== CATEGORIAS ===")
        for c in Categoria.objects.all():
            self.stdout.write(f"ID: {c.id} | Nombre: {c.nombre}")
            
        self.stdout.write("\n=== INSUMOS ===")
        for i in Insumo.objects.all():
            self.stdout.write(f"ID: {i.id} | Nombre: {i.nombre} | Cat ID: {i.categoria.id if i.categoria else 'None'}")
            
        self.stdout.write("\n=== PROVEEDORES ===")
        for p in Proveedor.objects.all():
            insumos = p.insumos.all()
            insumos_str = ", ".join([f"{i.nombre} (Cat {i.categoria.id})" for i in insumos])
            self.stdout.write(f"ID: {p.id} | Nombre: {p.nombre}")
            self.stdout.write(f"   -> Insumos: {insumos_str if insumos else 'NINGUNO'}")
