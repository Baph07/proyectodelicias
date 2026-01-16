from django.urls import path
from .views import ingresos, ventas_diarias, ingresar_venta, reporte_ventas, reporte_deudores, seleccionar_tipo_venta, seleccionar_metodo_pago, confirmar_venta, pagar_deuda, tasa_bcv_deuda, confirmar_pago_deuda, borrar_venta_temp, eliminar_producto_temp

urlpatterns = [
    path('', ingresos, name='ingresos'),                # Lista de ventas
    path('ventas_diarias/', ventas_diarias, name='ventas_diarias'),
    path('ingresar/', ingresar_venta, name='ingresar_venta'),  # Botón Ingresar Venta
    path('reporte/<str:tipo>/', reporte_ventas, name='reporte_ventas'), 
    path('deudores/', reporte_deudores, name='reporte_deudores'),
    path('tipo-venta/', seleccionar_tipo_venta, name='seleccionar_tipo_venta'),
    path('ingresos/metodo_pago/', seleccionar_metodo_pago, name='seleccionar_metodo_pago'),
    path('ingresos/confirmar_venta/<int:venta_id>/', confirmar_venta, name='confirmar_venta'),
     path('pagar_deuda/<int:venta_id>/', pagar_deuda, name='pagar_deuda'),
    path('tasa_bcv_deuda/', tasa_bcv_deuda, name='tasa_bcv_deuda'),
    path('confirmar_pago_deuda/', confirmar_pago_deuda, name='confirmar_pago_deuda'),
    path('borrar-venta/', borrar_venta_temp, name='borrar_venta_temp'),
    path('eliminar-producto/<int:index>/', eliminar_producto_temp, name='eliminar_producto_temp'),



]
