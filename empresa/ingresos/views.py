from django.shortcuts import render, redirect
from .forms import ClienteForm, ProductoVentaForm, VentaForm
from .models import Cliente, Venta, DetalleVenta
from inventario.models import Producto
from inventario.views import PRODUCTOS, PRECIOS

# ---------------- Ingresar Venta ----------------
def ingresar_venta(request):
    # Inicializar sesión para productos
    if 'venta_productos' not in request.session:
        request.session['venta_productos'] = []

    # Paso 1: elegir tipo de venta
    if request.method == 'POST' and 'tipo_venta' in request.POST:
        tipo = request.POST.get('tipo_venta')
        request.session['tipo_venta'] = tipo
        # Si es contado, se crea la venta ya sin cliente
        if tipo == 'contado':
            # Crear venta temporal enumerada
            ultima = Venta.objects.filter(pago_contado=True).count()
            venta = Venta.objects.create(
                cliente=None,  # Cliente será None para ventas de contado
                pago_contado=True
            )
            request.session['venta_id'] = venta.id
            return redirect('agregar_productos_venta')
        else:
            return redirect('datos_cliente')

    return render(request, 'ingresos/seleccionar_tipo.html')


# ---------------- Datos Cliente para pago pendiente ----------------
def datos_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente_data = form.cleaned_data
            cliente, _ = Cliente.objects.get_or_create(
                id_cliente=cliente_data['id_cliente'],
                defaults={'nombre': cliente_data['nombre'], 'celular': cliente_data['celular']}
            )
            # Crear venta pendiente
            venta = Venta.objects.create(
                cliente=cliente,
                pago_contado=False
            )
            request.session['venta_id'] = venta.id
            return redirect('agregar_productos_venta')
    else:
        form = ClienteForm()
    return render(request, 'ingresos/datos_cliente.html', {'form': form})


# ---------------- Agregar productos ----------------
def agregar_productos_venta(request):
    venta_id = request.session.get('venta_id')
    venta = Venta.objects.get(id=venta_id)

    producto_form = ProductoVentaForm(request.POST or None)
    if request.method == 'POST' and 'agregar_producto' in request.POST:
        if producto_form.is_valid():
            data = producto_form.cleaned_data
            key = data['nombre']
            if data['tamaño']:
                key += f" {data['tamaño']}"
            if data['sabor']:
                key += f" {data['sabor']}"
            precio = PRECIOS.get(key, 0)

            # Actualizar stock solo si es contado o pendiente
            producto_obj = Producto.objects.get(nombre=data['nombre'], tamaño=data['tamaño'], sabor=data['sabor'])
            producto_obj.stock -= data['cantidad']
            producto_obj.save()

            DetalleVenta.objects.create(
                venta=venta,
                producto=producto_obj,
                cantidad=data['cantidad'],
                tamaño=data['tamaño'],
                sabor=data['sabor'],
                precio_unitario=precio
            )

    detalles = venta.detalleventa_set.all()
    if request.method == 'POST' and 'finalizar_venta' in request.POST:
        # Limpiar sesión
        del request.session['venta_id']
        return redirect('ingresos')

    return render(request, 'ingresos/agregar_productos.html', {
        'producto_form': producto_form,
        'detalles': detalles,
        'venta': venta
    })

# ---------------- Ventas diarias ----------------
def ventas_diarias(request):
    ventas = Venta.objects.filter(pago_contado=True)  # solo ventas de contado
    return render(request, 'ingresos/ventas_diarias.html', {'ventas': ventas})

# ---------------- Pagos pendientes ----------------
def pagos_pendientes(request):
    pendientes = Venta.objects.filter(pago_contado=False)
    return render(request, 'ingresos/pagos_pendientes.html', {'pendientes': pendientes})
