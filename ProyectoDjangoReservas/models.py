from django.db import connection, models

class Servicio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, default=None)
    foto = models.ImageField(upload_to='imagenes_bd/', null=True)
    descripcion = models.CharField(max_length=500, null=True, blank=True)
    precio = models.CharField(max_length=255, null=True, blank=True)
    categoria = models.CharField(max_length=255, null=True, blank=True)
    estado = models.BooleanField(null=True, blank=True)

    class Meta:
        db_table = 'servicios'

class Galeria(models.Model):
    id = models.AutoField(primary_key=True)
    url_imagen = models.ImageField(upload_to='galeria_bd/', null=True)
    estado = models.BooleanField(null=True, blank=True)

    class Meta:
        db_table = 'galeria'