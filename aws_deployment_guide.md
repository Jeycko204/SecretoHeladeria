# Guía de Despliegue en AWS y Migración de Base de Datos

Esta guía detalla los pasos para llevar tu aplicación `SecretoHeladeria` a una instancia AWS EC2 y cómo mover tus datos locales.

## 1. Exportar Base de Datos Local
Para exportar tu base de datos actual (MySQL) a un archivo SQL que puedas importar en el servidor:

```bash
mysqldump -u secreto_user -p secreto_heladeria_db > backup_secreto_heladeria.sql
# Te pedirá la contraseña (2417)
```
*Nota: He intentado ejecutar este comando automáticamente por ti.*

## 2. Configuración de AWS (EC2)

1.  **Lanzar Instancia**:
    *   Ve a la consola de AWS EC2.
    *   Lanza una nueva instancia "Ubuntu Server 22.04 LTS" (t2.micro es suficiente para pruebas/capa gratuita).
    *   Crea y descarga tu par de claves (`.pem`).

2.  **Configurar Seguridad (Security Group)**:
    *   Asegúrate de permitir tráfico entrante en:
        *   SSH (Puerto 22) - Tu IP
        *   HTTP (Puerto 80) - 0.0.0.0/0
        *   Django Dev (Puerto 8000) - 0.0.0.0/0 (Solo para pruebas rápidas, no recomendado prod)

## 3. Preparar el Servidor

Conéctate a tu instancia:
```bash
ssh -i "tu-clave.pem" ubuntu@tu-ip-publica-aws
```

Instala las dependencias necesarias:
```bash
sudo apt update
sudo apt install python3-pip python3-dev libmysqlclient-dev mysql-server nginx git
```

## 4. Configurar Base de Datos en AWS

1.  **Entrar a MySQL**: `sudo mysql`
2.  **Crear Base de Datos y Usuario**:
    ```sql
    CREATE DATABASE secreto_heladeria_db CHARACTER SET utf8mb4;
    CREATE USER 'secreto_user'@'localhost' IDENTIFIED BY '2417';
    GRANT ALL PRIVILEGES ON secreto_heladeria_db.* TO 'secreto_user'@'localhost';
    FLUSH PRIVILEGES;
    EXIT;
    ```

## 5. Subir Código y Datos

Desde tu máquina local:
1.  **Subir código**: Puedes usar git (recomendado) o SCP.
    *   *Git*: `git clone tu-repo-url` en el servidor.
    *   *SCP*: `scp -i clave.pem -r /ruta/a/proyecto ubuntu@ip:/home/ubuntu/`
2.  **Subir respaldo de BD**:
    ```bash
    scp -i clave.pem backup_secreto_heladeria.sql ubuntu@ip:/home/ubuntu/
    ```

## 6. Importar Datos y Ejecutar

En el servidor:
1.  **Importar BD**:
    ```bash
    mysql -u secreto_user -p secreto_heladeria_db < backup_secreto_heladeria.sql
    ```
2.  **Configurar Entorno**:
    ```bash
    cd SecretoHeladeria-pruebas
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install gunicorn mysqlclient
    ```
3.  **Ajustar Settings**:
    *   Edita `secreto_heladeria/settings.py` (o usa variables de entorno).
    *   Añade la IP pública de AWS a `ALLOWED_HOSTS`.
    *   Asegúrate de que la config de BD apunte a localhost (ya debería estar así).

4.  **Ejecutar**:
    ```bash
    python manage.py runserver 0.0.0.0:8000
    # O para producción:
    # gunicorn --bind 0.0.0.0:8000 secreto_heladeria.wsgi
    ```

Ahora deberías poder acceder a `http://tu-ip-aws:8000`.
