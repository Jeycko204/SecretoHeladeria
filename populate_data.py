import os
import django
import random
from datetime import timedelta
from django.utils import timezone
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secreto_heladeria.settings')
django.setup()

from django.contrib.auth.models import User
from compras.models import UserProfile, Categoria, Proveedor, Insumo, OrdenCompra, DetalleOrden, Compra

def populate():
    print("--- Starting Data Population ---")

    # 1. Create Users and Profiles
    users_data = [
        {'username': 'jefe_compras', 'email': 'compras@secreto.cl', 'password': 'password123', 'dept': 'COMPRAS'},
        {'username': 'analista_finanzas', 'email': 'finanzas@secreto.cl', 'password': 'password123', 'dept': 'FINANZAS'},
        {'username': 'bodeguero', 'email': 'bodega@secreto.cl', 'password': 'password123', 'dept': 'BODEGA'},
        {'username': 'admin_general', 'email': 'admin@secreto.cl', 'password': 'password123', 'dept': 'COMPRAS', 'is_superuser': True},
    ]

    users = {}
    for u_data in users_data:
        user, created = User.objects.get_or_create(username=u_data['username'], defaults={
            'email': u_data['email'],
            'is_staff': True,
            'is_superuser': u_data.get('is_superuser', False)
        })
        if created:
            user.set_password(u_data['password'])
            user.save()
            print(f"Created user: {user.username}")
        
        # Create/Update Profile
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.department = u_data['dept']
        profile.save()
        users[u_data['username']] = user

    # 2. Create Categories
    categories = ['Lácteos', 'Frutas', 'Envases', 'Saborizantes', 'Limpieza']
    cats_objs = {}
    for cat_name in categories:
        c, _ = Categoria.objects.get_or_create(nombre=cat_name)
        cats_objs[cat_name] = c
    print(f"Categories ensure: {list(cats_objs.keys())}")

    # 3. Create Insumos & Proveedores
    # Helper to create provider
    def create_provider(name, cat_name, rut, insumos_list):
        cat = cats_objs[cat_name]
        prov, created = Proveedor.objects.get_or_create(rut=rut, defaults={
            'nombre': name,
            'contacto': f'Contacto {name}',
            'telefono': '912345678',
            'email': f'contacto@{name.lower().replace(" ", "")}.cl',
            'direccion': f'Av {name} 123',
            'tiempo_entrega': 2,
            'monto_minimo': 50000,
            'categoria': cat,
            'dias_entrega': 'LUN,MIE,VIE'
        })
        
        # Create and link insumos
        for ins_name, unit in insumos_list:
            ins, _ = Insumo.objects.get_or_create(nombre=ins_name, categoria=cat, defaults={'unidad_medida': unit})
            prov.insumos.add(ins)
        return prov

    prov_lacteos = create_provider('Lacteos del Sur', 'Lácteos', '76123456-1', [('Leche Entera', 'L'), ('Crema de Leche', 'L'), ('Manjar', 'kg')])
    prov_frutas = create_provider('Frutas Frescas SPA', 'Frutas', '76123456-2', [('Frutillas', 'kg'), ('Plátanos', 'kg'), ('Frambuesas', 'kg')])
    prov_envases = create_provider('Envases Chile', 'Envases', '76123456-3', [('Vaso 100ml', 'unidad'), ('Cucharas', 'caja'), ('Servilletas', 'paquete')])
    
    providers = [prov_lacteos, prov_frutas, prov_envases]
    print("Providers created.")

    # 4. Create OrdenCompra in various states
    
    # Helper to create order
    def create_order(user, status, provider, items):
        order = OrdenCompra.objects.create(
            solicitante=user,
            estado=status,
            neto=0, iva=0, monto_total=0 # Will update later
        )
        
        for insumo_obj, qty, price in items:
            DetalleOrden.objects.create(
                orden=order,
                proveedor=provider,
                insumo=insumo_obj.nombre,
                insumo_fk=insumo_obj,
                unidad_medida=insumo_obj.unidad_medida,
                cantidad=qty,
                precio_unitario=price,
                subtotal=qty*price
            )
        
        order.update_totals()
        return order

    # get some insumos
    ins_leche = Insumo.objects.get(nombre='Leche Entera')
    ins_frutilla = Insumo.objects.get(nombre='Frutillas')
    ins_vasos = Insumo.objects.get(nombre='Vaso 100ml')

    # A. En Espera (Created by Compras)
    oc_espera = create_order(users['jefe_compras'], 'EN_ESPERA', prov_lacteos, [
        (ins_leche, 50, 1000), 
        (Insumo.objects.get(nombre='Crema de Leche'), 20, 4000)
    ])
    print(f"Created OC En Espera: {oc_espera}")

    # B. Aprobada (Approved seems to settle implicitly, usually manual action, but we set state directly)
    oc_aprobada = create_order(users['jefe_compras'], 'APROBADA', prov_frutas, [
        (ins_frutilla, 10, 3500)
    ])
    print(f"Created OC Aprobada: {oc_aprobada}")

    # C. Rechazada
    oc_rechazada = create_order(users['jefe_compras'], 'RECHAZADO', prov_envases, [
        (ins_vasos, 1000, 50)
    ])
    oc_rechazada.motivo_anulacion = "Presupuesto excedido"
    oc_rechazada.usuario_anulo = users['analista_finanzas']
    oc_rechazada.fecha_anulacion = timezone.now()
    oc_rechazada.save()
    print(f"Created OC Rechazada: {oc_rechazada}")

    # D. Cerrada (Simulating full cycle -> Compra)
    oc_cerrada = create_order(users['jefe_compras'], 'CERRADA', prov_lacteos, [
        (ins_leche, 100, 950)
    ])
    # Create associated Compra manually as logic usually does
    Compra.objects.create(
        proveedor=prov_lacteos,
        nombre_proveedor=prov_lacteos.nombre,
        numero_factura=f"AUTOGEN-{oc_cerrada.id}",
        fecha_compra=timezone.now().date(),
        monto_total=oc_cerrada.monto_total,
        direccion_entrega=prov_lacteos.direccion,
        correo_contacto=prov_lacteos.email,
        descripcion=f"Generada desde OC-{oc_cerrada.id}"
    )
    print(f"Created OC Cerrada and Compra: {oc_cerrada}")

    print("--- Population Complete ---")

if __name__ == '__main__':
    populate()
