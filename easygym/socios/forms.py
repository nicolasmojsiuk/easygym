from django.utils import timezone
from datetime import timedelta

from django import forms
from .models import Socios, Membresias, Suscripciones


class SocioForm(forms.ModelForm):
    class Meta:
        model = Socios
        fields = ['nombre', 'dni', 'email', 'whatsapp']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control custom-input', 'placeholder': 'Nombre completo'}),
            'dni': forms.TextInput(attrs={'class': 'form-control custom-input', 'placeholder': 'DNI sin puntos'}),
            'email': forms.EmailInput(attrs={'class': 'form-control custom-input', 'placeholder': 'correo@ejemplo.com'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control custom-input', 'placeholder': 'Ej: +54911...'}),
        }

class MembresiaForm(forms.ModelForm):
    class Meta:
        model = Membresias
        fields = ['nombre', 'precio', 'duracion_dias', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control custom-input'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control custom-input'}),
            'duracion_dias': forms.NumberInput(attrs={'class': 'form-control custom-input'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control custom-input', 'rows': 2}),
        }


class SuscripcionesForm(forms.ModelForm):
    class Meta:

        model = Suscripciones
        fields = ['socio', 'membresia', 'fecha_inicio', 'monto']

        widgets = {
            'socio': forms.Select(attrs={'class': 'form-select custom-input'}),
            'membresia': forms.Select(attrs={'class': 'form-select custom-input'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control custom-input', 'type': 'date'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control custom-input', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['socio'].queryset = Socios.objects.filter(activo=True).order_by('nombre')
        self.fields['membresia'].queryset = Membresias.objects.filter(activo=True).order_by('nombre')