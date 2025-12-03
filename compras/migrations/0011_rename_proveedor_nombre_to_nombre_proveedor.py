from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0010_alter_compra_proveedor_nombre'),
    ]

    operations = [
        migrations.RenameField(
            model_name='compra',
            old_name='proveedor_nombre',
            new_name='nombre_proveedor',
        ),
    ]
