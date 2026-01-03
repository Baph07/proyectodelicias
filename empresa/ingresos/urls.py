from django.urls import path
from .views import ingresar_venta, datos_cliente, agregar_productos_venta, ventas_diarias, pagos_pendientes

urlpatterns = [
    path('', ventas_diarias, name='ingresos'),
    path('ingresar/', ingresar_venta, name='ingresar_venta'),
    path('datos_cliente/', datos_cliente, name='datos_cliente'),
    path('agregar_productos/', agregar_productos_venta, name='agregar_productos_venta'),
    path('pagos_pendientes/', pagos_pendientes, name='pagos_pendientes'),
]

