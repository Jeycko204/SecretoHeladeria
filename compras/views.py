from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum, Q
from django.db import transaction
from django.db.models.deletion import ProtectedError
from django.contrib.auth.decorators import login_required, user_passes_test


# Chequeo para permitir acceso a superuser (root), staff, o usuarios con rol
def _admin_check(user):
    """
    Verifica si el usuario tiene permisos de administrador, ya sea por ser superusuario,
    miembro del staff, o tener un rol específico como 'jefe_compras' o 'administrador'.
    """
    if not user or not user.is_authenticated:
        return False
    if getattr(user, 'is_superuser', False) or getattr(user, 'is_staff', False):
        return True
    # Check for UserProfile department
    if hasattr(user, 'profile') and user.profile.department in ['COMPRAS', 'BODEGA', 'FINANZAS', 'INVENTARIO']:
        return True
    try:
        empleado = getattr(user, 'empleado', None)
        return bool(empleado and getattr(empleado, 'rol', None) in ('jefe_compras', 'administrador', 'bodeguero'))
    except Exception:
        return False


# admin_required actúa como decorador; redirige a 'login' si falla
admin_required = user_passes_test(_admin_check, login_url='login')

from .models import Proveedor, Categoria, Compra, OrdenCompra, DetalleOrden, EvaluacionProveedor, Insumo
from .forms import ProveedorForm, CategoriaForm, CompraForm, OrdenCompraForm, DetalleOrdenFormSet, EvaluacionProveedorForm
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

@admin_required
def inventario_view(request):
    """
    Vista principal del panel de compras. Muestra estadísticas clave como
    el número de proveedores, compras, y el gasto total.
    """
    proveedores_count = Proveedor.objects.count()
    compras_count = Compra.objects.count()
    categorias_count = Categoria.objects.count()
    from django.utils import timezone
    from datetime import timedelta
    
    # Determine permissions
    user = request.user
    role = None
    dept = None
    if hasattr(user, 'profile'):
        dept = user.profile.department
    
    # Check for legacy roles
    try:
        empleado = getattr(user, 'empleado', None)
        if empleado:
            role = empleado.rol
    except:
        pass

    is_admin = user.is_superuser or user.is_staff or role in ['administrador', 'jefe_compras']
    is_compras = dept == 'COMPRAS' or is_admin
    
    perms = {
        'can_view_proveedores': is_compras,
        'can_view_categorias': is_compras,
        'can_view_reportes': is_compras,
        'can_view_ordenes': True, # Everyone allowed here can view orders
    }

    # Gasto semanal (ultimos 7 dias)
    one_week_ago = timezone.now() - timedelta(days=7)
    gasto_total = Compra.objects.filter(fecha_compra__gte=one_week_ago).aggregate(total=Sum('monto_total'))['total'] or 0

    context = {
        'proveedores_count': proveedores_count,
        'compras_count': compras_count,
        'categorias_count': categorias_count,
        'gasto_total': gasto_total,
        'perms': perms,
    }
    return render(request, 'compras/index.html', context)

# ... (skipping unchanged parts) ...

@admin_required
def api_get_insumos(request):
    proveedor_id = request.GET.get('proveedor_id')
    categoria_id = request.GET.get('categoria_id')
    get_all = request.GET.get('all') == 'true'
    
    if get_all:
        insumos = Insumo.objects.all()
    elif proveedor_id:
        try:
            proveedor = Proveedor.objects.get(pk=proveedor_id)
            insumos = proveedor.insumos.all()
        except Proveedor.DoesNotExist:
            return JsonResponse({'error': 'Proveedor no encontrado'}, status=404)
    else:
        return JsonResponse({'error': 'Proveedor ID requerido'}, status=400)
        
    if categoria_id:
        insumos = insumos.filter(categoria_id=categoria_id)
        
    data = []
    for insumo in insumos:
        data.append({
            'id': insumo.id,
            'nombre': insumo.nombre,
            'unidad_medida': insumo.unidad_medida
        })
        
    return JsonResponse({'insumos': data})

