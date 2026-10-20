# 🚀 Sistema de Gestión de Servicios con Autenticación y Sesiones (Django)

Proyecto desarrollado para la **Unidad 4 · Semana 7 (Pulido Funcional, UX y Simulacro de Defensa)**, basado en la base de la Unidad 3. Permite la gestión segura de servicios profesionales con autenticación de usuarios, aislamiento estricto de datos, búsqueda por título y paginación.

---

## ✨ Características Principales

* 🔐 **Sistema de Autenticación Propio:** Vistas de Registro (`/registro/`), Login (`/login/`) y Logout (`/logout/`) utilizando `django.contrib.auth`.
* 🛡️ **Aislamiento de Datos por Usuario:** Cada usuario registrado gestiona únicamente sus propios servicios (`propietario=request.user`), protegiendo las vistas con el decorador `@login_required`.
* 📋 **CRUD Completo con Búsqueda y Paginación (Semana 7):** Creación, lectura, edición y eliminación de servicios con filtrado por búsqueda (`?q=`) y paginación de 5 elementos por página.
* 🎨 **Diseño Moderno & UX:** Interfaces estilizadas con **Tailwind CSS**, diseño responsive (`overflow-x-auto`), estados vacíos informativos y manejo de mensajes flash (`messages`).
* 🗄️ **Base de Datos Robusta:** Conexión a MySQL (Aiven) mediante `PyMySQL` y variables de entorno (`python-decouple`).

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python 3.12, Django 6.1.1
* **Base de Datos:** MySQL (Aiven Cloud)
* **Frontend:** Tailwind CSS (CDN), HTML5
* **Despliegue & Servidor:** Gunicorn, WhiteNoise (Archivos estáticos)

---

## ⚙️ Instalación y Ejecución Local

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/garciavasquezdsm3/u3s6-garcia-vasquez-oscar.git
   cd u3s6-garcia-vasquez-oscar
   ```

2. **Crear y activar el entorno virtual:**
   ```bash
   python -m venv env
   # En Windows:
   env\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar las variables de entorno:**
   Crea un archivo `.env` en la raíz del proyecto basado en `.env.example`:
   ```env
   SECRET_KEY=tu-clave-secreta
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000
   DB_NAME=defaultdb
   DB_USER=avnadmin
   DB_PASSWORD=tu-password-aiven
   DB_HOST=tu-host-aiven.aivencloud.com
   DB_PORT=28536
   ```

5. **Aplicar migraciones y ejecutar:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
   Abre en tu navegador: `http://127.0.0.1:8000/`

---

## 🚢 Despliegue en Producción (Render)

* **Build Command:**
  ```bash
  pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
  ```
* **Start Command:**
  ```bash
  gunicorn miproyecto.wsgi
  ```

---

## 👨‍💻 Autor

* **Óscar García Vásquez**
* Grupo / DSM3
