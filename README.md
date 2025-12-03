# Secreto Heladería - Sistema de Compras

Sistema de gestión de compras para heladería desarrollado con Django.

## Requisitos

- Python 3.8+
- Django 5.2.7
- SQLite3

## Instalación en otro PC

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Jeycko204/SecretoHeladeria.git
   cd SecretoHeladeria
   ```

2. **Crear y activar entorno virtual:**
   ```bash
   python -m venv venv
   
   # En Linux/Mac:
   source venv/bin/activate
   
   # En Windows:
   venv\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Usar la base de datos incluida:**
   
   La base de datos `db.sqlite3` ya está incluida en el repositorio con datos de prueba.
   No necesitas ejecutar migraciones - simplemente ejecuta:
   
   ```bash
   python manage.py runserver
   ```

5. **Acceder al sistema:**
   - URL: `http://127.0.0.1:8000`
   - Usuario admin ya configurado en la BD (credenciales según tu configuración)

## Estructura del Proyecto

```
SecretoHeladeria/
├── compras/              # Aplicación principal de compras
│   ├── models.py        # Modelos: Categoria, Insumo, Proveedor, OrdenCompra
│   ├── views.py         # Vistas y lógica de negocio
│   ├── forms.py         # Formularios Django
│   └── templates/       # Plantillas HTML
├── static/              # Archivos estáticos (CSS, JS)
├── templates/           # Plantillas base y autenticación
├── media/               # Archivos subidos por usuarios
└── db.sqlite3          # Base de datos con datos de prueba
```

## Funcionalidades

- Gestión de categorías de insumos
- Gestión de insumos con unidades de medida
- Gestión de proveedores con insumos asociados
- Creación de órdenes de compra
- Sistema de autenticación

## Notas

- La base de datos incluida tiene datos de prueba para facilitar el testing
- Los archivos de debug y logs están excluidos del repositorio
- El entorno virtual (`venv/`) no se incluye - debe crearse localmente
