# API Testing Guide

This guide explains how to interact with the Secreto Heladería API using authentication tokens.

## base URL
All API endpoints are prefixed with `/api/`.
Local URL: `http://127.0.0.1:8000/api/`

## Authentication

The API uses **JWT (JSON Web Tokens)**. You must obtain an access token and include it in the header of your requests.

### 1. Obtain Token

**Endpoint:** `POST /api/token/`

**Request Body:**
```json
{
    "username": "jefe_compras",
    "password": "password123"
}
```

**Response:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 2. Use Token

Include the **access** token in the `Authorization` header:

`Authorization: Bearer <your_access_token>`

## Common Endpoints

| Resource | Method | Endpoint | Description |
|----------|--------|----------|-------------|
| **Proveedores** | GET | `/api/proveedores/` | List all providers |
| | POST | `/api/proveedores/` | Create a provider |
| **Ordenes** | GET | `/api/ordenes/` | List purchase orders |
| | POST | `/api/ordenes/` | Create a new order |
| **Orden Actions** | POST | `/api/ordenes/<id>/aprobar/` | Approve order (Finanzas only) |
| | POST | `/api/ordenes/<id>/rechazar/` | Reject order (Finanzas only) |
| | POST | `/api/ordenes/<id>/cerrar/` | Close order (Bodega only) |

## Example: Create Order (cURL)

```bash
# 1. Get Token
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"jefe_compras","password":"password123"}' | jq -r .access)

# 2. Create Order
curl -X POST http://127.0.0.1:8000/api/ordenes/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "detalles": [
      {
        "proveedor": 1,
        "insumo": "Leche",
        "unidad_medida": "Lt",
        "cantidad": 100,
        "precio_unitario": 900
      }
    ]
  }'
```
