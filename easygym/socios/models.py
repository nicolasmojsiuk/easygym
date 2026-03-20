import uuid

from django.utils import timezone
from datetime import timedelta

from django.db import models

class Socios(models.Model):
    numero_socio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    dni = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Socio #{self.numero_socio} - {self.nombre} - (DNI: {self.dni})"


    class Meta:
        verbose_name = "Socio"
        verbose_name_plural = "Socios"
        db_table = 'socios'

class Membresias(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_dias = models.PositiveIntegerField(default=30)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Suscripciones(models.Model):
    # Django genera automáticamente el ID (id_suscripcion)

    # numero_socio (Relación con la tabla Socios)
    socio = models.ForeignKey('Socios', on_delete=models.CASCADE, related_name='suscripciones_set')

    # id_membresia (Relación con la tabla Membresias)
    membresia = models.ForeignKey('Membresias', on_delete=models.PROTECT)

    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField(editable=False)  # Se calcula automáticamente

    # Campos de dinero y estado de cobro
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    pagado = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Suscripción"
        verbose_name_plural = "Suscripciones"
        db_table = 'Suscripciones'  # Nombre de la tabla en plural

    def save(self, *args, **kwargs):
        # Lógica: Fecha Fin = Inicio + duración de la membresía elegida
        if not self.fecha_fin:
            self.fecha_fin = self.fecha_inicio + timedelta(days=self.membresia.duracion_dias)
        super().save(*args, **kwargs)

    @property
    def estado(self):
        """Calcula si está vigente o vencida según la fecha actual"""
        if timezone.now().date() > self.fecha_fin:
            return "Vencida"
        return "Activa"

    def __str__(self):
        estado_pago = "Pagado" if self.pagado else "Pendiente"
        return f"Suscrip. {self.id} - {self.socio.nombre} ({estado_pago})"


class FormaPago(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Forma de Pago"
        verbose_name_plural = "Formas de Pago"
        db_table = 'Formas_Pago'

    def __str__(self):
        return self.nombre


class Pagos(models.Model):
    # Relación con la suscripción (Cada pago pertenece a una suscripción)
    suscripcion = models.ForeignKey('Suscripciones', on_delete=models.CASCADE, related_name='pagos_detalle')

    # Relación con la forma de pago (Efectivo, Transferencia, etc.)
    forma_pago = models.ForeignKey(FormaPago, on_delete=models.PROTECT)

    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(default=timezone.now)

    # Comprobante o nro de operación para transferencias
    referencia = models.CharField(max_length=100, blank=True, null=True, help_text="Nro de ticket o transferencia")
    notas = models.TextField(blank=True, null=True)

    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        db_table = 'Pagos'

    def __str__(self):
        return f"Pago {self.id} - {self.suscripcion.socio.nombre} (${self.monto})"


class ConfiguracionGym(models.Model):

    nombre_gimnasio = models.CharField(max_length=100)
    telefono = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.CharField(max_length=200, blank=True)

    descripcion = models.TextField(blank=True)

    moneda = models.CharField(max_length=5, default="$")

    logo = models.ImageField(upload_to="logos/", blank=True, null=True)

    def __str__(self):
        return self.nombre_gimnasio