from django.db import models
from django.contrib.auth import get_user_model

from intercambiadores.models import Planta

# Create your models here.

class Caldera(models.Model):
    planta = models.ForeignKey(Planta, on_delete=models.PROTECT, related_name="planta_caldera")
    tag = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=100, verbose_name="Descripción")
    fabricante = models.CharField(max_length=45, null = True, blank = True)
    modelo = models.CharField(max_length=45, null = True, blank = True)
    creado_al = models.DateTimeField(auto_now_add=True)
    editado_al = models.DateTimeField(null = True)

    creado_por = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name="caldera_creada_por")
    editado_por = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, null = True, related_name="caldera_editada_por")

    class Meta:
        db_table = "calderas_caldera"