"""
URL configuration for simulaciones_pequiven project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Bienvenida.as_view(), name='bienvenida'),
    path('logout/', CerrarSesion.as_view(), name='cerrar_sesion'),
    path('intercambiadores/', include('intercambiadores.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('', include('pwa.urls')),
    path('migrar/intercambiadores/',ComponerIntercambiadores.as_view(), name="migrar_intercambiadores"),
    path('migrar/fluidos/',ComponerFluidos.as_view(), name="migrar_intercambiadores"),
    path('manual/', ManualDeUsuario.as_view(), name="manual"),
    # path("__debug__/", include("debug_toolbar.urls")),
]