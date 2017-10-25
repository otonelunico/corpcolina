from django.db import models
from django.contrib.auth.models import User


class Tecnico(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField()
    def __str__(self):
        return '{}'.format(self.nombre+" "+self.apellido)

class Estado(models.Model):
    titulo = models.CharField(max_length=50)
    def __str__(self):
        return '{}'.format(self.titulo)


class Establecimiento(models.Model):
    titulo = models.CharField(max_length=50)
    def __str__(self):
        return '{}'.format(self.titulo)

class Tema(models.Model):
    titulo = models.CharField(max_length=60)
    def __str__(self):
        return '{}'.format(self.titulo)

class Ticket(models.Model):
    usuario = models.ForeignKey(User, null=False, blank=True, on_delete=models.CASCADE)
    tema = models.ForeignKey(Tema, null=False, blank=True, on_delete=models.CASCADE)
    establecimiento = models.ForeignKey(Establecimiento, null=True, blank=True, on_delete=models.CASCADE)
    nom_contacto = models.CharField(max_length=50)
    ape_contacto = models.CharField(max_length=50)
    correo_contacto = models.EmailField()
    fijo_contacto = models.IntegerField(null=True, blank=True)
    celu_contacto = models.IntegerField(null=True, blank=True)
    resum_problema = models.CharField(max_length=100)
    asignado = models.IntegerField( null=True, blank=True)
    detall_problema = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado =  models.ForeignKey(Estado, null=False, blank=True, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return '{}'.format(self.resum_problema)

class Respuestas(models.Model):
    usuario = models.ForeignKey(User, null=False, blank=True, on_delete=models.CASCADE)
    mensaje = models.TextField(null=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(Ticket, null=True, blank=True, on_delete=models.CASCADE)

class Transfer(models.Model):
    transfer = models.TextField(null=False, blank=True)
