from django.urls import path
from .views import *

urlpatterns = [
    path('', ConsultaUsuarios.as_view(), name="consultar_usuarios"),
    path('crear/', CrearNuevoUsuario.as_view(), name="crear_nuevo_usuario")
]
