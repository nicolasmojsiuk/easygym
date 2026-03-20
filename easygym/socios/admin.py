from django.contrib import admin
from django.utils.html import format_html
from .models import Socios, Membresias, Suscripciones, FormaPago, Pagos

@admin.register(Socios)
class SociosAdmin(admin.ModelAdmin):
    list_display = ('numero_socio', 'nombre', 'dni', 'whatsapp', 'activo')
    search_fields = ('nombre', 'dni')
    list_filter = ('activo',)
    ordering = ('-numero_socio',)

@admin.register(Membresias)
class MembresiaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'duracion_dias', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)

@admin.register(Suscripciones)
class SuscripcionAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_socio', 'get_membresia', 'monto', 'status_pago', 'status_vencimiento')
    search_fields = ('socio__nombre', 'socio__dni', 'membresia__nombre')
    list_filter = ('pagado', 'membresia', 'fecha_fin')
    readonly_fields = ('fecha_fin',) # Como es editable=False en el modelo, lo ponemos lectura

    def get_socio(self, obj):
        return obj.socio.nombre
    get_socio.short_description = 'Socio'

    def get_membresia(self, obj):
        return obj.membresia.nombre
    get_membresia.short_description = 'Plan'

    def status_pago(self, obj):
        if obj.pagado:
            return format_html('<span style="color: #28a745; font-weight: bold;">✔ Pagado</span>')
        return format_html('<span style="color: #dc3545; font-weight: bold;">✘ Pendiente</span>')
    status_pago.short_description = 'Estado Pago'

    def status_vencimiento(self, obj):
        if obj.estado == "Activa":
            return format_html('<b style="color:green;">Activa</b>')
        return format_html('<b style="color:red;">Vencida</b>')
    status_vencimiento.short_description = 'Vencimiento'

@admin.register(FormaPago)
class FormaPagoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    list_filter = ('activo',)

@admin.register(Pagos)
class PagosAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_socio', 'forma_pago', 'monto', 'fecha_pago')
    search_fields = ('suscripcion__socio__nombre', 'referencia')
    list_filter = ('forma_pago', 'fecha_pago')
    date_hierarchy = 'fecha_pago' # Agrega una barra de navegación por fechas arriba

    def get_socio(self, obj):
        return obj.suscripcion.socio.nombre
    get_socio.short_description = 'Socio'