@admin_required
def proveedores_list(request):
    """
    Muestra una lista de todos los proveedores. Permite buscar proveedores
    por nombre a través de un parámetro 'q' en la URL.
    """
    query = request.GET.get('q', '')
    proveedores = Proveedor.objects.select_related('categoria').order_by('nombre')
    if query:
        proveedores = proveedores.filter(nombre__icontains=query)
    context = {'proveedores': proveedores}
    return render(request, 'compras/proveedores_list.html', context)

@admin_required
def proveedor_create(request):
    """
    Gestiona la creación de un nuevo proveedor. Muestra un formulario vacío
    en una solicitud GET y procesa los datos del formulario en una solicitud POST.
    """
    if request.method == 'POST':
        form = ProveedorForm(request.POST, request.FILES)
        if form.is_valid():
            proveedor = form.save()
            
            # Process insumos_data
            insumos_data = request.POST.getlist('insumos_data')
            if insumos_data:
                # Parse the data structure: insumos_data[0][categoria], insumos_data[0][nombre], etc.
                insumos_dict = {}
                for key in request.POST:
                    if key.startswith('insumos_data['):
                        # Extract index and field name
                        parts = key.replace('insumos_data[', '').replace(']', '.').split('.')
                        if len(parts) >= 2:
                            index = parts[0]
                            field = parts[1]
                            if index not in insumos_dict:
                                insumos_dict[index] = {}
                            insumos_dict[index][field] = request.POST[key]
                
                # Create Insumo objects
                for insumo_data in insumos_dict.values():
                    if 'categoria' in insumo_data and 'nombre' in insumo_data and 'unidad_medida' in insumo_data:
                        # Check if insumo already exists
                        insumo, created = Insumo.objects.get_or_create(
                            nombre=insumo_data['nombre'],
                            categoria_id=insumo_data['categoria'],
                            defaults={'unidad_medida': insumo_data['unidad_medida']}
                        )
                        proveedor.insumos.add(insumo)
            
            messages.success(request, 'Proveedor creado exitosamente.')
            return redirect('compras:proveedores_list')
        else:
            # Debug: print form errors
            print("Form errors:", form.errors)
            print("Form data:", request.POST)
    else:
        form = ProveedorForm()
    return render(request, 'compras/proveedor_form.html', {
        'form': form, 
        'title': 'Crear Proveedor',
        'categorias': Categoria.objects.all()
    })

# Import export views
from .export_views import (
    export_compras_excel, export_compras_pdf,
    export_ordenes_excel, export_ordenes_pdf,
    export_proveedores_excel, export_proveedores_pdf
)

@admin_required
def compras_list(request):
    """
    Muestra el listado de todas las compras registradas con búsqueda y paginación.
    """
    query = request.GET.get('q', '')
    compras = Compra.objects.all().order_by('-fecha_compra')
    
    if query:
        compras = compras.filter(
            Q(numero_factura__icontains=query) |
            Q(nombre_proveedor__icontains=query) |
            Q(proveedor__nombre__icontains=query)
        )
    
    # Paginación
    paginator = Paginator(compras, 15)  # 15 items por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'compras': page_obj, 'query': query}
    return render(request, 'compras/compras_list.html', context)

@admin_required
def categorias_list(request):
    """Muestra una lista de todas las categorías de proveedores."""
    categorias = Categoria.objects.all()
    context = {'categorias': categorias}
    return render(request, 'compras/categorias_list.html', context)

@admin_required
def categoria_create(request):
    """
    Gestiona la creación de una nueva categoría. Muestra un formulario
    en blanco en GET y lo procesa en POST.
    """
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('compras:categorias_list')
    else:
        form = CategoriaForm()
    return render(request, 'compras/categoria_form.html', {'form': form, 'title': 'Crear Categoría'})



