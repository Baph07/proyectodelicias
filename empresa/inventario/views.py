from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Producto
from .forms import CategoriaForm, ProductoForm
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home.html')
# Diccionarios de productos y precios
PRODUCTOS = {
    'helados': {
        'Helado 2 Litros': ['Chocolate','Fresa','Stracciatella','Torta Suiza','ManteOreo','Ron con Pasas','Tornado','Stracciatella Fresa','Chicle','Samba','Cocosette','Uva'],
        'Helado 4.4 Litros': ['Chocolate','Fresa','Stracciatella','Torta Suiza','ManteOreo','Ron con Pasas','Tornado','Stracciatella Fresa','Chicle','Samba','Cocosette','Uva']
    },
    'postres': {
        'Tortas': {'Porción':['Piña','Marmoleada','Arequipe'], 'Completa Medio Kilo':['Piña','Marmoleada','Arequipe'], 'Completa Kilo':['Piña','Marmoleada','Arequipe']},
        'Quesillo': {'Porción':[], 'Completo':[]},
        'Yogurt': {'Pequeño':['Griego','Fresa','Piña','Durazno','Ciruela'], 'Mediano':['Griego','Fresa','Piña','Durazno','Ciruela'], 'Grande':['Griego','Fresa','Piña','Durazno','Ciruela']}
    },
    'otros': ['Cono Barquilla', 'Barquillon','Mini Cesta', 'Cesta','Refresco litro y medio','Chupeta','Chesito','Q-citos','Caramelo lokiño','Galleta María','Galleta rellena']
}

PRECIOS = {
    # Helados
    'Helado 2 Litros Chocolate': 25000,
    'Helado 2 Litros Fresa': 25000,
    'Helado 4.4 Litros Chocolate': 50000,
    'Helado 4.4 Litros Fresa': 50000,
    # Postres - Tortas
    'Torta Porción Piña': 7000,
    'Torta Completa Piña': 35000,
    # Quesillo
    'Quesillo Porción': 4000,
    'Quesillo Completo': 20000,
    # Yogurt
    'Yogurt Pequeño Griego': 5000,
    'Yogurt Mediano Fresa': 8000,
    # Otros
    'Refresco litro y medio': 3000,
    'Chupeta': 500,
    'Chesito': 2500,
}

# ===============================
# LISTA DE INVENTARIO
# ===============================
@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'inventario/lista.html', {'productos': productos})

