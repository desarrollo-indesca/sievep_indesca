from django.urls import path
from .views import *

urlpatterns = [
    path('', ConsultaCalderas.as_view(), name="consulta_calderas"),
]