@admin_required
def categoria_edit(request, pk):
    """
    Permite editar una categoría existente, identificada por su clave primaria (pk).
    """
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada correctamente.')
            return redirect('compras:categorias_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'compras/categoria_form.html', {'form': form, 'title': 'Editar Categoría'})

@admin_required
def categoria_delete(request, pk):
    """
    Gestiona la eliminación de una categoría. Previene la eliminación si la
    categoría está asociada a algún proveedor para mantener la integridad de los datos.
    """
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        try:
            categoria.delete()
            messages.success(request, 'Categoría eliminada correctamente.')
            return redirect('compras:categorias_list')
        except ProtectedError:
            messages.error(request, 'No se puede eliminar esta categoría porque tiene elementos asociados.')
            return redirect('compras:categorias_list')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar la categoría: {e}')
            return redirect('compras:categorias_list')
    return render(request, 'compras/categoria_confirm_delete.html', {'categoria': categoria})


@admin_required
def compra_create(request):
    """
    Gestiona el registro de una nueva compra.
    """
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Compra registrada exitosamente.')
            return redirect('compras:compras_list')
    else:
        form = CompraForm()
    context = {'form': form, 'title': 'Registrar Nueva Compra'}
    return render(request, 'compras/compra_form.html', context)


@admin_required
def compra_delete(request, pk):
    """
    Elimina una compra específica, identificada por su clave primaria.
    """
    compra = get_object_or_404(Compra, pk=pk)
    if request.method == 'POST':
        compra.delete()
        messages.success(request, 'Compra eliminada correctamente.')
        return redirect('compras:compras_list')
    return render(request, 'compras/compra_confirm_delete.html', {'compra': compra})


@admin_required
def compra_edit(request, pk):
    """
    Permite editar los detalles de una compra existente.
    """
    compra = get_object_or_404(Compra, pk=pk)
    if request.method == 'POST':
        form = CompraForm(request.POST, instance=compra)
        if form.is_valid():
            form.save()
            messages.success(request, 'Compra actualizada correctamente.')
            return redirect('compras:compras_list')
    else:
        form = CompraForm(instance=compra)
    return render(request, 'compras/compra_form.html', {'form': form, 'title': 'Editar Compra'})


@admin_required
def compra_detail(request, pk):
    """
    Muestra los detalles completos de una compra específica.
    """
    compra = get_object_or_404(Compra, pk=pk)
    return render(request, 'compras/compra_detail.html', {'compra': compra})


@admin_required
def proveedor_delete(request, pk):
    """
    Gestiona la eliminación de un proveedor. Si el proveedor tiene compras
    asociadas, se previene la eliminación para proteger la integridad de los datos
    y se informa al usuario.
    """
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        try:
            proveedor.delete()
            messages.success(request, 'Proveedor eliminado correctamente.')
            return redirect('compras:proveedores_list')
        except ProtectedError:
            # Si hay compras asociadas, muestra una página de error con detalles.
            compras_relacionadas = Compra.objects.filter(proveedor=proveedor)
            return render(request, 'compras/proveedor_cannot_delete.html', {
                'proveedor': proveedor,
                'compras': compras_relacionadas,
            })
        except Exception as e:
            # Captura otros posibles errores durante la eliminación.
            messages.error(request, 'No se pudo eliminar el proveedor: {}'.format(e))
            return redirect('compras:proveedores_list')
    # Muestra una página de confirmación antes de eliminar.
    return render(request, 'compras/proveedor_confirm_delete.html', {'proveedor': proveedor})


@admin_required
def proveedor_edit(request, pk):
    """
    Permite editar los datos de un proveedor existente.
    """
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, request.FILES, instance=proveedor)
        if form.is_valid():
            proveedor = form.save()
            
            # Process insumos_data
            proveedor.insumos.clear()  # Clear existing insumos
            
            insumos_dict = {}
            for key in request.POST:
                if key.startswith('insumos_data['):
                    parts = key.replace('insumos_data[', '').replace(']', '.').split('.')
                    if len(parts) >= 2:
                        index = parts[0]
                        field = parts[1]
                        if index not in insumos_dict:
                            insumos_dict[index] = {}
                        insumos_dict[index][field] = request.POST[key]
            
            for insumo_data in insumos_dict.values():
                if 'categoria' in insumo_data and 'nombre' in insumo_data and 'unidad_medida' in insumo_data:
                    insumo, created = Insumo.objects.get_or_create(
                        nombre=insumo_data['nombre'],
                        categoria_id=insumo_data['categoria'],
                        defaults={'unidad_medida': insumo_data['unidad_medida']}
                    )
                    proveedor.insumos.add(insumo)
            
            messages.success(request, 'Proveedor actualizado correctamente.')
            return redirect('compras:proveedores_list')
        else:
            # Debug: print form errors
            print("EDIT Form errors:", form.errors)
            print("EDIT Form data:", request.POST)
    else:
        form = ProveedorForm(instance=proveedor)
        
    # Prepare existing insumos for JavaScript
    import json
    existing_insumos = []
    for insumo in proveedor.insumos.all():
        existing_insumos.append({
            'categoria': insumo.categoria.id if insumo.categoria else '',
            'nombre': insumo.nombre,
            'unidad_medida': insumo.unidad_medida
        })
    
    return render(request, 'compras/proveedor_form.html', {
        'form': form, 
        'title': 'Editar Proveedor',
        'categorias': Categoria.objects.all(),
        'existing_insumos_json': json.dumps(existing_insumos)
    })

