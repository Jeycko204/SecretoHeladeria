import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secreto_heladeria.settings')
django.setup()

from django.contrib.auth.models import User
from compras.models import UserProfile, OrdenCompra, DetalleOrden, Proveedor, Insumo, Categoria

def create_test_data():
    print("Creating test data...")

    # 1. Create Users and Profiles
    users_data = [
        {'username': 'finanzas', 'password': 'password123', 'dept': 'FINANZAS'},
        {'username': 'bodega', 'password': 'password123', 'dept': 'BODEGA'},
        {'username': 'compras', 'password': 'password123', 'dept': 'COMPRAS'},
    ]

    created_users = []

    for u_data in users_data:
        user, created = User.objects.get_or_create(username=u_data['username'])
        if created:
            user.set_password(u_data['password'])
            user.save()
            print(f"Created user: {u_data['username']}")
        else:
            print(f"User already exists: {u_data['username']}")
        
        # Create or update profile
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.department = u_data['dept']
        profile.save()
        created_users.append(user)

    # 2. Ensure basic data (Category, Provider, Insumo)
    cat, _ = Categoria.objects.get_or_create(nombre="General")
    prov, _ = Proveedor.objects.get_or_create(
        rut="11111111-1",
        defaults={
            'nombre': 'Proveedor Test',
            'contacto': 'Juan Test',
            'telefono': '123456789',
            'email': 'test@proveedor.com',
            'direccion': 'Calle Test 123',
            'tiempo_entrega': 1,
            'monto_minimo': 10000,
            'categoria': cat
        }
    )
    insumo, _ = Insumo.objects.get_or_create(
        nombre="Insumo Test",
        defaults={'categoria': cat, 'unidad_medida': 'Unidad'}
    )

    # 3. Create Orders
    # Order 1: En Espera
    oc1 = OrdenCompra.objects.create(
        solicitante=created_users[2], # compras
        estado='EN_ESPERA'
    )
    DetalleOrden.objects.create(
        orden=oc1,
        proveedor=prov,
        insumo_fk=insumo,
        insumo=insumo.nombre,
        unidad_medida='Unidad',
        cantidad=10,
        precio_unitario=1000
    )
    oc1.update_totals()
    print(f"Created Order #{oc1.id} (EN_ESPERA)")

    # Order 2: En Espera
    oc2 = OrdenCompra.objects.create(
        solicitante=created_users[2], # compras
        estado='EN_ESPERA'
    )
    DetalleOrden.objects.create(
        orden=oc2,
        proveedor=prov,
        insumo_fk=insumo,
        insumo=insumo.nombre,
        unidad_medida='Unidad',
        cantidad=5,
        precio_unitario=2000
    )
    oc2.update_totals()
    print(f"Created Order #{oc2.id} (EN_ESPERA)")

    # Order 3: Aprobada
    oc3 = OrdenCompra.objects.create(
        solicitante=created_users[2], # compras
        estado='APROBADA'
    )
    DetalleOrden.objects.create(
        orden=oc3,
        proveedor=prov,
        insumo_fk=insumo,
        insumo=insumo.nombre,
        unidad_medida='Unidad',
        cantidad=20,
        precio_unitario=500
    )
    oc3.update_totals()
    print(f"Created Order #{oc3.id} (APROBADA)")

    print("\nDone! Test credentials:")
    for u in users_data:
        print(f"User: {u['username']} | Pass: {u['password']} | Role: {u['dept']}")

if __name__ == '__main__':
    create_test_data()
