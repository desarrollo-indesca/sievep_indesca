from django.urls import path
from .views import *

urlpatterns = [
    path('', ConsultaCompresores.as_view(), name="consulta_compresores"),
    path('duplicar/<int:pk>/', DuplicarCompresores.as_view(), name="duplicar_compresores"),
    path('ficha/<int:pk>/', ProcesarFichaSegunCaso.as_view(), name="ficha_caso")
]