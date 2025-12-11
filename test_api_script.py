import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000/api"

def log(msg):
    with open("api_test_results.txt", "a") as f:
        f.write(msg + "\n")
    print(msg)

def get_token(username, password):
    url = f"{BASE_URL}/token/"
    try:
        response = requests.post(url, data={'username': username, 'password': password})
        if response.status_code == 200:
            return response.json()['access']
        else:
            log(f"Login failed for {username}: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        log("Error: Could not connect to server. Is it running on port 8000?")
        sys.exit(1)

def test_workflow():
    # Clear file
    open("api_test_results.txt", "w").close()
    
    log("--- 1. Login as Jefe Compras ---")
    token_compras = get_token("jefe_compras", "password123")
    if not token_compras: return

    headers = {'Authorization': f'Bearer {token_compras}'}

    log("\n--- 2. List Providers ---")
    resp = requests.get(f"{BASE_URL}/proveedores/", headers=headers)
    if resp.status_code == 200:
        proveedores = resp.json()
        log(f"Found {len(proveedores)} providers")
        if proveedores:
            first_provider_id = proveedores[0]['id']
            log(f"Using Provider ID: {first_provider_id}")
        else:
            log("No providers found to test creation.")
            return
    else:
        log(f"Failed to list providers: {resp.text}")
        return

    log("\n--- 3. Create Order (Jefe Compras) ---")
    order_data = {
        "detalles": [
            {
                "proveedor": first_provider_id,
                "insumo": "Insumo Test API",
                "unidad_medida": "UN",
                "cantidad": 10,
                "precio_unitario": 500
            }
        ]
    }
    resp = requests.post(f"{BASE_URL}/ordenes/", json=order_data, headers=headers)
    if resp.status_code == 201:
        order = resp.json()
        order_id = order['id']
        log(f"Order Created! ID: {order_id}, State: {order['estado']}")
    else:
        log(f"Failed to create order: {resp.text}")
        return

    log("\n--- 4. Login as Finanzas ---")
    token_finanzas = get_token("analista_finanzas", "password123")
    headers_fin = {'Authorization': f'Bearer {token_finanzas}'}
    
    log(f"\n--- 5. Approve Order {order_id} (Finanzas) ---")
    resp = requests.post(f"{BASE_URL}/ordenes/{order_id}/aprobar/", headers=headers_fin)
    if resp.status_code == 200:
        log("Order Approved successfully!")
    else:
        log(f"Failed to approve: {resp.text}")

    log("\n--- 6. Login as Bodega ---")
    token_bodega = get_token("bodeguero", "password123")
    headers_bod = {'Authorization': f'Bearer {token_bodega}'}

    log(f"\n--- 7. Close Order {order_id} (Bodega) ---")
    resp = requests.post(f"{BASE_URL}/ordenes/{order_id}/cerrar/", headers=headers_bod)
    if resp.status_code == 200:
        log("Order Closed successfully!")
    else:
        log(f"Failed to close: {resp.text}")

if __name__ == "__main__":
    test_workflow()
