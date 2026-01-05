from django import forms
from .models import Producto

# ===============================
# FORMULARIO PASO 1: SELECCIONAR CATEGORÍA
# ===============================
class CategoriaForm(forms.Form):
    CATEGORIA_CHOICES = [
        ('helados', 'Helados'),
        ('postres', 'Postres'),
        ('otros', 'Otros'),
    ]
    categoria = forms.ChoiceField(
        choices=CATEGORIA_CHOICES,
        label="Categoría",
        widget=forms.Select(attrs={
            'class': 'input no-move'  # ahora es compacto y estático
        })
    )

# ===============================
# FORMULARIO PASO 2: AGREGAR PRODUCTO
# ===============================
class ProductoForm(forms.Form):
    # Estos campos se llenarán dinámicamente desde views.py
    nombre = forms.ChoiceField(choices=[], label="Producto", widget=forms.Select(attrs={'class': 'form-select'}))
    tamaño = forms.ChoiceField(choices=[], required=False, label="Tamaño", widget=forms.Select(attrs={'class': 'form-select'}))
    sabor = forms.ChoiceField(choices=[], required=False, label="Sabor", widget=forms.Select(attrs={'class': 'form-select'}))
    cantidad = forms.IntegerField(min_value=1, initial=1, label="Cantidad", widget=forms.NumberInput(attrs={'class': 'form-input'}))
