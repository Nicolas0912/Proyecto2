from django.db import connection, models
from django.contrib.auth.models import User

class Profile(models.Model):
    id = models.CharField(max_length=11,primary_key=True)
    telefono = models.CharField(max_length=25, null=True)
    documento = models.CharField(max_length=25, null=True)
    profile_img = models.ImageField(upload_to='profile_bd/', null=True)
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'profile'

class Servicio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, default=None)
    foto = models.ImageField(upload_to='imagenes_bd/', null=True)
    descripcion = models.CharField(max_length=500, null=True, blank=True)
    precio = models.CharField(max_length=255, null=True, blank=True)
    estado = models.BooleanField(null=True, blank=True)
    categoria = models.CharField(max_length=25, null=True, blank=True)
    max_personas = models.IntegerField(null=True, blank=True)
    min_personas = models.IntegerField(null=True, blank=True)
    dias_dispo = models.CharField(max_length=255,null=True, blank=True)

    class Meta:
        db_table = 'servicios'
        
class Galeria(models.Model):
    id = models.AutoField(primary_key=True)
    url_imagen = models.ImageField(upload_to='galeria_bd/', null=True)
    estado = models.BooleanField(null=True, blank=True)

    class Meta:
        db_table = 'galeria'

class Restaurante(models.Model):
    id = models.AutoField(primary_key=True)
    url_img = models.ImageField(upload_to='restaurante_bd/', null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    ubicacion = models.CharField(max_length=255,blank=True, null=True)
    is_active = models.BooleanField(null=True, blank=True)
    
    class Meta:
        db_table = 'restaurante'