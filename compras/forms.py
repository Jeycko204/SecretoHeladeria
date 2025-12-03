from django import forms
from .models import Proveedor, Categoria, Compra, OrdenCompra, DetalleOrden, EvaluacionProveedor
from .validators import validate_rut
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
import re

class ProveedorForm(forms.ModelForm):
    DIAS_CHOICES = [
        ('LUN', 'Lunes'),
        ('MAR', 'Martes'),
        ('MIE', 'Miércoles'),
        ('JUE', 'Jueves'),
        ('VIE', 'Viernes'),
        ('SAB', 'Sábado'),
        ('DOM', 'Domingo'),
    ]
    dias_entrega = forms.MultipleChoiceField(
        choices=DIAS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Frecuencia de entrega"
    )

    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de empresa', 'required': True}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rut', 'required': True, 'pattern': '[0-9]+-?[0-9kK]'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contacto principal', 'required': True}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefono', 'required': True, 'pattern': '[0-9\s\-\(\)\+]+', 'title': 'Solo números, espacios, guiones y paréntesis'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'required': True}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Direccion de entrega', 'required': True}),
            'tiempo_entrega': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tiempo de entrega', 'required': True, 'min': 1, 'max': 30, 'type': 'number'}),
            'monto_minimo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monto minimo', 'required': True, 'min': 0, 'type': 'number', 'step': '1'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'certificacion': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'insumos': forms.MultipleHiddenInput(),
            'agregar_contacto_secundario': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'contacto_secundario_nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'contacto_secundario_apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'contacto_secundario_rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RUT', 'pattern': '[0-9]+-?[0-9kK]'}),
            'contacto_secundario_telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono', 'pattern': '[0-9\\s\\-\\(\\)\\+]+'}),
            'contacto_secundario_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'contacto_secundario_direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
        }
        error_messages = {
            'nombre': {
                'required': 'El campo nombre es obligatorio',
            },
            'rut': {
                'required': 'El campo RUT es obligatorio',
            },
            'contacto': {
                'required': 'El campo contacto es obligatorio',
            },
            'telefono': {
                'required': 'El campo teléfono es obligatorio',
            },
            'email': {
                'required': 'El campo email es obligatorio',
                'invalid': 'Ingrese un email válido',
            },
            'direccion': {
                'required': 'El campo dirección es obligatorio',
            },
            'tiempo_entrega': {
                'required': 'El campo tiempo de entrega es obligatorio',
            },
            'monto_minimo': {
                'required': 'El campo monto mínimo es obligatorio',
            },
            'categoria': {
                'required': 'El campo categoría es obligatorio',
            },
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        
        if not rut:
            raise ValidationError('El campo RUT es obligatorio')

        # Limpiar formato: eliminar puntos y espacios, dejar guión
        rut_clean = rut.replace('.', '').replace(' ', '').strip()
        
        # Validar usando el validador robusto
        try:
            validate_rut(rut_clean)
        except ValidationError as e:
            raise ValidationError(e.message)
        
        return rut_clean
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        errors = []
        
        if not telefono:
            errors.append('El campo teléfono es obligatorio')
        else:
            # Remove spaces, dashes, parentheses
            telefono_clean = telefono.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '')
            
            # Validate that it contains only numbers
            if not telefono_clean.isdigit():
                errors.append('Ingrese un teléfono válido. Solo números (ej: 912345678 o +56912345678)')
            elif len(telefono_clean) < 8 or len(telefono_clean) > 15:
                errors.append('El teléfono debe tener entre 8 y 15 dígitos')
        
        if errors:
            raise ValidationError(errors)
        
        return telefono
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre:
            raise ValidationError('El campo nombre es obligatorio')
        
        # Check if nombre contains numbers
        if re.search(r'\d', nombre):
            raise ValidationError('El campo nombre no debe contener números')
        
        # Check minimum length
        if len(nombre.strip()) < 3:
            raise ValidationError('El nombre debe tener al menos 3 caracteres')
        
        return nombre.strip()
    
    def clean_contacto(self):
        contacto = self.cleaned_data.get('contacto')
        if not contacto:
            raise ValidationError('El campo contacto es obligatorio')
        
        # Check if contacto contains numbers (should be a person's name)
        if re.search(r'\d', contacto):
            raise ValidationError('El nombre del contacto no debe contener números')
        
        # Check minimum length
        if len(contacto.strip()) < 3:
            raise ValidationError('El nombre del contacto debe tener al menos 3 caracteres')
        
        return contacto.strip()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('El campo email es obligatorio')
        
        # Basic email format validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError('Ingrese un email válido (ej: contacto@empresa.cl)')
        
        return email.lower().strip()
    
    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')
        if not direccion:
            raise ValidationError('El campo dirección es obligatorio')
        
        # Check minimum length
        if len(direccion.strip()) < 5:
            raise ValidationError('La dirección debe tener al menos 5 caracteres')
        
        return direccion.strip()
    
    def clean_tiempo_entrega(self):
        tiempo = self.cleaned_data.get('tiempo_entrega')
        if tiempo is None:
            raise ValidationError('El campo tiempo de entrega es obligatorio')
        
        # Validate range
        if tiempo < 1:
            raise ValidationError('El tiempo de entrega debe ser al menos 1 día')
        
        if tiempo > 30:
            raise ValidationError('El tiempo de entrega no puede superar los 30 días')
        
        return tiempo
    
    def clean_monto_minimo(self):
        monto = self.cleaned_data.get('monto_minimo')
        if monto is None:
            raise ValidationError('El campo monto mínimo es obligatorio')
        
        # Validate that it's not negative
        if monto < 0:
            raise ValidationError('El monto mínimo no puede ser negativo')
        
        # Validate reasonable range
        if monto > 10000000:  # 10 million
            raise ValidationError('El monto mínimo parece demasiado alto. Verifique el valor ingresado')
        
        return monto
    
    def clean_categoria(self):
        categoria = self.cleaned_data.get('categoria')
        if not categoria:
            raise ValidationError('Debe seleccionar una categoría')
        
        return categoria

    def clean_dias_entrega(self):
        dias = self.cleaned_data.get('dias_entrega')
        if not dias:
            raise ValidationError('Debe seleccionar al menos un día de entrega')
        if dias:
            return ",".join(dias)
        return ""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.dias_entrega:
            self.initial['dias_entrega'] = self.instance.dias_entrega.split(',')

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'nombre': {
                'required': 'El campo nombre es obligatorio',
            },
        }
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre:
            raise ValidationError('El campo nombre es obligatorio')
        
        # Check if nombre contains numbers
        if re.search(r'\d', nombre):
            raise ValidationError('El campo nombre no debe contener números')
        
        return nombre

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['proveedor', 'numero_factura', 'fecha_compra', 'monto_total', 'descripcion']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'numero_factura': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_compra': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_fecha_compra(self):
        """Validación: la fecha de compra debe ser exactamente la fecha actual."""
        fecha = self.cleaned_data.get('fecha_compra')
        from datetime import date
        if fecha and fecha != date.today():
            raise forms.ValidationError('La fecha de la compra debe ser la fecha actual.')
        return fecha

