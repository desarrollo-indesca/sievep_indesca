from django.urls import path
from .views import *

urlpatterns = [
    # path('simulaciones', Simulaciones.as_view(), name='consulta_simulaciones'),
    # path('simulaciones/registro/', FormularioSimulaciones.as_view(), name="formulario_simulacion_intercambiadores"),
    path('', SeleccionTipo.as_view(), name="seleccion_tipo_intercambiador"),

    # RUTAS PARA TUBO CARCASA
    path('tubo_carcasa/', ConsultaTuboCarcasa.as_view(), name="consulta_tubo_carcasa"),
    path('tubo_carcasa/<int:pk>/', ConsultaEvaluacionesTuboCarcasa.as_view(), name="consulta_evaluaciones_tubo_carcasa"),
    path('tubo_carcasa/crear/', CrearIntercambiadorTuboCarcasa.as_view(),name="crear_tubo_carcasa"),
    path('tubo_carcasa/<int:pk>/evaluar/', CrearEvaluacionTuboCarcasa.as_view(),name="crear_evaluacion_tubo_carcasa"),
]
