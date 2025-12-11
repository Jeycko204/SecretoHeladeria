from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from .validators import validate_rut, validate_email_format, validate_pdf_file, validate_phone

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Insumo(models.Model):
    nombre = models.CharField("Nombre del insumo", max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='insumos')
    unidad_medida = models.CharField("Unidad de medida", max_length=50)
    
    def __str__(self):
        return f"{self.nombre} ({self.unidad_medida})"


class Proveedor(models.Model):
    DIAS_CHOICES = [
        ('LUN', 'Lunes'),
        ('MAR', 'Martes'),
        ('MIE', 'Miércoles'),
        ('JUE', 'Jueves'),
        ('VIE', 'Viernes'),
        ('SAB', 'Sábado'),
        ('DOM', 'Domingo'),
    ]

    nombre = models.CharField("Nombre de la empresa", max_length=100)
    rut = models.CharField("RUT", max_length=12, unique=True, validators=[validate_rut])
    contacto = models.CharField("Contacto principal", max_length=100)
    telefono = models.CharField("Teléfono", max_length=20, validators=[validate_phone])
    email = models.EmailField("Email", validators=[validate_email_format])
    direccion = models.CharField("Dirección de entrega", max_length=255)
    dias_entrega = models.CharField("Días de entrega", max_length=50, blank=True, help_text="Días en que el proveedor realiza entregas (ej: Lunes, Miércoles).")
    tiempo_entrega = models.PositiveIntegerField("Tiempo de entrega (días)", validators=[MinValueValidator(1), MaxValueValidator(30)])
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, blank=True, null=True, help_text="Categoría principal del proveedor")
    monto_minimo = models.DecimalField("Monto mínimo de pedido", max_digits=12, decimal_places=0, validators=[MinValueValidator(10000)])
    certificacion = models.FileField("Certificación (PDF)", upload_to='certificaciones/', blank=True, null=True, validators=[validate_pdf_file])
    insumos = models.ManyToManyField(Insumo, related_name='proveedores', blank=True, help_text="Insumos que ofrece este proveedor")
    
    # Secondary contact fields
    agregar_contacto_secundario = models.BooleanField("¿Agregar contacto secundario?", default=False)
    contacto_secundario_nombre = models.CharField("Nombre contacto secundario", max_length=100, blank=True)
    contacto_secundario_apellido = models.CharField("Apellido contacto secundario", max_length=100, blank=True)
    contacto_secundario_rut = models.CharField("RUT contacto secundario", max_length=12, blank=True)
    contacto_secundario_telefono = models.CharField("Teléfono contacto secundario", max_length=20, blank=True)
    contacto_secundario_email = models.EmailField("Email contacto secundario", blank=True)
    contacto_secundario_direccion = models.CharField("Dirección contacto secundario", max_length=255, blank=True)


    def __str__(self):
        return self.nombre



class Compra(models.Model):
    """Representa una compra realizada a un proveedor."""
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True, related_name='compras')
    nombre_proveedor = models.CharField("Nombre proveedor (histórico)", max_length=200, blank=True, help_text="Nombre del proveedor en el momento de la compra")
    numero_factura = models.CharField("Número de Factura", max_length=50, unique=True, validators=[MinLengthValidator(3)])
    fecha_compra = models.DateField("Fecha de Compra")
    monto_total = models.DecimalField("Monto Total", max_digits=12, decimal_places=0, validators=[MinValueValidator(0)])
    direccion_entrega = models.CharField("Dirección de entrega", max_length=255)
    correo_contacto = models.EmailField("Correo de contacto")
    
    descripcion = models.TextField("Descripción", blank=True, help_text="Detalles de la compra (opcional).")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_compra']

    def __str__(self):
        prov_name = self.proveedor.nombre if self.proveedor else (self.nombre_proveedor or "(Proveedor eliminado)")
        return f"Factura {self.numero_factura} de {prov_name}"

    def clean(self):
        if self.monto_total < 0:
            raise ValidationError({'monto_total': 'El monto total no puede ser negativo.'})
        # La fecha de la compra debe ser la fecha actual (no se permiten fechas pasadas)
        if self.fecha_compra != date.today():
            raise ValidationError({'fecha_compra': 'La fecha de la compra debe ser la fecha actual.'})

    def save(self, *args, **kwargs):
        # Copiar el nombre del proveedor para conservar historial
        if self.proveedor:
            try:
                self.nombre_proveedor = self.proveedor.nombre
            except Exception:
                pass
        # Ejecutar validaciones de modelo
        self.clean()
        super().save(*args, **kwargs)

