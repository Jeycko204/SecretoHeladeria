from django.contrib.auth.models import User
from .models import Notification, UserProfile

def create_notification(user, notification_type, orden, message):
    """Crea una notificación para un usuario específico."""
    Notification.objects.create(
        user=user,
        notification_type=notification_type,
        orden_compra=orden,
        message=message
    )

def get_users_by_department(department):
    """Obtiene todos los usuarios de un departamento específico."""
    return User.objects.filter(profile__department=department)

def notify_finance_new_order(orden):
    """Notifica a Finanzas que hay una nueva orden en espera."""
    finance_users = get_users_by_department('FINANZAS')
    for user in finance_users:
        create_notification(
            user,
            'ORDER_CREATED',
            orden,
            f"Nueva Orden de Compra #{orden.id} requiere aprobación."
        )

def notify_bodega_approved_order(orden):
    """Notifica a Bodega que una orden ha sido aprobada."""
    bodega_users = get_users_by_department('BODEGA')
    for user in bodega_users:
        create_notification(
            user,
            'ORDER_APPROVED',
            orden,
            f"Orden de Compra #{orden.id} aprobada y lista para recepción."
        )

def notify_compras_status_change(orden):
    """Notifica al departamento de Compras sobre cambios de estado (Aprobada/Rechazada)."""
    compras_users = get_users_by_department('COMPRAS')
    
    status_msg = ""
    notif_type = ""
    
    if orden.estado == 'APROBADA':
        status_msg = "ha sido APROBADA"
        notif_type = 'ORDER_APPROVED'
    elif orden.estado == 'RECHAZADA':
        status_msg = "ha sido RECHAZADA"
        notif_type = 'ORDER_REJECTED'
    elif orden.estado == 'CERRADA':
        status_msg = "ha sido CERRADA"
        notif_type = 'ORDER_CLOSED'
        
    for user in compras_users:
        create_notification(
            user,
            notif_type,
            orden,
            f"Orden de Compra #{orden.id} {status_msg}."
        )
