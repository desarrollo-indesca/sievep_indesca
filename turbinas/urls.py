from django.urls import path
from .views import *

urlpatterns = [
    path('vapor/', ConsultaTurbinasVapor.as_view(), name="consulta_turbinas_vapor"),
    path('vapor/creacion/', CreacionTurbinaVapor.as_view(), name="creacion_turbina_vapor"),
    path('vapor/edicion/<int:pk>', EdicionTurbinaVapor.as_view(), name="edicion_turbina_vapor"),
    path('vapor/evaluaciones/<int:pk>/', ConsultaEvaluacionTurbinaVapor.as_view(), name="evaluaciones_turbina_vapor"),
    path('vapor/evaluaciones/<int:pk>/crear/', CreacionEvaluacionTurbinaVapor.as_view(), name="evaluacion_turbina_vapor"),
    path("vapor/evaluar/<int:pk>/", CalcularResultadosVentilador.as_view(), name="evaluar_turbina_vapor")
]