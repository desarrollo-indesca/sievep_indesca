from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, get_user_model
from django.http import HttpResponse
from intercambiadores.models import Fluido, Unidades

class Bienvenida(View):
    context = {
        'titulo': "PEQUIVEN - Simulaciones"
    }
    
    def get(self, request):
        print(request.user)
        if(request.user.is_authenticated):
            return render(request, 'bienvenida.html', context=self.context)
        else:
            return render(request, 'usuarios/login.html', context=self.context)
        
    def post(self, request):
        username = request.POST["email"]
        password = request.POST["password"]
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                user = user
            else:
                user = None
            
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            self.context['errores'] = 'Datos Incorrectos.'
            return redirect('/')
        
class CerrarSesion(View):
    def get(self, request):
        logout(request)
        return redirect('/')
    
class ComponerFluidos(View):
    def get(self, request):
        import csv
        with open('./fluidos.csv','r') as file:
            csvreader = csv.reader(file, delimiter=";")
            for row in csvreader:
                print(row)
                Fluido.objects.create(
                    nombre = row[0],
                    formula = row[1],
                    peso_molecular = row[2].replace(",","."),
                    estado= row[3],
                    unidad_temperatura = Unidades.objects.get(pk=1) if row[4] == 'C' else Unidades.objects.get(pk=2),
                    a = float(row[5].replace(",",".")), b = float(row[6].replace(",",".")),
                    c = float(row[7].replace(",",".")), d = float(row[8].replace(",",".")[:row[8].index('E')])*10**int(row[8][row[8].index('E')+1:]) if 'E' in row[8] else row[8].replace(',','.'),
                    minimo = row[9] if len(row[9]) else -255, maximo = row[10] if len(row[10]) else 1000,
                )

            return HttpResponse("A")