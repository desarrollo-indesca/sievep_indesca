from django.urls import path
from .views import *

urlpatterns = [
    path('turbinas/vapor/', ConsultaTurbinasVapor.as_view(), name="consulta_turbinas_vapor"),
    path('turbinas/creacion/', CreacionTurbinaVapor.as_view(), name="creacion_turbina_vapor")
]