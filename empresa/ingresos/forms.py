from django import forms
from .models import Cliente, Venta
from inventario.models import Producto

# ---------------- Cliente ----------------
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'id_cliente', 'celular']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-input'}),
            'id_cliente': forms.TextInput(attrs={'class':'form-input'}),
            'celular': forms.TextInput(attrs={'class':'form-input'}),
        }

# ---------------- Producto Venta ----------------
class ProductoVentaForm(forms.Form):
    categoria = forms.ChoiceField(
        choices=[('helados','Helados'), ('postres','Postres'), ('otros','Otros')],
        widget=forms.Select(attrs={'class':'form-select'})
    )
    nombre = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class':'form-select'}))
    tamaño = forms.ChoiceField(choices=[], required=False, widget=forms.Select(attrs={'class':'form-select'}))
    sabor = forms.ChoiceField(choices=[], required=False, widget=forms.Select(attrs={'class':'form-select'}))
    cantidad = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={'class':'form-input'}))

# ---------------- Pago ----------------
class VentaForm(forms.Form):
    pago_contado = forms.ChoiceField(
        choices=[('contado','Pago de contado'),('pendiente','Pago pendiente')],
        widget=forms.RadioSelect
    )
    metodo_pago = forms.ChoiceField(
        choices=[('dolares','Dólares'), ('bs_efectivo','Bs efectivo'), ('bs_transferencia','Bs transferencia')],
        required=False,
        widget=forms.Select(attrs={'class':'form-select'})
    )
