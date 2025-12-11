import os
import django
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

# Manual setup of Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secreto_heladeria.settings')
django.setup()

from compras.forms import ProveedorForm
from compras.models import Categoria

def run_verification():
    print("--- Verifying ProveedorForm Validations ---")
    
    # helper to print pass/fail
    def check(condition, msg):
        print(f"[{'PASS' if condition else 'FAIL'}] {msg}")

    # 1. Test empty form - should fail
    form = ProveedorForm(data={})
    check(not form.is_valid(), "Empty form is invalid")
    check('categoria' in form.errors, "Category is required in errors")

    # 2. Test form with data but missing category
    data = {
        'nombre': 'Test Provider',
        'rut': '12345678-5',
        'contacto': 'Juan Perez',
        'telefono': '912345678',
        'email': 'test@example.com',
        'direccion': 'Calle Falsa 123',
        'tiempo_entrega': 5,
        'monto_minimo': 50000,
        'dias_entrega': ['LUN']
    }
    form = ProveedorForm(data=data)
    check(not form.is_valid(), "Form without category is invalid")
    check('categoria' in form.errors, "Category error present: " + str(form.errors.get('categoria', '')))

    # 3. Test form with valid data including category
    # Ensure a category exists
    cat, _ = Categoria.objects.get_or_create(nombre="Test Cat")
    data['categoria'] = cat.id
    form = ProveedorForm(data=data)
    check(form.is_valid(), "Form with all fields is valid")
    
    # 4. Test Certification Optionality
    # Form without file is valid (as per second instruction)
    form = ProveedorForm(data=data)
    check(form.is_valid(), "Form without certification file is valid (Correct)")

    # 5. Test PDF Size Limit (Validation usually happens on file clean, let's mock a file)
    # This is harder to test without a real file upload in request, but we can call the validator directly.
    from compras.validators import validate_pdf_file
    from django.core.exceptions import ValidationError
    
    class MockFile:
        def __init__(self, name, size):
            self.name = name
            self.size = size

    # Small PDF
    try:
        validate_pdf_file(MockFile('test.pdf', 1024))
        check(True, "Small PDF passes validation")
    except ValidationError:
        check(False, "Small PDF failed validation")

    # Large PDF > 5MB
    try:
        validate_pdf_file(MockFile('large.pdf', 6 * 1024 * 1024))
        check(False, "Large PDF should fail validation")
    except ValidationError:
        check(True, "Large PDF failed validation as expected")

    # Non-PDF
    try:
        validate_pdf_file(MockFile('image.jpg', 1024))
        check(False, "Non-PDF should fail validation")
    except ValidationError:
        check(True, "Non-PDF failed validation as expected")

if __name__ == "__main__":
    run_verification()