from django.contrib.auth.views import LoginView
from .forms import UserAuthenticationForm, AdminAuthenticationForm

class UserLoginView(LoginView):
    authentication_form = UserAuthenticationForm
    template_name = 'registration/login.html'

class AdminLoginView(LoginView):
    authentication_form = AdminAuthenticationForm
    template_name = 'registration/admin_login.html'

@admin_required
def orden_compra_list(request):
    query = request.GET.get('q', '')
    ordenes = OrdenCompra.objects.all().order_by('-fecha_emision')
    if query:
        ordenes = ordenes.filter(
            Q(id__icontains=query)
            # Q(proveedor__nombre__icontains=query) # Removed as proveedor is not in OrdenCompra
        )
    
    # Paginación
    paginator = Paginator(ordenes, 15)  # 15 items por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Filtrar por rol
    dept = None
    if hasattr(request.user, 'profile'):
        dept = request.user.profile.department
    
    # Determine permissions
    is_admin = request.user.is_superuser or request.user.is_staff or getattr(request.user, 'empleado', None) and request.user.empleado.rol in ['administrador', 'jefe_compras']
    is_compras = dept == 'COMPRAS' or is_admin
    is_finanzas = dept == 'FINANZAS' or is_admin
    is_bodega = dept == 'BODEGA' or is_admin
    
    perms = {
        'can_create_oc': is_compras,
        'can_edit_oc': is_compras,
        'can_anular_oc': is_compras,
        'can_approve_oc': is_finanzas,
        'can_reject_oc': is_finanzas,
        'can_close_oc': is_bodega,
    }

    return render(request, 'compras/orden_compra_list.html', {'ordenes': page_obj, 'query': query, 'perms': perms})

from .decorators import department_required

