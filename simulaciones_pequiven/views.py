from django.views import View
from django.shortcuts import render

class Bienvenida(View):
    def get(self, request):
        return render(request, 'bienvenida.html')