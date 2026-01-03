from django.db import models
from inventario.models import Producto

class Egreso(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} ({self.fecha.date()})"
