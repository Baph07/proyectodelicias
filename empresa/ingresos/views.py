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
    ventas = []  # lista vacía para evitar errores en el template
    return render(request, 'ingresos/lista_ingresos.html', {'ventas': ventas})

# Vista para ventas diarias (lista de ventas)
def ventas_diarias(request):
    return render(request, 'ingresos/ventas_diarias.html')

# Vista para ingresar venta
@login_required
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

    # Datos para Postres y Otros
    PRODUCTOS_POSTRES = {
        'Tortas': ['Porción', 'Completa'],
        'Quesillo': ['Porción', 'Completo'],
        'Yogurt': ['Pequeño', 'Mediano', 'Grande']
    }
    SABORES_POSTRES = {
        'Tortas': ['Piña','Marmoleada','Arequipe'],
        'Quesillo': [],
        'Yogurt': ['Griego','Fresa','Piña','Durazno','Ciruela']
    }
    PRODUCTOS_OTROS = [
        'Refresco litro y medio','Chupeta','Chesito','Q-citos','Caramelo lokiño','Galleta María','Galleta rellena'
    ]

    # Inicializar venta temporal en sesión
    if 'venta_temp' not in request.session:
        request.session['venta_temp'] = []

    categoria_seleccionada = None
    tipo_helado_seleccionado = None
    postre_seleccionado = None
    tamaños_postre = []
    sabores_postre = []

    if request.method == 'POST':
        categoria_seleccionada = request.POST.get('categoria')
        tipo_helado_seleccionado = request.POST.get('tipo_helado')
        postre_seleccionado = request.POST.get('tipo_postre')

        # Preparar tamaños y sabores de postres para el template
        if categoria_seleccionada == 'Postres' and postre_seleccionado:
            tamaños_postre = PRODUCTOS_POSTRES.get(postre_seleccionado, [])
            sabores_postre = SABORES_POSTRES.get(postre_seleccionado, [])

        # Agregar producto temporalmente
        if 'agregar_producto' in request.POST:
            producto = {'categoria': categoria_seleccionada, 'cantidad': int(request.POST.get('cantidad', 1))}

            if categoria_seleccionada == 'Helados':
                producto.update({
                    'tipo_helado': tipo_helado_seleccionado,
                    'sabor1': request.POST.get('sabor1'),
                    'sabor2': request.POST.get('sabor2')
                })

            elif categoria_seleccionada == 'Postres':
                producto.update({
                    'tipo_postre': postre_seleccionado,
                    'tamaño': request.POST.get('tamaño'),
                    'sabor1': request.POST.get('sabor1')
                })

            elif categoria_seleccionada == 'Otros':
                producto.update({
                    'nombre': request.POST.get('nombre')
                })

            request.session['venta_temp'].append(producto)
            request.session.modified = True
            return redirect('ingresar_venta')

        # Registrar venta completa
        elif 'registrar_venta' in request.POST:
            tipo_venta = request.session.get('tipo_venta', 'contado')

            nueva_venta = Venta.objects.create(tipo_venta=tipo_venta)

            for p in request.session.get('venta_temp', []):
                ProductoVenta.objects.create(
                    venta=nueva_venta,
                    categoria=p['categoria'],
                    tipo_helado=p.get('tipo_helado'),
                    sabor1=p.get('sabor1'),
                    sabor2=p.get('sabor2'),
                    tipo_postre=p.get('tipo_postre'),
                    tamaño=p.get('tamaño'),
                    nombre=p.get('nombre'),
                    cantidad=p.get('cantidad', 1)
                )

            request.session['venta_temp'] = []
            request.session.pop('tipo_venta', None)
            return redirect('ingresos')

    context = {
        'categorias': categorias,
        'tipos_helados': tipos_helados,
        'sabores': sabores,
        'doble_sabor': doble_sabor,
        'postres': PRODUCTOS_POSTRES,
        'sabores_postres_dict': SABORES_POSTRES,
        'otros': PRODUCTOS_OTROS,
        'categoria_seleccionada': categoria_seleccionada,
        'tipo_helado_seleccionado': tipo_helado_seleccionado,
        'postre_seleccionado': postre_seleccionado,
        'tamaños_postre': tamaños_postre,
        'sabores_postre': sabores_postre,
        'venta_temp': request.session.get('venta_temp', [])
    }

    return render(request, 'ingresos/ingresar_venta.html', context)



def reporte_ventas(request, tipo='diaria'):
    hoy = timezone.now().date()

    if tipo == 'diaria':
        ventas = Venta.objects.filter(fecha__date=hoy, tipo_venta='contado').order_by('id')
        titulo = "Ventas Diarias"
    elif tipo == 'semanal':
        hace_7_dias = hoy - timedelta(days=7)
        ventas = Venta.objects.filter(fecha__date__gte=hace_7_dias, tipo_venta='contado').order_by('id')
        titulo = "Ventas Semanales"
    else:
        ventas = Venta.objects.all().order_by('id')
        titulo = "Todas las Ventas"

    return render(request, 'ingresos/reporte_ventas.html', {'ventas': ventas, 'titulo': titulo, 'fecha_actual': hoy})
    
def reporte_ventas_pdf(request, tipo='diaria'):
    hoy = timezone.now().date()

    if tipo == 'diaria':
        ventas = Venta.objects.filter(fecha__date=hoy,tipo_venta='contado').order_by('id')
        titulo = "Ventas Diarias"
    elif tipo == 'semanal':
        hace_7_dias = hoy - timedelta(days=7)
        ventas = Venta.objects.filter(fecha__date__gte=hace_7_dias, tipo_venta='contado').order_by('id')
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

def seleccionar_tipo_venta(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo_venta')
        request.session['tipo_venta'] = tipo
        return redirect('ingresar_venta')

    return render(request, 'ingresos/seleccionar_tipo_venta.html')

def reporte_deudores(request):
    ventas = Venta.objects.filter(tipo_venta='credito').order_by('-fecha')
    return render(request, 'ingresos/reporte_deudores.html', {'ventas': ventas})
