from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Socios, Membresias, Suscripciones, FormaPago, Pagos, ConfiguracionGym
from .forms import SocioForm, MembresiaForm, SuscripcionesForm
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from django.conf import settings
import qrcode
import io

@login_required
def lista_socios(request):
    # Lógica para guardar NUEVO o EDITAR existente
    socio_id = request.POST.get('socio_id')  # Campo oculto en el form
    if request.method == 'POST':
        if socio_id:  # Si hay ID, estamos editando
            instancia = get_object_or_404(Socios, numero_socio=socio_id)
            form = SocioForm(request.POST, instance=instancia)
        else:  # Si no hay ID, es nuevo
            form = SocioForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('lista_socios')

    socios = Socios.objects.filter(activo=True).order_by('-fecha_alta')
    form = SocioForm()
    return render(request, 'socios.html', {'socios': socios, 'form': form})

def editar_socio(request, id):
    socio = get_object_or_404(Socios, numero_socio=id)
    if request.method == 'POST':
        form = SocioForm(request.POST, instance=socio)
        if form.is_valid():
            form.save()
            return redirect('lista_socios')


def desactivar_socio(request, id):
    socio = get_object_or_404(Socios, numero_socio=id)
    socio.activo = False # "Eliminar" es desactivar
    socio.save()
    return redirect('lista_socios')


@login_required
def lista_membresias(request):
    if request.method == 'POST':
        # Buscamos el ID que solo envía el modal de edición
        edit_id = request.POST.get('membresia_id_editar')

        if edit_id:  # LÓGICA DE EDICIÓN
            instancia = get_object_or_404(Membresias, id=edit_id)
            form = MembresiaForm(request.POST, instance=instancia)
        else:  # LÓGICA DE CREACIÓN
            form = MembresiaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('lista_membresias')

    # GET
    membresias = Membresias.objects.filter(activo=True)
    form = MembresiaForm()
    return render(request, 'membresias.html', {'membresias': membresias, 'form': form})

def desactivar_membresia(request, id):
    # Usamos 'id' porque es el campo que Django te marca como disponible
    membresia = get_object_or_404(Membresias, id=id)
    membresia.activo = False
    membresia.save()
    return redirect('lista_membresias')

@login_required
def lista_suscripciones(request):
    if request.method == 'POST':
        form = SuscripcionesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_suscripciones')
    else:
        form = SuscripcionesForm()
        # Esto asegura que el dropdown de socios solo muestre a los activos
        form.fields['socio'].queryset = Socios.objects.filter(activo=True)
        form.fields['membresia'].queryset = Membresias.objects.filter(activo=True)

    suscripciones = Suscripciones.objects.all().order_by('-fecha_inicio')
    context = {
        'suscripciones': Suscripciones.objects.all().order_by('-id'),
        'form': SuscripcionesForm(),
        'membresias_lista': Membresias.objects.filter(activo=True),
        'formas_pago': FormaPago.objects.filter(activo=True),  # ESTO ES NUEVO
    }
    return render(request, 'suscripciones.html', context)

def eliminar_suscripcion(request, id):
    suscripcion = get_object_or_404(Suscripciones, id=id)
    suscripcion.delete() # Aquí sí solemos borrar, o puedes usar activo=False si prefieres
    return redirect('lista_suscripciones')


from django.core.mail import EmailMessage

def pagar_suscripcion(request, id):
    suscripcion = get_object_or_404(Suscripciones, id=id)

    if request.method == 'POST':
        forma_pago_id = request.POST.get('forma_pago')
        referencia = request.POST.get('referencia')
        forma_pago = get_object_or_404(FormaPago, id=forma_pago_id)

        pago = Pagos.objects.create(
            suscripcion=suscripcion,
            forma_pago=forma_pago,
            monto=suscripcion.monto,
            referencia=referencia,
            fecha_pago=timezone.localtime(timezone.now())
        )

        suscripcion.pagado = True
        suscripcion.save()

        # Enviar correo si el socio tiene email
        email_socio = suscripcion.socio.email
        if email_socio:
            config = ConfiguracionGym.objects.first()
            pdf_buffer = generar_pdf_comprobante(pago, config)

            mail = EmailMessage(
                subject=f'Comprobante de pago - {config.nombre_gimnasio}',
                body=f'Hola {suscripcion.socio.nombre}, adjuntamos tu comprobante de pago.',
                to=[email_socio],
            )
            mail.attach(
                f'comprobante_{pago.id}.pdf',
                pdf_buffer.read(),
                'application/pdf'
            )
            mail.send()

        return JsonResponse({'ok': True, 'pago_id': pago.id})

    return redirect('lista_suscripciones')


def generar_pdf_comprobante(pago, config):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    if config.logo:
        p.drawImage(config.logo.path, 50, 750, width=80, height=80)

    p.setFont("Helvetica-Bold", 18)
    p.drawString(150, 800, config.nombre_gimnasio)
    p.setFont("Helvetica", 10)
    p.drawString(150, 785, f"Tel: {config.telefono}")
    p.drawString(150, 770, f"Email: {config.email}")
    p.drawString(150, 755, f"Dirección: {config.direccion}")

    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(300, 720, "COMPROBANTE DE PAGO")

    y, x = 680, 50
    p.setFont("Helvetica", 12)
    p.drawString(x, y, f"Socio: {pago.suscripcion.socio.nombre}"); y -= 20
    p.drawString(x, y, f"DNI: {pago.suscripcion.socio.dni}"); y -= 20
    p.drawString(x, y, f"Membresía: {pago.suscripcion.membresia.nombre}"); y -= 20
    p.drawString(x, y, f"Fecha inicio: {pago.suscripcion.fecha_inicio}"); y -= 20
    p.drawString(x, y, f"Fecha fin: {pago.suscripcion.fecha_fin}"); y -= 30

    p.setFont("Helvetica-Bold", 12)
    p.drawString(x, y, "Detalle del Pago"); y -= 20
    p.setFont("Helvetica", 12)
    p.drawString(x, y, f"Monto pagado: {config.moneda}{pago.monto}"); y -= 20
    p.drawString(x, y, f"Forma de pago: {pago.forma_pago.nombre}"); y -= 20
    fecha_local = timezone.localtime(pago.fecha_pago)
    p.drawString(x, y, f"Fecha de pago: {fecha_local.strftime('%d/%m/%Y %H:%M')}"); y -= 20
    if pago.referencia:
        p.drawString(x, y, f"Referencia: {pago.referencia}"); y -= 20

    url_verificacion = f"http://127.0.0.1:8000/verificar_pago/{pago.token}/"
    qr = qrcode.make(url_verificacion)
    qr_buffer = io.BytesIO()
    qr.save(qr_buffer)
    qr_buffer.seek(0)
    p.drawImage(ImageReader(qr_buffer), 420, 600, width=120, height=120)
    p.setFont("Helvetica", 8)
    p.drawCentredString(480, 585, "Escanee para verificar")

    p.setFont("Helvetica", 10)
    p.drawString(x, 380, "Gracias por su pago")
    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer


def comprobante_pago(request, pago_id):
    pago = Pagos.objects.select_related(
        "suscripcion__socio",
        "suscripcion__membresia",
        "forma_pago"
    ).get(id=pago_id)

    config = ConfiguracionGym.objects.first()

    pdf_buffer = generar_pdf_comprobante(pago, config)

    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="comprobante_{pago_id}.pdf"'
    return response