# ===============================
# AGREGAR PRODUCTO MULTI-STEP
# ===============================
@login_required
def agregar_producto(request):
    paso = int(request.GET.get('paso', 1))
    categoria = request.GET.get('categoria')
    tipo_postre = request.GET.get('tipo_postre')  # para postres
    tamaño_sel = request.GET.get('tamaño')

    # -------------------------------
    # Paso 1: seleccionar categoría
    # -------------------------------
    if paso == 1:
        if request.method == 'POST':
            form = CategoriaForm(request.POST)
            if form.is_valid():
                cat = form.cleaned_data['categoria']
                url = reverse('agregar_producto')
                return HttpResponseRedirect(f"{url}?paso=2&categoria={cat}")
        else:
            form = CategoriaForm()
        return render(request, "inventario/agregar.html", {"form": form, "paso": 1})

    # -------------------------------
    # Paso 2: seleccionar tipo de postre (solo para postres)
    # -------------------------------
    elif paso == 2:
        if categoria == 'postres':
            tipos = [(p, p) for p in PRODUCTOS['postres'].keys()]
            if request.method == 'POST':
                tipo_postre_sel = request.POST.get('tipo_postre')
                if tipo_postre_sel:
                    url = reverse('agregar_producto')
                    return HttpResponseRedirect(f"{url}?paso=3&categoria={categoria}&tipo_postre={tipo_postre_sel}")
            return render(request, "inventario/agregar.html", {"paso": 2, "categoria": categoria, "tipos": tipos})

        # Para Helados y Otros, directamente paso 3
        return HttpResponseRedirect(f"{reverse('agregar_producto')}?paso=3&categoria={categoria}")

    # -------------------------------
    # Paso 3: seleccionar producto, tamaño, sabor y cantidad
    # -------------------------------
    elif paso == 3:
        opciones_nombre = []
        opciones_tamaño = []
        opciones_sabor = []

        # ----- HELADOS -----
        if categoria == 'helados':
            opciones_nombre = [('Helado', 'Helado')]
            opciones_tamaño = [(t, t) for t in PRODUCTOS['helados'].keys()]
            todos_sabores = set()
            for lista in PRODUCTOS['helados'].values():
                todos_sabores.update(lista)
            opciones_sabor = [(s, s) for s in sorted(todos_sabores)]

        # ----- POSTRES -----
        elif categoria == 'postres' and tipo_postre:
            opciones_nombre = [(tipo_postre, tipo_postre)]
            if tipo_postre == 'Tortas':
                opciones_tamaño = [(t, t) for t in PRODUCTOS['postres']['Tortas'].keys()]
                opciones_sabor = [(s, s) for s in ['Piña','Arequipe','Marmoleada']]
            elif tipo_postre == 'Quesillo':
                opciones_tamaño = [('Porción','Porción'),('Completo','Completo')]
                opciones_sabor = []
            elif tipo_postre == 'Yogurt':
                opciones_tamaño = [(t, t) for t in PRODUCTOS['postres']['Yogurt'].keys()]
                opciones_sabor = [(s, s) for s in ['Griego','Fresa','Piña','Durazno','Ciruela']]

        # ----- OTROS -----
        elif categoria == 'otros':
            opciones_nombre = [(p, p) for p in PRODUCTOS['otros']]

        # Crear formulario
        if request.method == 'POST':
            form = ProductoForm(request.POST)
            form.fields['nombre'].choices = opciones_nombre
            form.fields['tamaño'].choices = opciones_tamaño
            form.fields['sabor'].choices = opciones_sabor

            if form.is_valid():
                nombre = form.cleaned_data['nombre']
                tamaño_val = form.cleaned_data.get('tamaño')
                sabor_val = form.cleaned_data.get('sabor')
                cantidad = form.cleaned_data['cantidad']

                # Construir key para precios
                key = nombre
                if tamaño_val:
                    key = f"{key} {tamaño_val}"
                if sabor_val:
                    key = f"{key} {sabor_val}"
                precio = PRECIOS.get(key, 0)

                # ---------------- Ajustar stock para helados ----------------
                if categoria == 'helados':
                    if tamaño_val == 'Helado 2 Litros':
                        stock_nuevo = cantidad * 14
                    elif tamaño_val == 'Helado 4.4 Litros':
                        stock_nuevo = cantidad * 30
                    else:
                        stock_nuevo = cantidad
                else:
                    stock_nuevo = cantidad

                # ---------------- Guardar o actualizar ----------------
                producto_existente = Producto.objects.filter(
                    nombre=nombre,
                    categoria=categoria,
                    tamaño=tamaño_val,
                    sabor=sabor_val
                ).first()

                if producto_existente:
                    producto_existente.stock += stock_nuevo
                    producto_existente.precio = precio
                    producto_existente.save()
                else:
                    Producto.objects.create(
                        nombre=nombre,
                        categoria=categoria,
                        tamaño=tamaño_val,
                        sabor=sabor_val,
                        stock=stock_nuevo,
                        precio=precio
                    )
                return redirect('inventario')
        else:
            form = ProductoForm()
            form.fields['nombre'].choices = opciones_nombre
            form.fields['tamaño'].choices = opciones_tamaño
            form.fields['sabor'].choices = opciones_sabor

        return render(request, "inventario/agregar.html", {
            "form": form,
            "paso": 3,
            "categoria": categoria,
            "tipo_postre": tipo_postre,
            "tamaño": tamaño_sel
        })
