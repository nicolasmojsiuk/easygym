# 🏋️ EasyGym

Sistema de gestión integral para gimnasios desarrollado con Django. Permite administrar socios, membresías, suscripciones y finanzas, con envío automático de comprobantes de pago por correo electrónico.

---

## ✨ Funcionalidades

- **Gestión de socios** — alta, baja y modificación de datos de cada socio
- **Membresías y suscripciones** — creación y seguimiento de planes y vencimientos
- **Finanzas** — registro de pagos e historial de movimientos
- **Comprobantes por email** — envío automático del comprobante de pago al socio una vez registrado el cobro (requiere configurar credenciales de correo en `settings.py`)

---

## 🛠️ Tecnologías utilizadas

| Capa | Tecnología |
|---|---|
| Backend | Python 3 / Django |
| Base de datos | PostgreSQL |
| Frontend | HTML, CSS, JavaScript |
| Correo | Django Email (SMTP) |

---

## ⚙️ Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/easygym.git
cd easygym
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos

Asegurate de tener PostgreSQL instalado y creá una base de datos para el proyecto. Luego editá `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'easygym_db',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Configurar el envío de correos *(opcional)*

Para habilitar el envío automático de comprobantes de pago, completá las siguientes variables en `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'        # O el servidor SMTP que uses
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu_correo@gmail.com'
EMAIL_HOST_PASSWORD = 'tu_contraseña_de_aplicacion'
DEFAULT_FROM_EMAIL = 'EasyGym <tu_correo@gmail.com>'
```

> **Nota:** Si usás Gmail, necesitás generar una [contraseña de aplicación](https://myaccount.google.com/apppasswords) en tu cuenta de Google. Si estas credenciales no se completan, el sistema funciona con normalidad pero no enviará correos.

### 6. Aplicar migraciones

```bash
python manage.py migrate
```

### 7. Crear superusuario

```bash
python manage.py createsuperuser
```

### 8. Correr el servidor

```bash
python manage.py runserver
```

Accedé desde el navegador en [http://localhost:8000](http://localhost:8000)

---

## 🔐 Variables de entorno recomendadas

Para mayor seguridad, se recomienda mover los datos sensibles a un archivo `.env` usando [`python-decouple`](https://pypi.org/project/python-decouple/):

```
SECRET_KEY=tu_clave_secreta
DEBUG=True
DB_NAME=easygym_db
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicacion
```

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT. Podés usarlo, modificarlo y distribuirlo libremente.

---

## 👤 Autor

Desarrollado por **[Tu Nombre](https://github.com/nicolasmojsiuk)**
