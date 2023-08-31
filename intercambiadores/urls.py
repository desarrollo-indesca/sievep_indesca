from django.urls import path
from .views import *

urlpatterns = [
    path('', Simulaciones.as_view(), name='consulta_simulaciones'),
    path('registro', FormularioSimulaciones.as_view(), name="formulario_simulacion_intercambiadores")
]
