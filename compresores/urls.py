from django.urls import path
from .views import *

urlpatterns = [
    path('', ConsultaCompresores.as_view(), name="consulta_compresores"),
]