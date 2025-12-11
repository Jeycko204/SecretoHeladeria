# Guía de Despliegue en AWS EC2

Esta guía te llevará paso a paso para desplegar tu proyecto Django en una instancia EC2 de AWS.

## 1. Crear Instancia EC2

1.  Entra a la consola de AWS.
2.  Lanza una nueva instancia **Ubuntu Server 22.04 LTS** (o 24.04).
3.  **Tipo de instancia**: `t2.micro` (Capa gratuita) o `t3.small` si necesitas más potencia.
4.  **Key Pair**: Crea uno nuevo (ej: `mi-proyecto.pem`) y **descárgalo**. ¡No lo pierdas!
5.  **Security Group (Firewall)**:
    *   Permitir SSH (Puerto 22) desde tu IP.
    *   Permitir HTTP (Puerto 80) desde Anywhere (0.0.0.0/0).
    *   Permitir TCP Personalizado (Puerto 8080) desde Anywhere (0.0.0.0/0) (Si vas a usar ese puerto).

## 2. Conectarse al Servidor

Abre tu terminal en la carpeta donde tienes el archivo `.pem`.

```bash
chmod 400 mi-proyecto.pem
ssh -i "mi-proyecto.pem" ubuntu@<IP_PUBLICA_DE_TU_INSTANCIA>
```

### Opción: Usando PuTTY (Si estás en Windows o prefieres PuTTY)

Si usas PuTTY, necesitas convertir tu llave `.pem` a `.ppk`.

1.  **Convertir Llave**:
    *   Abre **PuTTYgen**.
    *   Haz clic en **Load** y selecciona tu archivo `.pem` (asegúrate de mostrar "All Files").
    *   Haz clic en **Save private key** y guárdala como `mi-proyecto.ppk`.
2.  **Conectar**:
    *   Abre **PuTTY**.
    *   **Host Name**: `admin@<IP_PUBLICA>` (Si es Debian) o `ubuntu@<IP_PUBLICA>` (Si es Ubuntu).
    *   En el menú izquierdo, ve a **Connection** -> **SSH** -> **Auth** -> **Credentials**.
    *   En "Private key file for authentication", selecciona tu archivo `.ppk`.
    *   Haz clic en **Open**.

## 3. Preparar el Servidor

Una vez conectado, actualiza e instala lo necesario:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx git -y
```

## 4. Clonar/Subir el Proyecto

Opción A: Usar Git (Recomendado)
```bash
git clone <URL_DE_TU_REPO>
cd SecretoHeladeria
```

Opción B: Copiar archivos con SCP (Desde tu compu local)
```bash
# Ejecutar desde tu máquina local, no en el servidor
scp -i "mi-proyecto.pem" -r /ruta/a/tu/proyecto ubuntu@<IP_PUBLICA>:/home/ubuntu/
```

## 5. Configurar Entorno Virtual

```bash
cd ~/SecretoHeladeria  # O la carpeta de tu proyecto
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn  # Necesario para producción
```

## 6. Configurar Variables y Base de Datos

1.  Asegúrate de que `ALLOWED_HOSTS` en `settings.py` incluya la IP pública de tu instancia.
    ```python
    ALLOWED_HOSTS = ['52.55.198.58', 'localhost', '127.0.0.1'] # Reemplaza con TU IP real
    ```
2.  Ejecuta migraciones:
    ```bash
    python manage.py migrate
    python manage.py collectstatic
    ```

## 7. Ejecutar el Servidor

### Opción Rápida (Pruebas / Desarrollo)
Para probar que todo funciona igual que en local (usando puerto 8080):

```bash
python manage.py runserver 0.0.0.0:8080
```
*Nota: Esto no es recomendado para producción real, pero sirve para la entrega si piden puerto 8080.*

### Opción Producción (Gunicorn + Nginx)

1.  **Probar Gunicorn**:
    ```bash
    gunicorn --bind 0.0.0.0:8080 secreto_heladeria.wsgi
    ```
    Si funciona, presiona `Ctrl+C`.

2.  **Crear servicio systemd** (para que corra siempre):
    ```bash
    sudo nano /etc/systemd/system/gunicorn.service
    ```
    Pega esto (ajusta rutas):
    ```ini
    [Unit]
    Description=gunicorn daemon
    After=network.target

    [Service]
    User=ubuntu
    Group=www-data
    WorkingDirectory=/home/ubuntu/SecretoHeladeria
    ExecStart=/home/ubuntu/SecretoHeladeria/venv/bin/gunicorn --access-logfile - --workers 3 --bind 0.0.0.0:8080 secreto_heladeria.wsgi:application

    [Install]
    WantedBy=multi-user.target
    ```

3.  **Iniciar servicio**:
    ```bash
    sudo systemctl start gunicorn
    sudo systemctl enable gunicorn
    ```

¡Listo! Tu API debería estar accesible en `http://<TU_IP>:8080/api/`.

## 8. Verificación y Pruebas

### Opción A: Desde tu Computadora Local (Recomendado)

Como ya configuramos el script `test_api_flow.py` con la IP de tu servidor, puedes ejecutarlo desde tu propia máquina para probar que el servidor responde correctamente a las peticiones externas.

```bash
# En tu terminal local (no en PuTTY)
python test_api_flow.py root root
```

### Opción B: Desde el Servidor (vía PuTTY)

Si quieres probar directamente dentro del servidor para descartar problemas de firewall:

1.  **Prueba básica con cURL**:
    ```bash
    curl http://127.0.0.1:8080/api/
    ```
    Deberías ver una respuesta JSON.

2.  **Probar el script en el servidor**:
    Si subiste el archivo `test_api_flow.py`, puedes editarlo para que apunte a localhost:
    ```bash
    nano test_api_flow.py
    # Cambia BASE_URL a "http://127.0.0.1:8080"
    python3 test_api_flow.py root root
    ```

