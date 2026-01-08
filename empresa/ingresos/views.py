from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Venta, ProductoVenta
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa




@login_required
def ingresos(request):
    # Obtener todas las ventas de la base de datos, ordenadas por ID
    ventas = Venta.objects.all().order_by('id')
    return render(request, 'ingresos/lista_ingresos.html', {'ventas': ventas})

# Vista para ventas diarias (lista de ventas)
def ventas_diarias(request):
    return render(request, 'ingresos/ventas_diarias.html')

# Vista para ingresar venta
def ingresar_venta(request):
    categorias = ['Helados', 'Postres', 'Otros']

    # Datos para Helados
    tipos_helados = [
        'Barquilla sencilla', 'Barquilla doble', 'Barquillón',
        'Mini Cesta', 'Cesta', 'Tina sencilla', 'Tina doble'
    ]
    sabores = [
        'Chocolate','Fresa','Stracciatella','Torta Suiza','ManteOreo',
        'Ron con Pasas','Tornado','Stracciatella Fresa','Chicle',
        'Samba','Cocosette','Uva'
    ]
    doble_sabor = ['Barquilla doble', 'Barquillón', 'Cesta', 'Tina doble']

    # Inicializar venta temporal en sesión
    if 'venta_temp' not in request.session:
        request.session['venta_temp'] = []

    categoria_seleccionada = None
    tipo_helado_seleccionado = None

    if request.method == 'POST':
        categoria_seleccionada = request.POST.get('categoria')
        tipo_helado_seleccionado = request.POST.get('tipo_helado')

        # Agregar producto temporalmente
        if 'agregar_producto' in request.POST:
            producto = {
                'categoria': categoria_seleccionada,
                'tipo_helado': tipo_helado_seleccionado,
                'sabor1': request.POST.get('sabor1'),
                'sabor2': request.POST.get('sabor2'),
                'cantidad': int(request.POST.get('cantidad', 1))
            }
            request.session['venta_temp'].append(producto)
            request.session.modified = True  # importante para que la sesión se actualice
            return redirect('ingresar_venta')

        # Registrar venta completa
        elif 'registrar_venta' in request.POST:
            nueva_venta = Venta.objects.create()
            for p in request.session.get('venta_temp', []):
                ProductoVenta.objects.create(
                    venta=nueva_venta,
                    categoria=p['categoria'],
                    tipo_helado=p.get('tipo_helado'),
                    sabor1=p.get('sabor1'),
                    sabor2=p.get('sabor2'),
                    cantidad=p.get('cantidad', 1)
                )
            # Limpiar venta temporal
            request.session['venta_temp'] = []
            return redirect('ingresos')  # redirige al dashboard

    context = {
        'categorias': categorias,
        'tipos_helados': tipos_helados,
        'sabores': sabores,
        'doble_sabor': doble_sabor,
        'categoria_seleccionada': categoria_seleccionada,
        'tipo_helado_seleccionado': tipo_helado_seleccionado,
        'venta_temp': request.session.get('venta_temp', [])
    }

    return render(request, 'ingresos/ingresar_venta.html', context)

def reporte_ventas(request, tipo='diaria'):
    hoy = timezone.now().date()

    if tipo == 'diaria':
        ventas = Venta.objects.filter(fecha__date=hoy).order_by('id')
        titulo = "Ventas Diarias"
    elif tipo == 'semanal':
        hace_7_dias = hoy - timedelta(days=7)
        ventas = Venta.objects.filter(fecha__date__gte=hace_7_dias).order_by('id')
        titulo = "Ventas Semanales"
    else:
        ventas = Venta.objects.all().order_by('id')
        titulo = "Todas las Ventas"

    return render(request, 'ingresos/reporte_ventas.html', {'ventas': ventas, 'titulo': titulo, 'fecha_actual': hoy})
    
def reporte_ventas_pdf(request, tipo='diaria'):
    hoy = timezone.now().date()

    if tipo == 'diaria':
        ventas = Venta.objects.filter(fecha__date=hoy).order_by('id')
        titulo = "Ventas Diarias"
    elif tipo == 'semanal':
        hace_7_dias = hoy - timedelta(days=7)
        ventas = Venta.objects.filter(fecha__date__gte=hace_7_dias).order_by('id')
        titulo = "Ventas Semanales"
    else:
        ventas = Venta.objects.all().order_by('id')
        titulo = "Todas las Ventas"

    template_path = 'ingresos/reporte_ventas_pdf.html'
    context = {'ventas': ventas, 'titulo': titulo, 'fecha_actual': hoy}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="{titulo}.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar PDF <pre>' + html + '</pre>')
    return response