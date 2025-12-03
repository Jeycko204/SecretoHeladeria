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
