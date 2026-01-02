from django.urls import path
from .views import lista_productos, agregar_producto

urlpatterns = [
    path('', lista_productos, name='inventario'),
    path('agregar/', agregar_producto, name='agregar_producto'),
]
