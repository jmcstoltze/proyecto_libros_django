from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from uuid import uuid4

# Create your models here.

# Se usará el modelo de Usuario por defecto de Django. EL tipo de usuario vendrá dado por si es superuser o no. Es decir, is_superuser True, entonces admin, de lo contratio es un lector (False). El campo de email de User es Unique por defecto.


# Modelo para géneros
class Genero(models.Model):
    nombre = models.CharField(max_length=100, unique=True, null=False, blank=False)
    
    # Representación de cadena que retorna el modelo
    def __str__(self):
        return self.nombre
    
    # Define opciones del modelo
    class Meta:
        verbose_name = "Genero"
        verbose_name_plural = "Generos"
        ordering = ["nombre"]


# Modelo para autores
class Autor(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    apellido = models.CharField(max_length=100, null=False, blank=False)

    # Representación de cadena que retorna el modelo
    def __str__(self):
        return f"{self.apellido}, {self.nombre}"
    
    # Define opciones del modelo
    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ["apellido", "nombre"]
        unique_together = ["nombre", "apellido"] ######## El autor es un campo unique


# Modelo para los libros
class Libro(models.Model):
    titulo = models.CharField(max_length=255, unique=True, null=False, blank=False)
    descripcion = models.CharField(max_length=255, null=False, blank=False)
    anio_publicacion = models.IntegerField(null=False, blank=False)
    portada_url = models.CharField(max_length=255, null=True, blank=True)
    genero = models.ManyToManyField(Genero) ################ Relación N:N con la entidad Genero
    autor = models.ManyToManyField(Autor) ################ Relación N:N con la entidad Autor
    
    # Representación de cadena que retorna el modelo
    def __str__(self):
        return self.titulo
    
    # Define opciones del modelo
    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"
        ordering = ["titulo"]


# Modelo para las reseñas
class Resena(models.Model):    
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE) ############## Relación 1:N con la entidad Libro
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) ################################### Relación 1:N con la entidad User
    calificacion = models.IntegerField(null=False, blank=False)
    comentario = models.CharField(max_length=255, null=False, blank=False)
    fecha_resena = models.DateTimeField(default=timezone.now)

    # Representación de cadena que retorna el modelo
    def __str__(self):
        return self.comentario
    
    # Define opciones del modelo
    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        ordering = ["-fecha_resena"] # Ordena de manera descendente por fecha


# Modelo para los contactos
class Contacto(models.Model):
    contact_form_uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    nombre = models.CharField(max_length=100, null=False, blank=False)
    apellido = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField()
    mensaje = models.CharField(max_length=255, null=False, blank=False)
    fecha_contacto = models.DateTimeField(default=timezone.now)

    # Representación de cadena que retorna el modelo
    def __str__(self):
        return self.mensaje
    
    # Define opciones del modelo
    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"
        ordering = ["-fecha_contacto"] # Ordena de manera descendente por fecha
