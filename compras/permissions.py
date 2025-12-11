from rest_framework import permissions

class IsJefeCompras(permissions.BasePermission):
    """
    Permite acceso a usuarios del grupo 'COMPRAS' o Staff.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff or request.user.is_superuser:
            return True
        return request.user.groups.filter(name='COMPRAS').exists()

class IsBodeguero(permissions.BasePermission):
    """
    Permite acceso a usuarios del grupo 'BODEGA' o Staff.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff or request.user.is_superuser:
            return True
        return request.user.groups.filter(name='BODEGA').exists()

class IsFinanzas(permissions.BasePermission):
    """
    Permite acceso a usuarios del grupo 'FINANZAS' o Staff.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff or request.user.is_superuser:
            return True
        return request.user.groups.filter(name='FINANZAS').exists()

class IsJefeComprasOrReadOnly(permissions.BasePermission):
    """
    Lectura para todos los autenticados, escritura solo para COMPRAS.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff or request.user.is_superuser:
            return True
        return request.user.groups.filter(name='COMPRAS').exists()
