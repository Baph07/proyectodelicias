from django.urls import path
from .views import ingresos, ventas_diarias, ingresar_venta, reporte_ventas, reporte_deudores, seleccionar_tipo_venta

urlpatterns = [
    path('', ingresos, name='ingresos'),                # Lista de ventas
    path('ventas_diarias/', ventas_diarias, name='ventas_diarias'),
    path('ingresar/', ingresar_venta, name='ingresar_venta'),  # Botón Ingresar Venta
    path('reporte/<str:tipo>/', reporte_ventas, name='reporte_ventas'), 
    path('deudores/', reporte_deudores, name='reporte_deudores'),
    path('tipo-venta/', seleccionar_tipo_venta, name='seleccionar_tipo_venta'),


]
