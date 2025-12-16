# Guía de Migración a Fedora Linux

Esta guía explica cómo configurar el proyecto `SecretoHeladeria` en un computador con Fedora.

## 1. Preparar el Entorno en Fedora

A diferencia de Ubuntu (que usa `apt`), Fedora utiliza `dnf`.

### Instalar Dependencias del Sistema
Abre una terminal en tu Fedora e instala Python, MySQL (MariaDB) y las librerías de desarrollo:

```bash
sudo dnf update
sudo dnf install python3-pip python3-devel mysql-devel mariadb-server gcc git redhat-rpm-config
```

### Iniciar y Configurar Base de Datos
Fedora usa MariaDB como reemplazo directo de MySQL.

1.  **Iniciar el servicio**:
    ```bash
    sudo systemctl start mariadb
    sudo systemctl enable mariadb
    ```

2.  **Configuración inicial (opcional pero recomendado)**:
    ```bash
    sudo mysql_secure_installation
    ```

3.  **Crear Base de Datos y Usuario**:
    Entra a la consola de base de datos:
    ```bash
    sudo mysql -u root -p
    ```
    Ejecuta los comandos SQL (igual que en la guía anterior):
    ```sql
    CREATE DATABASE secreto_heladeria_db CHARACTER SET utf8mb4;
    CREATE USER 'secreto_user'@'localhost' IDENTIFIED BY '2417';
    GRANT ALL PRIVILEGES ON secreto_heladeria_db.* TO 'secreto_user'@'localhost';
    FLUSH PRIVILEGES;
    EXIT;
    ```

## 2. Transferir Archivos

Tienes dos opciones para llevar el proyecto a la nueva PC:

*   **Opción A (Git)**: Si subiste tu código a GitHub/GitLab, simplemente clónalo:
    ```bash
    git clone <tu-url-del-repo>
    cd SecretoHeladeria-pruebas
    ```
*   **Opción B (USB/Red)**: Copia la carpeta del proyecto y el archivo `backup_secreto_heladeria.sql` usando un pendrive o red local.

## 3. Importar Base de Datos

Asumiendo que copiaste el archivo `backup_secreto_heladeria.sql` a la carpeta del proyecto en la nueva PC:

```bash
mysql -u secreto_user -p secreto_heladeria_db < backup_secreto_heladeria.sql
# Ingresa la contraseña: 2417
```

## 4. Configurar Python y Ejecutar

Dentro de la carpeta del proyecto en Fedora:

1.  **Crear entorno virtual**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Instalar dependencias del proyecto**:
    ```bash
    pip install -r requirements.txt
    ```
    *Nota: Si `mysqlclient` falla al instalar, asegúrate de haber instalado `mysql-devel` y `python3-devel` en el paso 1.*

3.  **Ejecutar el servidor**:
    ```bash
    python manage.py runserver
    ```

¡Listo! Tu proyecto debería estar corriendo en `http://127.0.0.1:8000`.
