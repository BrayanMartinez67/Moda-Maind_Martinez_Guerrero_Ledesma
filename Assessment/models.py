from django.db import models
from django.conf import settings

from django.db import models
from django.contrib.auth.models import User

class Outfit(models.Model):
    imagen = models.ImageField(upload_to='outfits/')
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Outfit {self.id}"



class Evento(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Lugar(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class TipoCuerpo(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Evaluacion(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)
    tipo_cuerpo = models.ForeignKey(TipoCuerpo, on_delete=models.SET_NULL, null=True, blank=True)

    altura = models.PositiveIntegerField(null=True, blank=True)
    ancho_hombros = models.PositiveIntegerField(null=True, blank=True)
    pecho_espalda = models.PositiveIntegerField(null=True, blank=True)
    cintura = models.PositiveIntegerField(null=True, blank=True)
    busto = models.PositiveIntegerField(null=True, blank=True)
    cadera = models.PositiveIntegerField(null=True, blank=True)

    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evaluación #{self.id} - {self.evento.nombre} en {self.lugar.nombre}"

class CategoriaSuperiorMujer(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class PrendaSuperiorMujer(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaSuperiorMujer, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='armario/superior_mujer/')
    descripcion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.categoria.nombre} de {self.usuario.username}"
    
    
    
class CategoriaInferiorMujer(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class PrendaInferiorMujer(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaInferiorMujer, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='prendas/inferior/')
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.descripcion


class CategoriaCalzadoMujer(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class PrendaCalzadoMujer(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaCalzadoMujer, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='prendas/calzado/')
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.descripcion


class CategoriaSuperiorHombre(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class PrendaSuperiorHombre(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaSuperiorHombre, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='prendas/superior_hombre/')
    descripcion = models.CharField(max_length=200)
  

    def __str__(self):
        return self.descripcion


class CategoriaInferiorHombre(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class PrendaInferiorHombre(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaInferiorHombre, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='prendas/inferior_hombre/')
    descripcion = models.CharField(max_length=200)
 

    def __str__(self):
        return self.descripcion

class CategoriaCalzadoHombre(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class PrendaCalzadoHombre(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaCalzadoHombre, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='prendas/calzado_hombre/')
    descripcion = models.CharField(max_length=200)


    def __str__(self):
        return self.descripcion
