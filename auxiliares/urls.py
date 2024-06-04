from django.urls import path
from .views import *

urlpatterns = [
    path('', SeleccionEquipo.as_view(), name="seleccion_equipo"),
    path('consultar_cas/', CargarFluidoNuevo.as_view(), name="consultar_cas_auxiliares"),
    path('registrar_fluido_cas/', RegistrarFluidoCAS.as_view(), name="registrar_fluido_cas_auxiliares"),

    # URLs de BOMBAS
    path('bombas/', ConsultaBombas.as_view(), name="consulta_bombas"),
    path('bombas/creacion/', CreacionBomba.as_view(), name="creacion_bomba"),
    path('bombas/edicion/<int:pk>/', EdicionBomba.as_view(), name="edicion_bomba"),
    path('bombas/instalacion/creacion/<int:pk>/', CreacionInstalacionBomba.as_view(), name="creacion_instalacion_bomba"),
    path('bombas/datos_fluido/', ObtencionDatosFluidosBomba.as_view(), name="datos_fluido_bomba"),
    path('bombas/evaluaciones/<int:pk>/', ConsultaEvaluacionBomba.as_view(), name = "evaluacion_bomba"),
    path('bombas/evaluar/<int:pk>/', CreacionEvaluacionBomba.as_view(), name = "crear_evaluacion_bomba"),

    path('bombas/evaluar/resultados/<int:pk>/', CalcularResultadosBomba.as_view(), name = "resultados_evaluacion_bombas"),
    path('bombas/evaluar/<int:pk>/historico/', GenerarGraficaBomba.as_view(), name='generar_historico_bomba'),

    # URLs de VENTILADORES
    path('ventiladores/', ConsultaVentiladores.as_view(), name="consulta_ventiladores"),
    path('ventiladores/creacion/', CreacionVentilador.as_view(), name="creacion_ventilador"),
    path('ventiladores/edicion/<int:pk>/', EdicionVentilador.as_view(), name="edicion_ventilador"),
    path('ventiladores/datos_fluido/', CalculoPropiedadesVentilador.as_view(), name="datos_fluido_ventilador"),
    path('ventiladores/evaluaciones/<int:pk>/', ConsultaEvaluacionVentilador.as_view(), name = "evaluaciones_ventilador"),
    path('ventiladores/evaluar/<int:pk>/', CreacionEvaluacionVentilador.as_view(), name='crear_evaluacion_ventilador'),
    path('ventiladores/evaluar/<int:pk>/resultado/', CalcularResultadosVentilador.as_view(), name='resultados_evaluacion_ventilador'),
    path('ventiladores/evaluaciones/<int:pk>/historico/', GenerarGraficaVentilador.as_view(), name='generar_historico_ventilador'),
]