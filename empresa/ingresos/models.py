from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    id_cliente = models.CharField(max_length=20, unique=True)
    celular = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Venta(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, null=True, blank=True
    )
    pago_contado = models.BooleanField(default=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venta #{self.id}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey('inventario.Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    tamaño = models.CharField(max_length=50, blank=True, null=True)
    sabor = models.CharField(max_length=50, blank=True, null=True)
    precio_unitario = models.FloatField()
