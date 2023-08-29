from django.views import View
from django.http import HttpResponse

class Bienvenida(View):
    def get(self, request):
        return HttpResponse("Bienvenido al portal de Simulaciones PEQUIVEN")