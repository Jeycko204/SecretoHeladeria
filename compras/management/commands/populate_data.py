from django.core.management.base import BaseCommand
from compras.models import Categoria, Proveedor, Insumo, OrdenCompra, DetalleOrden
from django.contrib.auth.models import User
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Populates the database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test data...')

        # 1. Categories
        categorias = ['Lácteos', 'Frutas', 'Envases', 'Saborizantes', 'Maquinaria']
        cat_objs = []
        for nombre in categorias:
            cat, created = Categoria.objects.get_or_create(nombre=nombre)
            cat_objs.append(cat)
        self.stdout.write(f'Created {len(cat_objs)} categories.')

        # 2. Insumos (Inputs)
        insumos_data = [
            ('Leche Entera', 'Litros', cat_objs[0]),
            ('Crema de Leche', 'Litros', cat_objs[0]),
            ('Frutillas', 'Kilos', cat_objs[1]),
            ('Plátanos', 'Kilos', cat_objs[1]),
            ('Vasos 200ml', 'Unidades', cat_objs[2]),
            ('Cucharas Plásticas', 'Unidades', cat_objs[2]),
            ('Esencia Vainilla', 'Litros', cat_objs[3]),
            ('Cacao en Polvo', 'Kilos', cat_objs[3]),
        ]
        
        insumo_objs = []
        for nombre, unidad, cat in insumos_data:
            insumo, created = Insumo.objects.get_or_create(
                nombre=nombre,
                categoria=cat,
                defaults={'unidad_medida': unidad}
            )
            insumo_objs.append(insumo)
        self.stdout.write(f'Created {len(insumo_objs)} insumos.')

        # 3. Proveedores
        proveedores_data = [
            ('Lácteos del Sur', '76.123.456-1', 'Juan Perez', 'lacteos@example.com', cat_objs[0]),
            ('Frutas Frescas SpA', '77.234.567-2', 'Maria Gonzalez', 'frutas@example.com', cat_objs[1]),
            ('Envases Chile', '78.345.678-3', 'Carlos Ruiz', 'envases@example.com', cat_objs[2]),
            ('Sabores Globales', '79.456.789-4', 'Ana Lopez', 'sabores@example.com', cat_objs[3]),
        ]

        prov_objs = []
        for nombre, rut, contacto, email, cat in proveedores_data:
            prov, created = Proveedor.objects.get_or_create(
                rut=rut,
                defaults={
                    'nombre': nombre,
                    'contacto': contacto,
                    'telefono': '+56912345678',
                    'email': email,
                    'direccion': 'Av. Siempre Viva 123',
                    'dias_entrega': 'Lunes, Jueves',
                    'tiempo_entrega': 2,
                    'categoria': cat,
                    'monto_minimo': 50000
                }
            )
            if created:
                # Add random insumos
                prov.insumos.add(*[i for i in insumo_objs if i.categoria == cat])
            prov_objs.append(prov)
        self.stdout.write(f'Created {len(prov_objs)} providers.')

        # 4. Ordenes de Compra (Purchase Orders)
        # Ensure we have a user for 'solicitante'
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.WARNING('No users found. Creating a default user.'))
            user = User.objects.create_user('testuser', 'test@example.com', 'password')

        for i in range(5):
            orden = OrdenCompra.objects.create(
                solicitante=user,
                estado='EN_ESPERA',
                neto=0, iva=0, monto_total=0
            )
            
            # Add details
            prov = random.choice(prov_objs)
            insumos_prov = prov.insumos.all()
            if not insumos_prov:
                continue
                
            for _ in range(random.randint(1, 3)):
                insumo = random.choice(insumos_prov)
                cantidad = Decimal(random.randint(10, 100))
                precio = Decimal(random.randint(1000, 5000))
                
                DetalleOrden.objects.create(
                    orden=orden,
                    proveedor=prov,
                    insumo=insumo.nombre,
                    insumo_fk=insumo,
                    unidad_medida=insumo.unidad_medida,
                    cantidad=cantidad,
                    precio_unitario=precio
                )
            
            orden.update_totals()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database with test data.'))
