from django.db import models

class Producto(models.Model):

    CATEGORIA_CHOICES = [
        ('helados', 'Helados'),
        ('postres', 'Postres'),
        ('otros', 'Otros'),
    ]

    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    tamaño = models.CharField(max_length=50, blank=True, null=True)
    sabor = models.CharField(max_length=50, blank=True, null=True)
    cantidad = models.PositiveIntegerField(default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)

    
    def __str__(self):
        return self.nombre
