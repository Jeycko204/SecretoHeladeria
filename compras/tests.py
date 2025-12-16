from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Proveedor, Categoria, Insumo, OrdenCompra, DetalleOrden, UserProfile
from decimal import Decimal

class SystemVerificationTests(TestCase):
    def setUp(self):
        # Create basic data
        self.categoria = Categoria.objects.create(nombre="Lácteos")
        self.insumo = Insumo.objects.create(
            nombre="Leche",
            categoria=self.categoria,
            unidad_medida="Litros"
        )
        self.user = User.objects.create_user(username='testuser', password='password')
        
    def test_proveedor_creation(self):
        """Verify Proveedor can be created with valid data"""
        proveedor = Proveedor.objects.create(
            nombre="Proveedor Test",
            rut="12345678-9",
            contacto="Juan Perez",
            telefono="+56912345678",
            email="contacto@proveedor.com",
            direccion="Calle Falsa 123",
            tiempo_entrega=3,
            monto_minimo=15000
        )
        self.assertEqual(proveedor.nombre, "Proveedor Test")
        self.assertEqual(Proveedor.objects.count(), 1)

    def test_orden_compra_workflow(self):
        """Verify the full workflow of an OrdenCompra"""
        proveedor = Proveedor.objects.create(
            nombre="Proveedor Test",
            rut="12345678-9",
            contacto="Juan Perez",
            telefono="+56912345678",
            email="contacto@proveedor.com",
            direccion="Calle Falsa 123",
            tiempo_entrega=3,
            monto_minimo=15000
        )
        
        # 1. Create Order
        orden = OrdenCompra.objects.create(solicitante=self.user)
        self.assertEqual(orden.estado, 'EN_ESPERA')
        self.assertEqual(orden.monto_total, 0)
        
        # 2. Add Details
        detalle = DetalleOrden.objects.create(
            orden=orden,
            proveedor=proveedor,
            insumo_fk=self.insumo,
            unidad_medida="Litros",
            cantidad=10,
            precio_unitario=1000
        )
        
        # 3. Verify Totals
        orden.refresh_from_db()
        self.assertEqual(orden.neto, 10000) # 10 * 1000
        self.assertEqual(orden.iva, 1900)   # 10000 * 0.19
        self.assertEqual(orden.monto_total, 11900)
        
        # 4. Change Status
        orden.estado = 'APROBADA'
        orden.save()
        self.assertEqual(orden.estado, 'APROBADA')
        
        orden.estado = 'RECHAZADA'
        orden.save()
        self.assertEqual(orden.estado, 'RECHAZADA')

class SystemIntegrationTests(TestCase):
    def setUp(self):
        # Setup Users
        self.user_compras = User.objects.create_user(username='compras', password='password')
        UserProfile.objects.create(user=self.user_compras, department='COMPRAS')
        
        self.user_finanzas = User.objects.create_user(username='finanzas', password='password')
        UserProfile.objects.create(user=self.user_finanzas, department='FINANZAS')
        
        self.user_bodega = User.objects.create_user(username='bodega', password='password')
        UserProfile.objects.create(user=self.user_bodega, department='BODEGA')
        
        # Setup Data
        self.categoria = Categoria.objects.create(nombre="Lácteos")
        self.insumo = Insumo.objects.create(
            nombre="Leche",
            categoria=self.categoria,
            unidad_medida="Litros"
        )
        self.proveedor = Proveedor.objects.create(
            nombre="Proveedor Test",
            rut="12345678-9",
            contacto="Juan Perez",
            telefono="+56912345678",
            email="contacto@proveedor.com",
            direccion="Calle Falsa 123",
            tiempo_entrega=3,
            monto_minimo=15000
        )
        self.proveedor.insumos.add(self.insumo)
        
        self.client = Client()

    def test_create_order_view(self):
        """Test creating an order via the view (COMPRAS user)"""
        self.client.force_login(self.user_compras)
        
        # Prepare POST data for formset
        data = {
            'detalles-TOTAL_FORMS': '1',
            'detalles-INITIAL_FORMS': '0',
            'detalles-MIN_NUM_FORMS': '0',
            'detalles-MAX_NUM_FORMS': '1000',
            
            'detalles-0-proveedor': self.proveedor.id,
            'detalles-0-insumo_fk': self.insumo.id,
            'detalles-0-unidad_medida': 'Litros',
            'detalles-0-cantidad': '10',
            'detalles-0-precio_unitario': '1000',
        }
        
        response = self.client.post(reverse('compras:orden_compra_create'), data)
        
        # Check redirection (success)
        self.assertRedirects(response, reverse('compras:orden_compra_list'))
        
        # Check order created
        self.assertEqual(OrdenCompra.objects.count(), 1)
        orden = OrdenCompra.objects.first()
        self.assertEqual(orden.estado, 'EN_ESPERA')
        self.assertEqual(orden.monto_total, 11900)

    def test_approve_order_view(self):
        """Test approving an order via the view (FINANZAS user)"""
        # Create order first
        orden = OrdenCompra.objects.create(solicitante=self.user_compras, estado='EN_ESPERA')
        DetalleOrden.objects.create(
            orden=orden,
            proveedor=self.proveedor,
            insumo_fk=self.insumo,
            unidad_medida="Litros",
            cantidad=10,
            precio_unitario=1000
        )
        orden.update_totals()
        
        self.client.force_login(self.user_finanzas)
        response = self.client.post(reverse('compras:orden_compra_aprobar', args=[orden.id]))
        
        self.assertRedirects(response, reverse('compras:orden_compra_detail', args=[orden.id]))
        
        orden.refresh_from_db()
        self.assertEqual(orden.estado, 'APROBADA')

    def test_reject_order_view(self):
        """Test rejecting an order via the view (FINANZAS user)"""
        orden = OrdenCompra.objects.create(solicitante=self.user_compras, estado='EN_ESPERA')
        
        self.client.force_login(self.user_finanzas)
        response = self.client.post(reverse('compras:orden_compra_rechazar', args=[orden.id]))
        
        self.assertRedirects(response, reverse('compras:orden_compra_detail', args=[orden.id]))
        
        orden.refresh_from_db()
        self.assertEqual(orden.estado, 'RECHAZADA')

    def test_close_order_view(self):
        """Test closing an order via the view (BODEGA user)"""
        orden = OrdenCompra.objects.create(solicitante=self.user_compras, estado='APROBADA')
        DetalleOrden.objects.create(
            orden=orden,
            proveedor=self.proveedor,
            insumo_fk=self.insumo,
            unidad_medida="Litros",
            cantidad=10,
            precio_unitario=1000
        )
        orden.update_totals()
        
        self.client.force_login(self.user_bodega)
        response = self.client.post(reverse('compras:orden_compra_cerrar', args=[orden.id]))
        
        self.assertRedirects(response, reverse('compras:compras_list'))
        
        orden.refresh_from_db()
        self.assertEqual(orden.estado, 'CERRADA')
