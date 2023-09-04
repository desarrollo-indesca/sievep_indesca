from django.urls import path
from .views import *

urlpatterns = [
    path('simulaciones', Simulaciones.as_view(), name='consulta_simulaciones'),
    path('simulaciones/registro/', FormularioSimulaciones.as_view(), name="formulario_simulacion_intercambiadores"),
    path('', ConsultaIntercambiadores.as_view(), name="consulta_intercambiadores"),

    # Consultar vía AJAX
    path('intercambiadores/<int:pk>/', Intercambiadores.as_view(), name="obtener_intercambiadores"),
    path('areas/<int:pk>/', Areas.as_view(), name="obtener_areas"),
    path('fluidos/<int:pk>/', Fluidos.as_view(), name="obtener_fluidos"),
]
