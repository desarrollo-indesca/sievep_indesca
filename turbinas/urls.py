from django.urls import path
from .views import *

urlpatterns = [
    path('vapor/', ConsultaTurbinasVapor.as_view(), name="consulta_turbinas_vapor"),
    path('vapor/creacion/', CreacionTurbinaVapor.as_view(), name="creacion_turbina_vapor"),
    path('vapor/edicion/<int:pk>', EdicionTurbinaVapor.as_view(), name="edicion_turbina_vapor")
]