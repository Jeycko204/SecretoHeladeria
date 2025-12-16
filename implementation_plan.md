# Verification Plan

I will verify the system functionality by creating a comprehensive test suite and performing manual UI checks.

## User Review Required
> [!NOTE]
> I will be creating a new test file `compras/tests.py` as no project-specific tests were found.

## Proposed Changes

### compras
#### [NEW] [tests.py](file:///home/deck/Documentos/backend/secretohel/SecretoHeladeria-pruebas/compras/tests.py)
- Create a `TestCase` class `SystemVerificationTests`.
- **Test Provider Creation**: Verify `Proveedor` can be created with valid data and fails with invalid RUT.
- **Test Order Workflow**:
    - Create an `OrdenCompra`.
    - Add `DetalleOrden` items.
    - Verify `update_totals` calculates correctly.
    - Test status transitions: `EN_ESPERA` -> `APROBADA`, `EN_ESPERA` -> `RECHAZADA`.
- **Test Permissions**: Verify that only users with correct departments can approve/reject orders (simulated in tests).

## Verification Plan

### Automated Tests
Run the newly created tests:
```bash
python manage.py test compras
```

### Manual Verification
I will use the browser tool to verify the critical "Order Approval" flow:
1.  **Login**: Access `/accounts/login/` with superuser credentials.
2.  **Create Order**: Go to `/ordenes/crear/` and create a new order.
3.  **Approve Order**: Navigate to the order detail and click "Aprobar" (verifying the button exists and works).
4.  **Check Status**: Confirm the status changes to `APROBADA`.
