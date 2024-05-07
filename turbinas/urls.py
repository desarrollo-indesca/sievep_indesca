from django.urls import path
from .views import *

urlpatterns = [
    path('turbinas/vapor/', ConsultaTurbinasVapor.as_view(), name="consulta_turbinas_vapor"),
]