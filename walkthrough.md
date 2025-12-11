# Verification Walkthrough

## User Setup
Ran the following command to set up users:
```bash
python3 manage.py setup_users
```
Users created/updated:
- `bodega` (Group: Inventario, Dept: BODEGA)
- `finanzas` (Group: Finanzas, Dept: FINANZAS)
- `compras` (Group: Compras, Dept: COMPRAS)

## Permission Verification

### 1. Edit Button Visibility
| User Role | View | Status |
| :--- | :--- | :--- |
| **Admin** | Order List / Detail | **Visible** |
| **Compras** | Order List / Detail | **Hidden** (Can only Anular/Clonar) |
| **Finanzas** | Order List / Detail | **Hidden** (Can only Approve/Reject) |

### 2. URL Access Control
Tried accessing `/compras/ordenes/<id>/editar/` as non-admin:
- **Result**: Redirected with error message "Solo el administrador puede editar órdenes de compra."

### 3. Anular and Clonar (Status Check)
- **Action**: Compras user clicks "Anular".
- **Result**: Order status updates to **`ANULADA`** (previously `RECHAZADA` was only for Finance).
- **Action**: Compras user clicks "Anular y Clonar".
- **Result**:
    - Original order marked as **`ANULADA`**.
    - User redirected to Create page with pre-filled data.
    - New order saved as `EN_ESPERA`.

### 4. Finance Rejection
- **Action**: Finanzas user clicks "Rechazar".
- **Result**: Order status updates to **`RECHAZADA`**. 
- **Result**: Correctly distinguished from `ANULADA`.
