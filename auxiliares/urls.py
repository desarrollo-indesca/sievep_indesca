from django.urls import path
from .views import *

urlpatterns = [
    path('', SeleccionEquipo.as_view(), name="seleccion_equipo"),

    # URLs de BOMBAS
    path('bombas/', ConsultaBombas.as_view(), name="consulta_bombas"),
    path('bombas/creacion/', CreacionBomba.as_view(), name="creacion_bomba"),
    path('bombas/edicion/<int:pk>/', EdicionBomba.as_view(), name="edicion_bomba"),
    path('bombas/datos_fluido/', ObtencionDatosFluidosBomba.as_view(), name="datos_fluido_bomba"),
]