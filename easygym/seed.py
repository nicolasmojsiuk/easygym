import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easygym.settings')
django.setup()

from datetime import date, timedelta
from decimal import Decimal
from socios.models import Socios, Membresias, Suscripciones, FormaPago, Pagos

efectivo = FormaPago.objects.get(id=2)
mercadopago = FormaPago.objects.get(id=1)

# MEMBRESIAS
mensual = Membresias.objects.create(nombre='Mensual', precio=26000, duracion_dias=30)
trimestral = Membresias.objects.create(nombre='Trimestral', precio=70000, duracion_dias=90)
anual = Membresias.objects.create(nombre='Anual', precio=250000, duracion_dias=365)

# SOCIOS
socios_data = [
    ('Lucas Fernández', '32145678', 'lucas.fernandez@gmail.com', '1145678901'),
    ('Valentina Gómez', '28976543', 'valen.gomez@gmail.com', '1167890123'),
    ('Matías Rodríguez', '35421876', 'matias.rod@hotmail.com', '1123456789'),
    ('Camila Torres', '30654321', 'cami.torres@gmail.com', '1198765432'),
    ('Nicolás Pérez', '27891234', 'nico.perez@gmail.com', '1134567890'),
    ('Sofía Martínez', '33567890', 'sofi.martinez@gmail.com', '1156789012'),
    ('Agustín López', '29345678', 'agus.lopez@hotmail.com', '1178901234'),
    ('Florencia Díaz', '36123456', 'flor.diaz@gmail.com', '1190123456'),
    ('Tomás Sánchez', '31789012', 'tomas.sanchez@gmail.com', '1112345678'),
    ('Lucía Romero', '34567890', 'lucia.romero@gmail.com', '1145678902'),
]

socios = []
for nombre, dni, email, wp in socios_data:
    s = Socios.objects.create(nombre=nombre, dni=dni, email=email, whatsapp=wp)
    socios.append(s)

# SUSCRIPCIONES Y PAGOS en los últimos 6 meses
hoy = date.today()

pagos_data = [
    # (socio_idx, membresia, fecha_inicio, forma_pago, referencia)
    (0, mensual,    hoy - timedelta(days=150), mercadopago, 'MP-001'),
    (0, mensual,    hoy - timedelta(days=120), mercadopago, 'MP-002'),
    (0, mensual,    hoy - timedelta(days=90),  mercadopago, 'MP-003'),
    (0, mensual,    hoy - timedelta(days=60),  mercadopago, 'MP-004'),
    (0, mensual,    hoy - timedelta(days=30),  mercadopago, 'MP-005'),
    (0, mensual,    hoy - timedelta(days=5),   mercadopago, 'MP-006'),

    (1, mensual,    hoy - timedelta(days=140), efectivo, None),
    (1, mensual,    hoy - timedelta(days=110), efectivo, None),
    (1, mensual,    hoy - timedelta(days=80),  efectivo, None),
    (1, mensual,    hoy - timedelta(days=50),  efectivo, None),
    (1, mensual,    hoy - timedelta(days=20),  efectivo, None),

    (2, trimestral, hoy - timedelta(days=160), mercadopago, 'MP-010'),
    (2, trimestral, hoy - timedelta(days=70),  mercadopago, 'MP-011'),
    (2, trimestral, hoy - timedelta(days=10),  mercadopago, 'MP-012'),

    (3, mensual,    hoy - timedelta(days=130), efectivo, None),
    (3, mensual,    hoy - timedelta(days=100), efectivo, None),
    (3, mensual,    hoy - timedelta(days=70),  efectivo, None),
    (3, mensual,    hoy - timedelta(days=40),  efectivo, None),
    (3, mensual,    hoy - timedelta(days=10),  efectivo, None),

    (4, anual,      hoy - timedelta(days=170), mercadopago, 'MP-020'),

    (5, mensual,    hoy - timedelta(days=120), efectivo, None),
    (5, mensual,    hoy - timedelta(days=90),  efectivo, None),
    (5, mensual,    hoy - timedelta(days=60),  mercadopago, 'MP-021'),
    (5, mensual,    hoy - timedelta(days=30),  mercadopago, 'MP-022'),
    (5, mensual,    hoy - timedelta(days=3),   mercadopago, 'MP-023'),

    (6, trimestral, hoy - timedelta(days=155), efectivo, None),
    (6, trimestral, hoy - timedelta(days=65),  efectivo, None),

    (7, mensual,    hoy - timedelta(days=100), mercadopago, 'MP-030'),
    (7, mensual,    hoy - timedelta(days=70),  mercadopago, 'MP-031'),
    (7, mensual,    hoy - timedelta(days=40),  mercadopago, 'MP-032'),
    (7, mensual,    hoy - timedelta(days=10),  mercadopago, 'MP-033'),

    (8, mensual,    hoy - timedelta(days=90),  efectivo, None),
    (8, mensual,    hoy - timedelta(days=60),  efectivo, None),
    (8, mensual,    hoy - timedelta(days=30),  efectivo, None),
    (8, mensual,    hoy - timedelta(days=2),   efectivo, None),

    (9, trimestral, hoy - timedelta(days=80),  mercadopago, 'MP-040'),
    (9, trimestral, hoy - timedelta(days=10),  mercadopago, 'MP-041'),
]

for socio_idx, membresia, fecha_inicio, forma_pago, referencia in pagos_data:
    socio = socios[socio_idx]

    sus = Suscripciones.objects.create(
        socio=socio,
        membresia=membresia,
        fecha_inicio=fecha_inicio,
        monto=membresia.precio,
        pagado=True,
    )

    Pagos.objects.create(
        suscripcion=sus,
        forma_pago=forma_pago,
        monto=membresia.precio,
        fecha_pago=fecha_inicio,
        referencia=referencia,
    )

print("✅ Datos cargados correctamente")
print(f"   {Socios.objects.count()} socios")
print(f"   {Suscripciones.objects.count()} suscripciones")
print(f"   {Pagos.objects.count()} pagos")