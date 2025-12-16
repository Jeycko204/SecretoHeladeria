from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.core.exceptions import ValidationError
import re

def vista_inicio(request):
    if not request.user.is_authenticated:
        from django.urls import reverse
        from django.shortcuts import redirect
        return redirect(reverse('login'))
    # Si el usuario es superuser (root) o staff, marcar role como 'superuser' para
    # que tenga acceso a todo el contenido en las plantillas.
    role = None
    if request.user.is_authenticated and (getattr(request.user, 'is_superuser', False) or getattr(request.user, 'is_staff', False)):
        role = 'superuser'
    else:
        try:
            if hasattr(request.user, 'profile') and request.user.profile.department:
                role = request.user.profile.department # 'COMPRAS', 'BODEGA', 'FINANZAS'
            else:
                # Alternativa: verificar grupos
                if request.user.groups.filter(name='BODEGA').exists():
                    role = 'BODEGA'
                elif request.user.groups.filter(name='COMPRAS').exists():
                    role = 'COMPRAS'
                elif request.user.groups.filter(name='FINANZAS').exists():
                    role = 'FINANZAS'
                else:
                    empleado = getattr(request.user, 'empleado', None)
                    role = empleado.rol if empleado else None
        except Exception:
            # Si no hay relación, el rol queda como None
            role = None
    
    allowed_roles = ['administrador', 'jefe_compras', 'superuser', 'COMPRAS', 'BODEGA', 'FINANZAS']
    can_access_compras = role in allowed_roles
    return render(request, 'home.html', {'role': role, 'can_access_compras': can_access_compras})

# Vista para registro de usuario
def vista_registro(request):
    errors = []
    if request.method == 'POST':
        def is_valid_rut(rut):
            rut = rut.upper().replace(".", "").replace("-", "")
            if not re.match(r'^[0-9]+[0-9K]$', rut):
                return False
            cuerpo = rut[:-1]
            dv = rut[-1]
            
            if not cuerpo.isdigit():
                return False

            suma = 0
            multiplo = 2
            for c in reversed(cuerpo):
                suma += int(c) * multiplo
                multiplo = multiplo + 1 if multiplo < 7 else 2
            
            resto = suma % 11
            dv_calculado = 11 - resto
            if dv_calculado == 11:
                dv_calculado = '0'
            elif dv_calculado == 10:
                dv_calculado = 'K'
            else:
                dv_calculado = str(dv_calculado)
            
            return dv == dv_calculado

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        rut = request.POST.get('rut', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        # Validaciones
        if not first_name:
            errors.append('El nombre es obligatorio.')
        if not last_name:
            errors.append('El apellido es obligatorio.')
        if not is_valid_rut(rut):
            errors.append('El RUT no es válido.')
        if not email or not re.match(r'^.{3,}@.{3,}\..+$', email):
            errors.append('El correo debe tener formato válido.')
        if not address:
            errors.append('La dirección es obligatoria.')
        if not telefono or not telefono.isdigit():
            errors.append('El teléfono debe ser numérico.')
        if not password or not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[^\w\d]).{8,}$', password):
            errors.append('La contraseña debe tener mínimo 8 caracteres, una mayúscula, una minúscula y un caracter especial.')
        if password != password2:
            errors.append('Las contraseñas no coinciden.')
        if User.objects.filter(username=rut).exists():
            errors.append('Ya existe un usuario con ese RUT.')
        if User.objects.filter(email=email).exists():
            errors.append('Ya existe un usuario con ese correo.')

        if not errors:
            user = User.objects.create_user(
                username=rut,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            # Guardar dirección y teléfono en el campo 'user.profile.address' y 'user.profile.telefono' si existe un perfil, o ignorar
            # Por ahora solo se crea el usuario
            from django.contrib.auth import login
            from compras.backends import RutAuthBackend
            login(request, user, backend='compras.backends.RutAuthBackend')
            return render(request, 'registration/login.html', {'register_success': True})
        else:
            return render(request, 'registration/register.html', {'register_errors': errors})
    else:
        return render(request, 'registration/register.html')
