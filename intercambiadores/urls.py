from django.urls import path
from .views import *

urlpatterns = [
    path('', FormularioSimulacion.as_view(), name='formulario_simulacion_intercambiadores')
]