from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class UserAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if user.is_staff or user.is_superuser:
            raise ValidationError(
                _("This login form is for regular users only. Admins should use the admin login page."),
                code='admin_login_not_allowed',
            )

class AdminAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_staff:
            raise ValidationError(
                _("This login form is for admin users only."),
                code='non_admin_login_not_allowed',
            )


class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = [] # No fields to edit directly on creation, maybe just hidden ones?
        # Actually, if we remove 'proveedor', the form might be empty if we don't have other fields.
        # But we need the form to save the instance.
        
class DetalleOrdenForm(forms.ModelForm):
    class Meta:
        model = DetalleOrden
        fields = ['proveedor', 'insumo', 'insumo_fk', 'unidad_medida', 'cantidad', 'precio_unitario']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control', 'required': True, 'onchange': 'loadInsumos(this)'}),
            'insumo': forms.HiddenInput(),
            'insumo_fk': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'unidad_medida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unidad de medida', 'required': True, 'readonly': True}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': True, 'min': 0.01, 'type': 'number'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'required': True, 'min': 1, 'type': 'number'}),
        }
        error_messages = {
            'proveedor': {
                'required': 'Debe seleccionar un proveedor',
            },
            'insumo': {
                'required': 'El campo insumo es obligatorio',
            },
            'unidad_medida': {
                'required': 'El campo unidad de medida es obligatorio',
            },
            'cantidad': {
                'required': 'El campo cantidad es obligatorio',
            },
            'precio_unitario': {
                'required': 'El campo precio unitario es obligatorio',
            },
        }
    
    def clean_insumo(self):
        # This field is now populated automatically or hidden, but we still want to save it.
        # If it's empty, we can populate it from insumo_fk name if available.
        insumo = self.cleaned_data.get('insumo')
        insumo_fk = self.cleaned_data.get('insumo_fk')
        
        if not insumo and insumo_fk:
            return insumo_fk.nombre
            
        return insumo
    
    def clean_unidad_medida(self):
        unidad = self.cleaned_data.get('unidad_medida')
        errors = []
        
        if not unidad:
            errors.append('El campo unidad de medida es obligatorio')
        else:
            if len(unidad.strip()) < 1:
                errors.append('La unidad de medida debe tener al menos 1 caracter')
        
        if errors:
            raise ValidationError(errors)
        
        return unidad.strip() if unidad else unidad
    
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        errors = []
        
        if cantidad is None:
            errors.append('El campo cantidad es obligatorio')
        else:
            if cantidad < 1:
                errors.append('La cantidad debe ser mínimo 1')
            if cantidad > 100000:
                errors.append('La cantidad parece demasiado alta')
        
        if errors:
            raise ValidationError(errors)
        
        return cantidad
    
    def clean_precio_unitario(self):
        precio = self.cleaned_data.get('precio_unitario')
        errors = []
        
        if precio is None:
            errors.append('El campo precio unitario es obligatorio')
        else:
            if precio < 1:
                errors.append('El precio unitario debe ser mínimo 1')
            if precio > 10000000:
                errors.append('El precio parece demasiado alto')
        
        if errors:
            raise ValidationError(errors)
        
        return precio

DetalleOrdenFormSet = inlineformset_factory(
    OrdenCompra, DetalleOrden, form=DetalleOrdenForm,
    extra=1, can_delete=True
)

class EvaluacionProveedorForm(forms.ModelForm):
    class Meta:
        model = EvaluacionProveedor
        fields = ['calidad', 'descripcion']
        widgets = {
            'calidad': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Breve descripcion...'}),
        }
