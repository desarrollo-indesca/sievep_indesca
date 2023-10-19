from django.urls import path
from .views import *

urlpatterns = [
    path('', ConsultaUsuarios.as_view(), name="consultar_usuarios"),
    path('crear/', CrearNuevoUsuario.as_view(), name="crear_nuevo_usuario"),
    path('editar/<int:pk>/', EditarUsuario.as_view(), name="editar_usuario")
]
