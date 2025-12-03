from django.urls import path
from . import views

app_name = 'compras'

urlpatterns = [
    path("", views.inventario_view, name="compras"),
    path("proveedores/", views.proveedores_list, name="proveedores_list"),
    path("proveedores/crear/", views.proveedor_create, name="proveedor_create"),
    path("proveedores/<int:pk>/eliminar/", views.proveedor_delete, name="proveedor_delete"),
    path("proveedores/<int:pk>/eliminar/", views.proveedor_delete, name="proveedor_delete"),
    path("proveedores/<int:pk>/editar/", views.proveedor_edit, name="proveedor_edit"),
    path("proveedores/<int:pk>/evaluar/", views.proveedor_evaluar, name="proveedor_evaluar"),
    path("proveedores/<int:pk>/historial/", views.proveedor_historial_evaluaciones, name="proveedor_historial"),
    path("categorias/", views.categorias_list, name="categorias_list"),
    path("categorias/crear/", views.categoria_create, name="categoria_create"),

    path("categorias/<int:pk>/editar/", views.categoria_edit, name="categoria_edit"),
    path("categorias/<int:pk>/eliminar/", views.categoria_delete, name="categoria_delete"),

    path("compras/", views.compras_list, name="compras_list"),
    path("compras/crear/", views.compra_create, name="compra_create"),
    path("compras/<int:pk>/eliminar/", views.compra_delete, name="compra_delete"),
    path("compras/<int:pk>/editar/", views.compra_edit, name="compra_edit"),
    path("compras/<int:pk>/", views.compra_detail, name="compra_detail"),
    
    path("ordenes/", views.orden_compra_list, name="orden_compra_list"),
    path("ordenes/historial-anulaciones/", views.historial_anulaciones, name="historial_anulaciones"),
    path("ordenes/crear/", views.orden_compra_create, name="orden_compra_create"),
    path("ordenes/<int:pk>/editar/", views.orden_compra_edit, name="orden_compra_edit"),
    path("ordenes/<int:pk>/anular/", views.orden_compra_anular, name="orden_compra_anular"),
    path("ordenes/<int:pk>/aprobar/", views.orden_compra_aprobar, name="orden_compra_aprobar"),
    path("ordenes/<int:pk>/cerrar/", views.orden_compra_cerrar, name="orden_compra_cerrar"),
    path("ordenes/<int:pk>/", views.orden_compra_detail, name="orden_compra_detail"),
    
    # Export URLs
    path("compras/export/excel/", views.export_compras_excel, name="export_compras_excel"),
    path("compras/export/pdf/", views.export_compras_pdf, name="export_compras_pdf"),
    path("ordenes/export/excel/", views.export_ordenes_excel, name="export_ordenes_excel"),
    path("ordenes/export/pdf/", views.export_ordenes_pdf, name="export_ordenes_pdf"),
    path("proveedores/export/excel/", views.export_proveedores_excel, name="export_proveedores_excel"),
    path("proveedores/export/pdf/", views.export_proveedores_pdf, name="export_proveedores_pdf"),
    path("api/insumos/", views.api_get_insumos, name="api_get_insumos"),
    path("api/proveedores/", views.api_get_proveedores, name="api_get_proveedores"),
    
    # Order status change URLs
    path("ordenes/<int:pk>/rechazar/", views.orden_compra_rechazar, name="orden_compra_rechazar"),
    
    # Notification URLs
    path("notifications/", views.notifications_list, name="notifications_list"),
    path("notifications/<int:pk>/mark-read/", views.notification_mark_read, name="notification_mark_read"),
    path("notifications/unread-count/", views.notification_unread_count, name="notification_unread_count"),
]