@admin_required
@department_required('COMPRAS')
def orden_compra_create(request):
    source_order_id = request.GET.get('source_order_id')
    initial_data = {}
    initial_formset = []
    
    if source_order_id:
        source_order = get_object_or_404(OrdenCompra, pk=source_order_id)
        # initial_data = {'proveedor': source_order.proveedor} # Removed
        for detalle in source_order.detalles.all():
            initial_formset.append({
                'proveedor': detalle.proveedor,
                'insumo': detalle.insumo,
                'unidad_medida': detalle.unidad_medida,
                'cantidad': detalle.cantidad,
                'precio_unitario': detalle.precio_unitario,
            })

    if request.method == 'POST':
        form = OrdenCompraForm(request.POST)
        formset = DetalleOrdenFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    orden = form.save(commit=False)
                    orden.solicitante = request.user
                    orden.estado = 'PENDIENTE'
                    
                    detalles = formset.save(commit=False)
                    
                    # Validate that there is at least one detail
                    if not detalles:
                        messages.error(request, 'La orden debe tener al menos un detalle.')
                        return render(request, 'compras/orden_compra_form.html', {
                            'form': form, 
                            'formset': formset,
                            'title': 'Registrar OC'
                        })
                        
                    orden.save()
                    for detalle in detalles:
                        detalle.orden = orden
                        detalle.save()
                    
                    orden.update_totals()
                    
                    # Notify Finanzas department
                    from .notifications import notify_finance_new_order
                    notify_finance_new_order(orden)
                    
                    messages.success(request, 'Orden de compra creada exitosamente.')
                    return redirect('compras:orden_compra_list')
            except Exception as e:
                messages.error(request, f'Error al crear la orden: {str(e)}')
    else:
        form = OrdenCompraForm(initial=initial_data)
        if initial_formset:
            formset = DetalleOrdenFormSet(queryset=DetalleOrden.objects.none(), initial=initial_formset)
            formset.extra = len(initial_formset)
        else:
            formset = DetalleOrdenFormSet(queryset=DetalleOrden.objects.none())

    return render(request, 'compras/orden_compra_form.html', {
        'form': form, 
        'formset': formset,
        'title': 'Registrar OC',
        'categorias': Categoria.objects.all()
    })

@admin_required
@department_required('COMPRAS')
def orden_compra_edit(request, pk):
    orden = get_object_or_404(OrdenCompra, pk=pk)
    
    # Logic for "Anular"
    if request.method == 'POST' and 'anular' in request.POST:
        if orden.estado == 'EN_ESPERA':
            orden.estado = 'RECHAZADO'
            orden.save()
            messages.success(request, 'Orden anulada correctamente.')
        return redirect('compras:orden_compra_detail', pk=orden.pk)

    # Prevent editing if not EN_ESPERA (though user said "no editable" if EN_ESPERA, 
    # but usually you edit DRAFT. If EN_ESPERA is locked, then we shouldn't be here unless it's to view/anular)
    # The requirement says: "en espera solo puede ser anulada, no editable".
    # So we should probably redirect or show error if trying to save changes.
    # But we need this view to handle the POST for "Anular" if we put the button in the form? 
    # Actually, "Anular" is better placed in Detail view.
    # If this view is strictly for editing content, we should block it if EN_ESPERA.
    
    if orden.estado == 'EN_ESPERA':
         messages.warning(request, 'Las órdenes en espera no se pueden editar, solo anular.')
         return redirect('compras:orden_compra_detail', pk=orden.pk)

    if request.method == 'POST':
        form = OrdenCompraForm(request.POST, instance=orden)
        formset = DetalleOrdenFormSet(request.POST, instance=orden)
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    orden = form.save()
                    detalles = formset.save(commit=False)
                    for detalle in detalles:
                        detalle.orden = orden
                        detalle.save()
                    # Handle deletions
                    for obj in formset.deleted_objects:
                        obj.delete()
                        
                    orden.update_totals()
                    
                    messages.success(request, 'Orden de compra actualizada correctamente.')
                    return redirect('compras:orden_compra_list')
            except Exception as e:
                messages.error(request, f'Error al actualizar la orden: {str(e)}')
    else:
        form = OrdenCompraForm(instance=orden)
        formset = DetalleOrdenFormSet(instance=orden)
    
    return render(request, 'compras/orden_compra_form.html', {
        'form': form, 
        'formset': formset, 
        'title': 'Editar OC',
        'orden': orden,
        'categorias': Categoria.objects.all()
    })

