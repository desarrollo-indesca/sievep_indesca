from django.urls import path
from .views import *

urlpatterns = [
    path('', ConsultaCompresores.as_view(), name="consulta_compresores"),
    path('duplicar/<int:pk>/', DuplicarCompresores.as_view(), name="duplicar_compresores"),
    path('ficha/<int:pk>/', ProcesarFichaSegunCaso.as_view(), name="ficha_caso"),
    
    path('crear/', CreacionCompresor.as_view(), name="creacion_compresor"),
    path('crear-caso/<int:pk>/', CreacionNuevoCaso.as_view(), name="creacion_nuevo_caso"),
    path('edicion-etapas/<int:pk>/', EdicionEtapa.as_view(), name="edicion_etapa"),

    path('editar/<int:pk>/', EdicionCompresor.as_view(), name="edicion_compresor"),
]