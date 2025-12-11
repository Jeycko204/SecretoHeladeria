# Guía de Pruebas de API - Secreto Heladería

Esta guía detalla cómo probar la API REST implementada con Django Rest Framework y autenticación JWT.

**URL Base del Servidor**: `http://52.55.198.58:8080/`

## Usuarios de Prueba

| Rol | Usuario | Contraseña | Permisos |
|-----|---------|------------|----------|
| **Jefe Compras** | `jefe_compras` | `Jefe123!` | Crear órdenes, Ver proveedores |
| **Finanzas** | `finanzas` | `Finanzas123!` | Aprobar/Rechazar órdenes |
| **Bodega** | `bodeguero` | `Bodega123!` | Cerrar órdenes |
| **Admin** | `root` | `root` | Acceso total |

## Script de Prueba Automatizado

El script `test_api_flow.py` realiza una prueba completa del flujo principal contra el servidor desplegado.

### Uso

```bash
python test_api_flow.py <usuario> <contraseña>
```

Ejemplo para probar flujo completo (usando admin para simplificar permisos en un solo script):
```bash
python test_api_flow.py root root
```

## Pruebas Manuales con cURL

### 1. Obtener Token (Login)
```bash
curl -X POST http://52.55.198.58:8080/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "jefe_compras", "password": "Jefe123!"}'
```
*Copia el "access" token de la respuesta.*

### 2. Listar Proveedores
```bash
curl -X GET http://52.55.198.58:8080/api/proveedores/ \
     -H "Authorization: Bearer <TU_TOKEN>"
```

### 3. Crear Orden de Compra
```bash
curl -X POST http://52.55.198.58:8080/api/ordenes/ \
     -H "Authorization: Bearer <TU_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{
        "detalles": [
            {
                "proveedor": 1,
                "insumo": "Prueba API Remota",
                "unidad_medida": "UN",
                "cantidad": 5,
                "precio_unitario": 1000
            }
        ]
     }'
```

### 4. Aprobar Orden (Finanzas)
*Requiere token de usuario Finanzas (`finanzas` / `Finanzas123!`)*
```bash
curl -X POST http://52.55.198.58:8080/api/ordenes/<ID_ORDEN>/aprobar/ \
     -H "Authorization: Bearer <TOKEN_FINANZAS>"
```

## Pruebas Manuales en el Navegador (Browsable API)

1.  Ve a [http://52.55.198.58:8080/api/](http://52.55.198.58:8080/api/)
2.  Haz clic en "Log in" (arriba a la derecha) e ingresa con `jefe_compras` / `Jefe123!` (o el usuario que desees probar).
3.  Navega a los endpoints y usa los formularios HTML para interactuar.