class OrdenCompra(models.Model):
    ESTADO_CHOICES = [
        ('EN_ESPERA', 'En Espera'),
        ('APROBADA', 'Aprobada'),
        ('RECHAZADA', 'Rechazada'),
        ('CERRADA', 'Cerrada'),
        ('ANULADA', 'Anulada'),
    ]

    # proveedor removed from OrdenCompra to allow multi-provider orders
    fecha_emision = models.DateField("Fecha de emisión", auto_now_add=True)
    neto = models.DecimalField("Neto", max_digits=12, decimal_places=0, default=0)
    iva = models.DecimalField("IVA (19%)", max_digits=12, decimal_places=0, default=0)
    monto_total = models.DecimalField("Monto Total", max_digits=12, decimal_places=0, default=0)
    estado = models.CharField("Estado", max_length=20, choices=ESTADO_CHOICES, default='EN_ESPERA')
    solicitante = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_solicitadas')
    
    # Campos para historial de anulaciones
    motivo_anulacion = models.TextField("Motivo de anulación", blank=True, null=True)
    usuario_anulo = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_anuladas')
    fecha_anulacion = models.DateTimeField("Fecha de anulación", null=True, blank=True)
    updated_at = models.DateTimeField("Última actualización", auto_now=True)

    def __str__(self):
        return f"OC-{self.id}"

    def update_totals(self):
        from decimal import Decimal
        self.neto = sum(detalle.subtotal for detalle in self.detalles.all())
        self.iva = self.neto * Decimal('0.19')
        self.monto_total = self.neto + self.iva
        self.save()

class DetalleOrden(models.Model):
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='detalles')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='detalles_orden')
    insumo = models.CharField("Insumo (Texto)", max_length=200, blank=True, help_text="Nombre del insumo (histórico o manual)")
    insumo_fk = models.ForeignKey(Insumo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Insumo (Catálogo)")
    unidad_medida = models.CharField("Unidad de medida", max_length=50)

    cantidad = models.DecimalField("Cantidad", max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    precio_unitario = models.DecimalField("Precio unitario", max_digits=12, decimal_places=0, validators=[MinValueValidator(1)])
    subtotal = models.DecimalField("Subtotal", max_digits=12, decimal_places=0, editable=False)
    fecha = models.DateField("Fecha", auto_now_add=True)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        # Update total of the order
        self.orden.update_totals()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.orden.update_totals()

class EvaluacionProveedor(models.Model):
    CALIDAD_CHOICES = [
        ('EXCELENTE', 'Excelente'),
        ('BUENO', 'Bueno'),
        ('MEDIO', 'Medio'),
        ('MALO', 'Malo'),
        ('MUY_MALO', 'Muy malo'),
    ]

    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='evaluaciones')
    usuario = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    calidad = models.CharField("Calidad", max_length=20, choices=CALIDAD_CHOICES)
    fecha = models.DateField("Fecha", auto_now_add=True)
    descripcion = models.TextField("Descripción breve", max_length=200)

    def __str__(self):
        return f"Evaluación de {self.proveedor.nombre} - {self.get_calidad_display()}"

# Notification System Models

DEPARTMENT_CHOICES = [
    ('COMPRAS', 'Compras'),
    ('INVENTARIO', 'Inventario'),
    ('BODEGA', 'Bodega'),
    ('FINANZAS', 'Finanzas'),
]

class UserProfile(models.Model):
    """User profile to store department information"""
    from django.contrib.auth.models import User
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    department = models.CharField("Departamento", max_length=20, choices=DEPARTMENT_CHOICES, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_department_display() if self.department else 'Sin departamento'}"
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"


class Notification(models.Model):
    """In-app notifications for order status changes"""
    from django.contrib.auth.models import User
    
    NOTIFICATION_TYPES = [
        ('ORDER_CREATED', 'Orden Creada'),
        ('ORDER_APPROVED', 'Orden Aprobada'),
        ('ORDER_REJECTED', 'Orden Rechazada'),
        ('ORDER_CLOSED', 'Orden Cerrada'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField("Tipo", max_length=20, choices=NOTIFICATION_TYPES)
    orden_compra = models.ForeignKey('OrdenCompra', on_delete=models.CASCADE)
    message = models.TextField("Mensaje")
    is_read = models.BooleanField("Leída", default=False)
    created_at = models.DateTimeField("Creada el", auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
    
    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.user.username}"
