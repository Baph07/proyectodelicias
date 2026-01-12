from django.db import models

class Venta(models.Model):
    TIPO_CHOICES = (
        ('contado', 'Contado'),
        ('credito', 'Crédito'),
    )

    fecha = models.DateTimeField(auto_now_add=True)
    tipo_venta = models.CharField(max_length=10, choices=TIPO_CHOICES)

    def __str__(self):
        return f"Venta {self.id} - {self.tipo_venta}"



class ProductoVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='productos')
    categoria = models.CharField(max_length=50)
    tipo_helado = models.CharField(max_length=50, blank=True, null=True)
    sabor1 = models.CharField(max_length=50, blank=True, null=True)
    sabor2 = models.CharField(max_length=50, blank=True, null=True)
    tipo_postre = models.CharField(max_length=50, blank=True, null=True)
    tamaño = models.CharField(max_length=50, blank=True, null=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.tipo_helado} ({self.sabor1}{', ' + self.sabor2 if self.sabor2 else ''})"
