from django.db.models.functions import window
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_socios, name='lista_socios'),
    path('editar/<int:id>/', views.editar_socio, name='editar_socio'),
    path('desactivar/<int:id>/', views.desactivar_socio, name='desactivar_socio'),
    path('membresias/', views.lista_membresias, name='lista_membresias'),
    path('membresias/desactivar/<int:id>/', views.desactivar_membresia, name='desactivar_membresia'),
    path('suscripciones/', views.lista_suscripciones, name='lista_suscripciones'),
    path('suscripciones/eliminar/<int:id>/', views.eliminar_suscripcion, name='eliminar_suscripcion'),
    path('suscripciones/pagar/<int:id>/', views.pagar_suscripcion, name='pagar_suscripcion'),
    path("comprobante/<int:pago_id>/", views.comprobante_pago, name="comprobante_pago"),
]