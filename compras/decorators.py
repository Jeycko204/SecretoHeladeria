"""
Permission decorators for department-based access control
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def department_required(*departments):
    """
    Decorator to restrict views to specific departments
    
    Usage:
        @department_required('INVENTARIO', 'BODEGA')
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión')
                return redirect('login')
            
            # Get user department
            user_dept = None
            if hasattr(request.user, 'profile'):
                user_dept = request.user.profile.department
            
            # Check if user has required department
            if user_dept not in departments:
                messages.error(request, 'No tienes permiso para realizar esta acción')
                return redirect('compras:ordenes_list')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