@admin_required
def orden_compra_detail(request, pk):
    orden = get_object_or_404(OrdenCompra, pk=pk)
    
    if request.method == 'POST':
        if 'anular' in request.POST:
            if orden.estado == 'EN_ESPERA':
                orden.estado = 'RECHAZADO'
                orden.save()
                
                if request.POST.get('clonar') == 'true':
                    # Clone logic
                    new_orden = OrdenCompra.objects.create(
                        solicitante=request.user,
                        estado='EN_ESPERA'
                    )
                    for detalle in orden.detalles.all():
                        detalle.pk = None
                        detalle.orden = new_orden
                        detalle.save()
                    new_orden.update_totals()
                    messages.success(request, 'Orden anulada y clonada exitosamente.')
                    return redirect('compras:orden_compra_edit', pk=new_orden.pk)
                
                messages.success(request, 'Orden anulada correctamente.')
                return redirect('compras:orden_compra_detail', pk=orden.pk)

    # Determine permissions
    dept = None
    if hasattr(request.user, 'profile'):
        dept = request.user.profile.department
    
    is_admin = request.user.is_superuser or request.user.is_staff or getattr(request.user, 'empleado', None) and request.user.empleado.rol in ['administrador', 'jefe_compras']
    is_compras = dept == 'COMPRAS' or is_admin
    is_finanzas = dept == 'FINANZAS' or is_admin
    is_bodega = dept == 'BODEGA' or is_admin
    
    perms = {
        'can_create_oc': is_compras,
        'can_edit_oc': is_compras,
        'can_anular_oc': is_compras,
        'can_approve_oc': is_finanzas,
        'can_reject_oc': is_finanzas,
        'can_close_oc': is_bodega,
    }

    return render(request, 'compras/orden_compra_detail.html', {'orden': orden, 'perms': perms})

@admin_required
@department_required('COMPRAS')
def orden_compra_anular(request, pk):
    """
    Vista especifica para anular desde el listado.
    """
    orden = get_object_or_404(OrdenCompra, pk=pk)
    if request.method == 'POST':
        if orden.estado == 'EN_ESPERA':
            try:
                with transaction.atomic():
                    motivo = request.POST.get('motivo_anulacion', '')
                    
                    orden.estado = 'RECHAZADO'
                    orden.motivo_anulacion = motivo
                    orden.usuario_anulo = request.user
                    orden.fecha_anulacion = timezone.now()
                    orden.save()
                    
                    if request.POST.get('clonar') == 'true':
                        new_orden = OrdenCompra.objects.create(
                            solicitante=request.user,
                            estado='EN_ESPERA'
                        )
                        for detalle in orden.detalles.all():
                            detalle.pk = None
                            detalle.orden = new_orden
                            detalle.save()
                        new_orden.update_totals()
                        messages.success(request, 'Orden anulada y clonada exitosamente.')
                        return redirect('compras:orden_compra_edit', pk=new_orden.pk)
                    
                    messages.success(request, 'Orden anulada correctamente.')
            except Exception as e:
                messages.error(request, f'Error al anular la orden: {str(e)}')
    return redirect('compras:orden_compra_list')

@admin_required
def historial_anulaciones(request):
    """
    Muestra el historial de órdenes anuladas con estadísticas por usuario.
    """
    query = request.GET.get('q', '')
    ordenes_anuladas = OrdenCompra.objects.filter(estado='RECHAZADO').order_by('-fecha_anulacion')
    
    if query:
        ordenes_anuladas = ordenes_anuladas.filter(
            Q(id__icontains=query) |
            Q(solicitante__username__icontains=query) |
            Q(usuario_anulo__username__icontains=query)
        )
    
    # Calcular estadísticas por usuario
    from django.contrib.auth.models import User
    users_stats = []
    users = User.objects.filter(ordenes_solicitadas__isnull=False).distinct()
    
    for user in users:
        total = OrdenCompra.objects.filter(solicitante=user).count()
        anuladas = OrdenCompra.objects.filter(solicitante=user, estado='RECHAZADO').count()
        porcentaje = round((anuladas / total * 100), 1) if total > 0 else 0
        
        if anuladas > 0:
            users_stats.append({
                'user': user,
                'total': total,
                'anuladas': anuladas,
                'porcentaje': porcentaje
            })
    
    users_stats = sorted(users_stats, key=lambda x: x['porcentaje'], reverse=True)
    
    paginator = Paginator(ordenes_anuladas, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'ordenes': page_obj,
        'query': query,
        'users_stats': users_stats[:5],
    }
    return render(request, 'compras/historial_anulaciones.html', context)

