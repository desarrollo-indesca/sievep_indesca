from django.db import models
from django.contrib.auth import get_user_model
import uuid

# Create your models here.

TIPOS_PREGUNTAS = [
    ('1', 'SI/NO'),
    ('2', 'NUMERICO'),
    ('3', 'TEXTO'),
    ('4', '1 AL 5'),
]

class Encuesta(models.Model):
    """
    Resumen:
        Modelo de registro de una encuesta.
    """
    nombre = models.CharField(max_length=50)

class Seccion(models.Model):
    """
    Resumen:
        Modelo de registro de una sección de una encuesta.
    """
    nombre = models.CharField(max_length=50)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE, related_name='secciones')

class Pregunta(models.Model):
    """
    Resumen:
        Modelo de registro de una pregunta de una encuesta.
    """
    nombre = models.CharField(max_length=150)
    tipo = models.CharField(max_length=1)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)

class Envio(models.Model):
    """
    Resumen:
        Modelo de registro de un envio de una encuesta por parte de un usuario.
    """
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

class Respuesta(models.Model):
    """
    Resumen:
        Modelo de registro de una respuesta de una encuesta por parte de un usuario.
    """
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    nombre = models.CharField(max_length=50)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    envio = models.ForeignKey(Envio, on_delete=models.CASCADE)
