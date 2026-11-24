from django.db import models
from django.utils import timezone


class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='categorias/', null=True, blank=True)
    pub_date = models.DateTimeField('fecha de registro', auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'


class Producto(models.Model):
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name='productos'
    )
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    descripcion = models.TextField('descripción', blank=True, null=True)
    pub_date = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
