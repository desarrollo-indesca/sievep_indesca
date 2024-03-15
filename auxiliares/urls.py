from django.urls import path
from .views import *

urlpatterns = [
    path('', SeleccionEquipo.as_view(), name="seleccion_equipo"),

    # URLs de BOMBAS
    path('bombas/', ConsultaBombas.as_view(), name="consulta_bombas"),
]