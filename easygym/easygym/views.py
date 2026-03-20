from django.conf import settings
from django.conf.urls.static import static
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone

from socios.models import Socios, Pagos, FormaPago, ConfiguracionGym
from datetime import timedelta






def verificar_pago(request, token):
    pago = get_object_or_404(
        Pagos.objects.select_related(
            "suscripcion__socio",
            "suscripcion__membresia"
        ),
        token=token
    )

    return render(request, "verificar_pago.html", {
        "pago": pago,
        "now": timezone.now().date(),
    })


@never_cache # Esto evita que el navegador guarde la página en el historial
@csrf_protect
def custom_login(request):
    if request.user.is_authenticated:
        return redirect('/home/')


    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Esto captura el ?next=/home/ de la URL si existe
            next_url = request.GET.get('next', '/home/')
            return redirect(next_url)
        else:
            # Enviamos la variable 'error' que ahora el HTML sí reconoce
            return render(request, 'login.html', {
                'error': 'Usuario o contraseña incorrectos'
            })

    return render(request, 'login.html')


def custom_logout(request):
    logout(request)
    return redirect('/')





def vista_finanzas(request):
    pagos = Pagos.objects.all().order_by('-fecha_pago')
    formas_pago = FormaPago.objects.filter(activo=True)

    # --- FILTROS ---
    metodo = request.GET.get('metodo')
    periodo = request.GET.get('periodo')
    mes_nro = request.GET.get('mes_nro')
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')

    hoy = timezone.now().date()

    if metodo:
        pagos = pagos.filter(forma_pago_id=metodo)

    if periodo == 'dia':
        pagos = pagos.filter(fecha_pago__date=hoy)
    elif periodo == 'semana':
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        pagos = pagos.filter(fecha_pago__date__gte=inicio_semana)
    elif periodo == 'mes':
        pagos = pagos.filter(fecha_pago__month=hoy.month, fecha_pago__year=hoy.year)

    if mes_nro:
        pagos = pagos.filter(fecha_pago__month=mes_nro, fecha_pago__year=hoy.year)

    if desde and hasta:
        pagos = pagos.filter(fecha_pago__date__range=[desde, hasta])

    # --- CÁLCULOS PARA TARJETAS ---
    total_recaudado = pagos.aggregate(Sum('monto'))['monto__sum'] or 0

    context = {
        'pagos': pagos,
        'formas_pago': formas_pago,
        'total_recaudado': total_recaudado,
        'hoy': hoy,
        # ✅ Agregado: el template necesita este dict para mostrar los filtros activos
        'filtros': {
            'metodo': metodo or '',
            'periodo': periodo or '',
            'mes_nro': mes_nro or '',
            'desde': desde or '',
            'hasta': hasta or '',
        },
    }
    return render(request, 'finanzas.html', context)

@login_required
def home(request):
    hoy = timezone.now().date()
    primer_dia_mes = hoy.replace(day=1)

    # Recaudación de hoy
    recaudacion_hoy = Pagos.objects.filter(
        fecha_pago__date=hoy
    ).aggregate(Sum('monto'))['monto__sum'] or 0

    # Recaudación del mes
    recaudacion_mes = Pagos.objects.filter(
        fecha_pago__date__gte=primer_dia_mes
    ).aggregate(Sum('monto'))['monto__sum'] or 0

    # Socios activos
    total_socios = Socios.objects.filter(activo=True).count()

    # Socios nuevos este mes
    socios_nuevos_mes = Socios.objects.filter(
        fecha_alta__date__gte=primer_dia_mes
    ).count()

    # Gráfico: ingresos por mes (últimos 6 meses)
    meses_labels = []
    meses_data = []

    for i in range(5, -1, -1):
        # Calcular el mes correspondiente
        mes_fecha = (hoy.replace(day=1) - timedelta(days=1)).replace(day=1) if i > 0 else primer_dia_mes
        # Forma correcta de restar meses
        año = hoy.year
        mes = hoy.month - i
        while mes <= 0:
            mes += 12
            año -= 1

        total = Pagos.objects.filter(
            fecha_pago__year=año,
            fecha_pago__month=mes
        ).aggregate(Sum('monto'))['monto__sum'] or 0

        from calendar import month_abbr
        meses_labels.append(f"{month_abbr[mes]} {año}")
        meses_data.append(float(total))

    context = {
        'total_socios': total_socios,
        'recaudacion_hoy': recaudacion_hoy,
        'recaudacion_mes': recaudacion_mes,
        'socios_nuevos_mes': socios_nuevos_mes,
        'meses_labels': meses_labels,
        'meses_data': meses_data,
    }

    return render(request, 'home.html', context)

@login_required
def vista_ajustes(request):

    configuracion = ConfiguracionGym.objects.first()

    # si no existe la configuración la creamos
    if not configuracion:
        configuracion = ConfiguracionGym.objects.create(
            nombre_gimnasio="Mi Gimnasio"
        )

    if request.method == "POST":

        configuracion.nombre_gimnasio = request.POST.get("nombre_gimnasio")
        configuracion.telefono = request.POST.get("telefono")
        configuracion.email = request.POST.get("email")
        configuracion.direccion = request.POST.get("direccion")
        configuracion.descripcion = request.POST.get("descripcion")
        configuracion.moneda = request.POST.get("moneda")

        if request.FILES.get("logo"):
            configuracion.logo = request.FILES.get("logo")

        configuracion.save()

        messages.success(request, "Ajustes guardados correctamente")

        return redirect("vista_ajustes")

    context = {
        "configuracion": configuracion
    }

    return render(request, "ajustes.html", context)