@admin_required
def orden_compra_cerrar(request, pk):
    """
    Cierra una orden APROBADA y crea automáticamente un registro en Compra.
    Solo permitido para BODEGA.
    """
    orden = get_object_or_404(OrdenCompra, pk=pk)
    
    # Verificar permiso de Bodega
    if not request.user.is_superuser:
        try:
            if request.user.profile.department != 'BODEGA':
                messages.error(request, 'Solo el departamento de Bodega puede cerrar órdenes.')
                return redirect('compras:orden_compra_detail', pk=orden.pk)
        except:
             # Si no tiene perfil, asumir que no es bodega (salvo superuser)
             messages.error(request, 'No tiene permisos para cerrar órdenes.')
             return redirect('compras:orden_compra_detail', pk=orden.pk)

    if request.method == 'POST':
        # Validar que la orden esté en estado APROBADO
        if orden.estado != 'APROBADA':
            messages.error(request, 'Solo se pueden cerrar órdenes aprobadas.')
            return redirect('compras:orden_compra_detail', pk=orden.pk)
        
        try:
            with transaction.atomic():
                # Obtener el primer proveedor de los detalles (o el más relevante)
                # Si hay múltiples proveedores, tomamos el primero
                primer_detalle = orden.detalles.first()
                if not primer_detalle:
                    messages.error(request, 'La orden no tiene detalles.')
                    return redirect('compras:orden_compra_detail', pk=orden.pk)
                
                # Crear la Compra
                compra = Compra.objects.create(
                    proveedor=primer_detalle.proveedor,
                    nombre_proveedor=primer_detalle.proveedor.nombre,
                    numero_factura=f"OC-{orden.id}-{timezone.now().strftime('%Y%m%d')}",
                    fecha_compra=timezone.now().date(),
                    monto_total=orden.monto_total,
                    direccion_entrega=primer_detalle.proveedor.direccion,
                    correo_contacto=primer_detalle.proveedor.email,
                    descripcion=f"Compra generada automáticamente desde Orden OC-{orden.id}"
                )
                
                # Cambiar estado de la orden a CERRADA
                orden.estado = 'CERRADA'
                orden.save()
                
                # Notificar a Compras
                from .notifications import notify_compras_status_change
                notify_compras_status_change(orden)
                
                messages.success(request, f'Orden cerrada exitosamente. Se creó la compra con factura {compra.numero_factura}.')
                return redirect('compras:compras_list')
        except Exception as e:
            messages.error(request, f'Error al cerrar la orden: {str(e)}')
            return redirect('compras:orden_compra_detail', pk=orden.pk)
    
    return redirect('compras:orden_compra_detail', pk=orden.pk)

@admin_required
def orden_compra_aprobar(request, pk):
    """
    Aprueba una orden EN_ESPERA.
    Solo permitido para FINANZAS.
    """
    orden = get_object_or_404(OrdenCompra, pk=pk)
    
    # Verificar permiso de Finanzas
    if not request.user.is_superuser:
        try:
            if request.user.profile.department != 'FINANZAS':
                messages.error(request, 'Solo el departamento de Finanzas puede aprobar órdenes.')
                return redirect('compras:orden_compra_detail', pk=orden.pk)
        except:
             messages.error(request, 'No tiene permisos para aprobar órdenes.')
             return redirect('compras:orden_compra_detail', pk=orden.pk)
    
    if request.method == 'POST':
        if orden.estado != 'EN_ESPERA':
            messages.error(request, 'Solo se pueden aprobar órdenes en espera.')
            return redirect('compras:orden_compra_detail', pk=orden.pk)
        
        orden.estado = 'APROBADA'
        orden.save()
        
        # Notificar a Bodega y Compras
        from .notifications import notify_bodega_approved_order, notify_compras_status_change
        notify_bodega_approved_order(orden)
        notify_compras_status_change(orden)
        
        messages.success(request, 'Orden aprobada exitosamente.')
        return redirect('compras:orden_compra_detail', pk=orden.pk)
    
    return redirect('compras:orden_compra_detail', pk=orden.pk)

