from django.urls import path
from .views import *

urlpatterns = [
    # path('simulaciones', Simulaciones.as_view(), name='consulta_simulaciones'),
    # path('simulaciones/registro/', FormularioSimulaciones.as_view(), name="formulario_simulacion_intercambiadores"),
    path('', SeleccionTipo.as_view(), name="seleccion_tipo_intercambiador"),
    path('consultar/<str:tipo>/', ConsultaVacia.as_view(), name="consulta_vacia"),

    # RUTAS PARA TUBO CARCASA
    path('tubo_carcasa/', ConsultaTuboCarcasa.as_view(), name="consulta_tubo_carcasa"),
    path('tubo_carcasa/<int:pk>/', ConsultaEvaluacionesTuboCarcasa.as_view(), name="consulta_evaluaciones_tubo_carcasa"),
    path('tubo_carcasa/crear/', CrearIntercambiadorTuboCarcasa.as_view(),name="crear_tubo_carcasa"),
    path('tubo_carcasa/editar/<int:pk>/', EditarIntercambiadorTuboCarcasa.as_view(),name="editar_tubo_carcasa"),
    path('tubo_carcasa/<int:pk>/evaluar/', CrearEvaluacionTuboCarcasa.as_view(),name="crear_evaluacion_tubo_carcasa"),

    # RUTAS PARA DOBLE TUBO
    path('doble_tubo/', ConsultaDobleTubo.as_view(), name="consulta_doble_tubo"),

    # RUTAS DE CONSULTAS DE FLUIDOS
    path('consultar_cas/', ConsultaCAS.as_view(), name="consultar_cas"),
    path('calcular_cp/', ConsultaCP.as_view(), name="consultar_cp"),
    path('evaluar/tubo_carcasa/<int:pk>/', EvaluarTuboCarcasa.as_view(), name="evaluar_tubo_carcasa"),
    path('evaluar/tubo_carcasa/grafica/<int:pk>/', ConsultaGraficasEvaluacion.as_view(), name="evaluar_tubo_carcasa"),

    # RUTAS AJAX PARA VALIDACIÓN DE DATOS
    path('validar_cdf_existente/',ValidarCambioDeFaseExistente.as_view(), name="validar_cdf_existente"),
    path('validar_cdf_existente_ev/<int:pk>/',ValidarCambioDeFaseExistenteEvaluacion.as_view(), name="validar_cdf_existente_ev"),
]
