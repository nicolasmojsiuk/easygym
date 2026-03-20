from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.custom_login, name='login'),

    path('home/', views.home, name='home'),

    path('logout/', views.custom_logout, name='logout'),
    path('socios/', include('socios.urls')),
    path('finanzas/', views.vista_finanzas, name='vista_finanzas'),
    path('ajustes/', views.vista_ajustes, name='vista_ajustes'),
    path("verificar_pago/<uuid:token>/", views.verificar_pago, name="verificar_pago"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)