@admin_required
def orden_compra_rechazar(request, pk):
    """
    Rechaza una orden EN_ESPERA.
    Solo permitido para FINANZAS.
    """
    orden = get_object_or_404(OrdenCompra, pk=pk)
    
    # Verificar permiso de Finanzas
    if not request.user.is_superuser:
        try:
            if request.user.profile.department != 'FINANZAS':
                messages.error(request, 'Solo el departamento de Finanzas puede rechazar órdenes.')
                return redirect('compras:orden_compra_detail', pk=orden.pk)
        except:
             messages.error(request, 'No tiene permisos para rechazar órdenes.')
             return redirect('compras:orden_compra_detail', pk=orden.pk)
    
    if request.method == 'POST':
        if orden.estado != 'EN_ESPERA':
            messages.error(request, 'Solo se pueden rechazar órdenes en espera.')
            return redirect('compras:orden_compra_detail', pk=orden.pk)
        
        orden.estado = 'RECHAZADA'
        orden.save()
        
        # Notificar a Compras
        from .notifications import notify_compras_status_change
        notify_compras_status_change(orden)
        
        messages.success(request, 'Orden rechazada.')
        return redirect('compras:orden_compra_detail', pk=orden.pk)
    
    return redirect('compras:orden_compra_detail', pk=orden.pk)

@admin_required
def proveedor_evaluar(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = EvaluacionProveedorForm(request.POST)
        if form.is_valid():
            evaluacion = form.save(commit=False)
            evaluacion.proveedor = proveedor
            evaluacion.usuario = request.user
            evaluacion.save()
            messages.success(request, 'Evaluación registrada correctamente.')
            return redirect('compras:proveedores_list')
    return redirect('compras:proveedores_list')

@admin_required
def proveedor_historial_evaluaciones(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    evaluaciones = proveedor.evaluaciones.all().order_by('-fecha')
    data = []
    for ev in evaluaciones:
        data.append({
            'usuario': ev.usuario.username if ev.usuario else 'Desconocido',
            'calidad': ev.get_calidad_display(),
            'fecha': ev.fecha.strftime('%d/%m/%Y'),
            'descripcion': ev.descripcion,
        })
    return JsonResponse({'evaluaciones': data, 'proveedor': proveedor.nombre})

@admin_required
def api_get_insumos(request):
    proveedor_id = request.GET.get('proveedor_id')
    categoria_id = request.GET.get('categoria_id')
    
    if not proveedor_id:
        return JsonResponse({'error': 'Proveedor ID requerido'}, status=400)
        
    try:
        proveedor = Proveedor.objects.get(pk=proveedor_id)
        insumos = proveedor.insumos.all()
        
        if categoria_id:
            insumos = insumos.filter(categoria_id=categoria_id)
            
        data = []
        for insumo in insumos:
            data.append({
                'id': insumo.id,
                'nombre': insumo.nombre,
                'unidad_medida': insumo.unidad_medida
            })
            
        return JsonResponse({'insumos': data})
    except Proveedor.DoesNotExist:
        return JsonResponse({'error': 'Proveedor no encontrado'}, status=404)

@admin_required
def api_get_proveedores(request):
    categoria_id = request.GET.get('categoria_id')
    
    if categoria_id:
        # Filter providers who have at least one insumo in this category
        proveedores = Proveedor.objects.filter(insumos__categoria_id=categoria_id).distinct()
    else:
        proveedores = Proveedor.objects.all()
        
    data = [{'id': p.id, 'nombre': p.nombre} for p in proveedores]
    return JsonResponse({'proveedores': data})






# ==================== Notification Views ====================

from django.http import JsonResponse

@login_required
def notifications_list(request):
    """List user notifications"""
    notifications = request.user.notifications.all()[:20]
    return render(request, 'compras/notifications_list.html', {
        'notifications': notifications
    })


@login_required
def notification_mark_read(request, pk):
    """Mark notification as read"""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})


@login_required
def notification_unread_count(request):
    """Get unread notification count"""
    count = request.user.notifications.filter(is_read=False).count()
    return JsonResponse({'count': count})
