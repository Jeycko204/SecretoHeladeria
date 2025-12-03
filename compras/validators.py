import re
from django.core.exceptions import ValidationError

def validate_rut(value):
    """
    Validador para RUT chileno con verificación de dígito verificador (Módulo 11).
    - Formato: números, guión, dígito verificador (0-9 o K).
    - Ejemplo: 12345678-9
    """
    if not re.match(r'^[0-9]+-[0-9kK]$', value):
        raise ValidationError('El RUT debe tener el formato 12345678-9 (sin puntos, con guión).')

    rut_body, dv = value.split('-')
    
    # Validar cuerpo numérico
    if not rut_body.isdigit():
        raise ValidationError('El cuerpo del RUT debe ser numérico.')
        
    # Algoritmo Módulo 11
    suma = 0
    multiplicador = 2
    
    for c in reversed(rut_body):
        suma += int(c) * multiplicador
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2
            
    resto = suma % 11
    dv_calculado = 11 - resto
    
    if dv_calculado == 11:
        dv_esperado = '0'
    elif dv_calculado == 10:
        dv_esperado = 'K'
    else:
        dv_esperado = str(dv_calculado)
        
    if dv.upper() != dv_esperado:
        raise ValidationError('El RUT no es válido (dígito verificador incorrecto).')

def validate_email_format(value):
    """
    Validador para formato de email específico.
    - Mínimo 3 caracteres antes del @.
    - Mínimo 3 caracteres después del @.
    - Debe contener un punto después del @.
    """
    if not re.match(r'^[a-zA-Z0-9._%+-]{3,}@[a-zA-Z0-9.-]{3,}\.[a-zA-Z]{2,}$', value):
        raise ValidationError('El formato del email no es válido. Asegúrate de que tenga al menos 3 caracteres antes y después del @, y un dominio válido.')

def validate_pdf_file(value):
    """
    Validador para asegurar que el archivo cargado sea un PDF.
    """
    if value:
        if not value.name.endswith('.pdf'):
            raise ValidationError('El archivo de certificación debe estar en formato PDF.')
        # Opcional: Limitar el tamaño del archivo (ej: 5MB)
        # limit = 5 * 1024 * 1024
        # if value.size > limit:
        #     raise ValidationError('El archivo es demasiado grande. El tamaño máximo es 5MB.')

def validate_phone(value):
    """
    Validador para teléfono.
    - Solo debe contener números, espacios, guiones y paréntesis.
    """
    if not re.match(r'^[0-9\s\-\(\)\+]+$', value):
        raise ValidationError('El teléfono solo debe contener números, espacios, guiones o paréntesis.')