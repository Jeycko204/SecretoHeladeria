from django.urls import path
from . import views

app_name = 'compras'

urlpatterns = [
    path("", views.vista_inventario, name="compras"),
    path("proveedores/", views.lista_proveedores, name="proveedores_list"),
    path("proveedores/crear/", views.crear_proveedor, name="proveedor_create"),

    path("proveedores/<int:pk>/eliminar/", views.eliminar_proveedor, name="proveedor_delete"),
    path("proveedores/<int:pk>/editar/", views.editar_proveedor, name="proveedor_edit"),
    path("proveedores/<int:pk>/evaluar/", views.evaluar_proveedor, name="proveedor_evaluar"),
    path("proveedores/<int:pk>/historial/", views.historial_evaluaciones_proveedor, name="proveedor_historial"),
    path("categorias/", views.lista_categorias, name="categorias_list"),
    path("categorias/crear/", views.crear_categoria, name="categoria_create"),

    path("categorias/<int:pk>/editar/", views.editar_categoria, name="categoria_edit"),
    path("categorias/<int:pk>/eliminar/", views.eliminar_categoria, name="categoria_delete"),

    path("compras/", views.lista_compras, name="compras_list"),
    path("compras/crear/", views.crear_compra, name="compra_create"),
    path("compras/<int:pk>/eliminar/", views.eliminar_compra, name="compra_delete"),
    path("compras/<int:pk>/editar/", views.editar_compra, name="compra_edit"),
    path("compras/<int:pk>/", views.detalle_compra, name="compra_detail"),
    
    path("ordenes/", views.lista_ordenes_compra, name="orden_compra_list"),
    path("ordenes/historial-anulaciones/", views.historial_anulaciones, name="historial_anulaciones"),
    path("ordenes/crear/", views.crear_orden_compra, name="orden_compra_create"),
    path("ordenes/<int:pk>/editar/", views.editar_orden_compra, name="orden_compra_edit"),
    path("ordenes/<int:pk>/anular/", views.anular_orden_compra, name="orden_compra_anular"),
    path("ordenes/<int:pk>/aprobar/", views.aprobar_orden_compra, name="orden_compra_aprobar"),
    path("ordenes/<int:pk>/cerrar/", views.cerrar_orden_compra, name="orden_compra_cerrar"),
    path("ordenes/<int:pk>/", views.detalle_orden_compra, name="orden_compra_detail"),
    
    # Export URLs
    path("compras/export/excel/", views.exportar_compras_excel, name="export_compras_excel"),
    path("compras/export/pdf/", views.exportar_compras_pdf, name="export_compras_pdf"),
    path("ordenes/export/excel/", views.exportar_ordenes_excel, name="export_ordenes_excel"),
    path("ordenes/export/pdf/", views.exportar_ordenes_pdf, name="export_ordenes_pdf"),
    path("proveedores/export/excel/", views.exportar_proveedores_excel, name="export_proveedores_excel"),
    path("proveedores/export/pdf/", views.exportar_proveedores_pdf, name="export_proveedores_pdf"),
    path("api/insumos/", views.api_obtener_insumos, name="api_get_insumos"),
    path("api/proveedores/", views.api_obtener_proveedores, name="api_get_proveedores"),
    
    # Order status change URLs
    path("ordenes/<int:pk>/rechazar/", views.rechazar_orden_compra, name="orden_compra_rechazar"),
    
    # Notification URLs
    path("notifications/", views.lista_notificaciones, name="notifications_list"),
    path("notifications/<int:pk>/mark-read/", views.marcar_notificacion_leida, name="notification_mark_read"),
    path("notifications/unread-count/", views.contar_notificaciones_no_leidas, name="notification_unread_count"),
]
