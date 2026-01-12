from django.db import models

class Venta(models.Model):
    TIPO_CHOICES = (
        ('contado', 'Contado'),
        ('credito', 'Crédito'),
    )

    fecha = models.DateTimeField(auto_now_add=True)
    tipo_venta = models.CharField(max_length=10, choices=TIPO_CHOICES)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    metodo_pago = models.CharField(max_length=50, blank=True, null=True)
    total_bs = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    def calcular_total(self):
        self.total = sum(p.subtotal for p in self.productos.all())
        self.save()


    def __str__(self):
        return f"Venta {self.id} - {self.tipo_venta} - ${self.total}"



class ProductoVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='productos')

    categoria = models.CharField(max_length=50)

    # Helados
    tipo_helado = models.CharField(max_length=50, blank=True, null=True)
    sabor1 = models.CharField(max_length=50, blank=True, null=True)
    sabor2 = models.CharField(max_length=50, blank=True, null=True)

    # Postres
    tipo_postre = models.CharField(max_length=50, blank=True, null=True)
    tamaño = models.CharField(max_length=50, blank=True, null=True)

    # Otros
    nombre = models.CharField(max_length=50, blank=True, null=True)

    cantidad = models.PositiveIntegerField(default=1)

    # 💰 NUEVO
    precio_unitario = models.DecimalField(max_digits=6, decimal_places=2)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.nombre or self.tipo_helado} - ${self.subtotal}"
