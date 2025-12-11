from django.contrib import admin
from .models import Proveedor, Categoria, Compra

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "contacto", "telefono")
    search_fields = ("nombre", "contacto")

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ("numero_factura", "proveedor", "fecha_compra", "monto_total")
    search_fields = ("numero_factura", "proveedor__nombre")
    list_filter = ("proveedor", "fecha_compra")

from .models import Insumo, OrdenCompra, DetalleOrden, UserProfile

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "unidad_medida")
    list_filter = ("categoria",)

class DetalleOrdenInline(admin.TabularInline):
    model = DetalleOrden
    extra = 0

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ("id", "solicitante", "estado", "monto_total", "fecha_emision")
    list_filter = ("estado", "fecha_emision")
    inlines = [DetalleOrdenInline]

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "department")
    list_filter = ("department",)

