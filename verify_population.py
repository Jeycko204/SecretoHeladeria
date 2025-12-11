import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secreto_heladeria.settings')
django.setup()

from django.contrib.auth.models import User
from compras.models import Proveedor, OrdenCompra, Compra, Categoria

def verify():
    with open('verification_output.txt', 'w') as f:
        f.write("--- Verification Results ---\n")
        f.write(f"Users: {User.objects.count()}\n")
        f.write(f"Usernames: {list(User.objects.values_list('username', flat=True))}\n")
        
        f.write(f"Categories: {Categoria.objects.count()}\n")
        f.write(f"Categories: {list(Categoria.objects.values_list('nombre', flat=True))}\n")
        
        f.write(f"Proveedores: {Proveedor.objects.count()}\n")
        
        f.write(f"Ordenes de Compra: {OrdenCompra.objects.count()}\n")
        for oc in OrdenCompra.objects.all():
            f.write(f" - OC {oc.id}: {oc.estado} (Total: {oc.monto_total})\n")
            
        f.write(f"Compras: {Compra.objects.count()}\n")
    print("Verification done.")

if __name__ == "__main__":
    verify()
