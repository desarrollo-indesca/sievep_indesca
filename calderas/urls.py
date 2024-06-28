from django.urls import path
from .views import *

urlpatterns = [
    path('', ConsultaCalderas.as_view(), name="consulta_calderas"),
    path('creacion/', CreacionCaldera.as_view(), name="creacion_caldera"),
    path('edicion/<int:pk>/', EdicionCaldera.as_view(), name="edicion_caldera"),
]