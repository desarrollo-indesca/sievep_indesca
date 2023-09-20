from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, get_user_model
from django.http import HttpResponse
from intercambiadores.models import Fluido, Unidades, TiposDeTubo, Tema, Intercambiador, PropiedadesTuboCarcasa, CondicionesTuboCarcasa
from django.db import transaction

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

# Esta vista es temporal. Fue usada para cargar los datos de los fluidos 
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

            return HttpResponse("CREADO EXITOSAMENTE")

# Carga de Intercambiadores (Revisión)
class ComponerIntercambiadores(View):
    def get(self, request):
        import csv
        from intercambiadores.models import TipoIntercambiador, Planta
        with open('./intercambiadores.csv','r') as file:
            csvreader = csv.reader(file, delimiter=";")
            for row in csvreader:
                print(row)
                for n,col in enumerate(row):
                    if(col == '*' or col == '-' or col == '/' or col == 'NIL'):
                        row[n] = ''
                    
                if(row[0] == 'AMC' and row[1] == 'OLEFINAS I'):
                    row[0] = Planta.objects.get(pk=1)
                elif(row[0] == 'AMC' and row[1] == 'OLEFINAS II'):
                    # row[0] = Planta.objects.get(pk=1)
                    continue
                
                row[4] = TipoIntercambiador.objects.get(pk=1)

                # Temperaturas de Entrada, Salida y Flujo Másico
                try:
                    row[6] = float(row[6].replace(',','.'))
                    row[7] = float(row[7].replace(',','.'))
                    row[8] = float(row[8].replace(',','.'))
                    row[19] = float(row[19].replace(',','.'))
                    row[20] = float(row[20].replace(',','.'))
                    row[21] = float(row[21].replace(',','.'))
                    row[35] = float(row[35].replace(',','.'))
                except:
                    continue
                
                row[9] = float(row[9].replace(',','.')) if len(row[9]) else ''
                row[10] = float(row[10].replace(',','.')) if len(row[10]) else ''
                row[11] = float(row[11].replace(',','.')) if len(row[11]) else ''
                row[12] = float(row[12].replace(',','.')) if len(row[12]) else ''

                row[13] = 'P' if 'Parcial' in row[13] else 'S' if 'Sin' in row[13] else 'T'
                row[14] = float(row[14].replace(',','.')) if len(row[14]) else ''
                row[15] = float(row[15].replace(',','.')) if len(row[15]) else ''
                row[16] = float(row[16].replace(',','.')) if len(row[16]) else ''
                row[17] = float(row[17].replace(',','.')) if len(row[17]) else ''
                
                row[22] = float(row[22].replace(',','.')) if len(row[22]) else ''
                row[23] = float(row[23].replace(',','.')) if len(row[23]) else ''
                row[24] = float(row[24].replace(',','.')) if len(row[24]) else ''
                row[25] = float(row[25].replace(',','.')) if len(row[25]) else ''

                row[26] = 'P' if 'Parcial' in row[26] else 'S' if 'Sin' in row[26] else 'T'
                row[27] = float(row[27].replace(',','.')) if len(row[27]) else ''
                row[28] = float(row[28].replace(',','.')) if len(row[28]) else ''
                row[29] = float(row[29].replace(',','.')) if len(row[29]) else ''
                row[30] = float(row[30].replace(',','.')) if len(row[30]) else ''

                # 31 Ensuciamiento

                row[32] = float(row[32].replace(',','.')) if len(row[32]) else ''

                # 33 U

                row[34] = float(row[34].replace(',','.')) if len(row[34]) else ''
                # row[35] = float(row[35].replace(',','.')) if  len(row[35]) else ''
                row[36] = float(row[36].replace(',','.')) if len(row[36]) else ''
                row[37] = float(row[37].replace(',','.')) if len(row[37]) else ''
                row[38] = float(row[38].replace(',','.')) if len(row[38]) else ''
                
                if(not TiposDeTubo.objects.filter(nombre__icontains = row[45]).exists()):
                    row[45] = TiposDeTubo.objects.create(nombre = row[45])
                else:
                    row[45] = TiposDeTubo.objects.filter(nombre__icontains = row[45]).first()

                row[46] = float(row[46].replace(',','.')) if len(row[46]) else ''
                row[48] = 'S' if 'Semi' in row[48] else 'N' if 'N' in row[48] else 'C'  

                try:
                    row[51] = Tema.objects.get(codigo = row[51])
                except:
                    row[51] = Tema.objects.get(pk=8) 

                # Fluidos (Caso Especial) 5,18
                for x in Fluido.objects.all():
                    if(x.nombre.lower() in row[5].lower()):
                        if(Fluido.objects.filter(nombre__icontains = x.nombre).count() > 1):
                            try:
                                if(row[9] > row[11]):
                                    row[5] = Fluido.objects.filter(nombre__icontains = x.nombre, estado = 'G').first()
                                else:
                                    row[5] = Fluido.objects.filter(nombre__icontains = x.nombre, estado = 'L').first()
                            except:
                                if(row[9] == ''):
                                    row[5] = Fluido.objects.filter(nombre__icontains = x.nombre, estado = 'L').first()
                                else:
                                    row[5] = Fluido.objects.filter(nombre__icontains = x.nombre, estado = 'G').first()
                        else:
                            row[5] = x
                        break
                    elif(x.formula != '' and x.formula.lower() in row[5].lower()):
                        if(Fluido.objects.filter(formula__icontains = x.formula).count() > 1):
                            try:
                                if(row[9] > row[11]):
                                    row[5] = Fluido.objects.filter(formula__icontains = x.formula, estado = 'G').first()
                                else:
                                    row[5] = Fluido.objects.filter(formula__icontains = x.formula, estado = 'L').first()
                            except:
                                if(row[9] is str):
                                    row[5] = Fluido.objects.filter(formula__icontains = x.formula, estado = 'L').first()
                                else:
                                    row[5] = Fluido.objects.filter(formula__icontains = x.formula, estado = 'G').first()
                        else:
                            row[5] = x
                        break

                if(row[5] == 'Vapor'):
                    row[5] = Fluido.objects.get(nombre = 'AGUA', estado = 'G')
                
                if(type(row[5]) == str):
                    if(type(row[9]) == float and type(row[11]) == float):
                        Fluido.objects.create(
                            nombre = row[5],
                            estado = 'G' if float(row[9]) > float(row[11]) else 'L',
                            formula = ''
                        )
                    elif(type(row[9]) == str and not len(row[9])):
                        Fluido.objects.create(
                            nombre = row[5],
                            estado = 'L',
                            formula = ''
                        )
                    else:
                        Fluido.objects.create(
                            nombre = row[5],
                            estado = 'G',
                            formula = ''
                        )

                for x in Fluido.objects.all():
                    if(x.nombre.lower() in row[18].lower()):
                        print("FLUIDO")
                        if(Fluido.objects.filter(nombre__icontains = x.nombre).count() > 1):
                            try:
                                if(row[19] > row[21]):
                                    row[18] = Fluido.objects.filter(nombre__icontains = x.nombre, estado = 'G').first()
                                else:
                                    row[18] = Fluido.objects.filter(nombre__icontains = x.nombre, estado = 'L').first()
                            except:
                                if(row[19] == ''):
                                    row[18] = Fluido.objects.filter(nombre__icontains = x.nombre, estado = 'L').first()
                                else:
                                    row[18] = Fluido.objects.filter(nombre__icontains = x.nombre, estado = 'G').first()
                        else:
                            row[18] = x
                        break
                    elif(x.formula != '' and x.formula.lower() in row[18].lower()):
                        print("FORMULA")
                        if(Fluido.objects.filter(formula__icontains = x.formula).count() > 1):
                            try:
                                if(row[19] > row[21]):
                                    row[18] = Fluido.objects.filter(formula__icontains = x.formula, estado = 'G').first()
                                else:
                                    row[18] = Fluido.objects.filter(formula__icontains = x.formula, estado = 'L').first()
                            except:
                                if(row[19] is str):
                                    row[18] = Fluido.objects.filter(formula__icontains = x.formula, estado = 'L').first()
                                else:
                                    row[18] = Fluido.objects.filter(formula__icontains = x.formula, estado = 'G').first()
                        else:
                            row[18] = x
                        break

                if(row[18] == 'Vapor'):
                    row[18] = Fluido.objects.get(nombre = 'AGUA', estado = 'G')
                
                if(type(row[18]) == str):
                    if(type(row[19]) == float and type(row[21]) == float):
                        Fluido.objects.create(
                            nombre = row[18],
                            estado = 'G' if float(row[19]) > float(row[21]) else 'L',
                            formula = ''
                        )
                    elif(type(row[19]) == str and not len(row[19])):
                        Fluido.objects.create(
                            nombre = row[18],
                            estado = 'L',
                            formula = ''
                        )
                    else:
                        Fluido.objects.create(
                            nombre = row[18],
                            estado = 'G',
                            formula = ''
                        )
                
                try:
                    with transaction.atomic():
                        intercambiador = Intercambiador.objects.create(
                            tag = row[2],
                            tipo = row[4],
                            fabricante = row[-5],
                            planta = Planta.objects.get(nombre = row[1]),
                            tema = row[-1],
                            servicio = row[3],
                            arreglo_flujo = 'C' # PREGUNTAR
                        )

                        propiedades = PropiedadesTuboCarcasa.objects.create(
                            intercambiador = intercambiador,
                            area = row[-18],
                            area_unidad = Unidades.objects.get(pk=3),
                            longitud_tubos = row[-16],
                            longitud_tubos_unidad = Unidades.objects.get(pk=4),
                            diametro_externo_tubos = row[-15],
                            diametro_interno_tubos = row[-14],
                            diametro_tubos_unidad = Unidades.objects.get(pk=5),
                            fluido_carcasa = row[5],
                            material_carcasa = row[-13],
                            conexiones_entrada_carcasa = row[-9],
                            conexiones_salida_carcasa = row[-8],
                            numero_pasos = 1,

                            material_tubo = row[-12],
                            fluido_tubo = row[18],
                            tipo_tubo = row[-7],
                            conexiones_entrada_tubos =row[-11],
                            conexiones_salida_tubos = row[-10],
                            pitch_tubos = row[-6],
                            unidades_pitch = Unidades.objects.get(pk=5),

                            criticidad = row[-4],
                            arreglo_serie = row[-3],
                            arreglo_paralelo = row[-2],
                            q = row[32]
                        )

                        condiciones_tubo = CondicionesTuboCarcasa.objects.create(
                            intercambiador = propiedades,
                            lado = 'T',
                            temp_entrada = row[19],
                            temp_salida = row[20],
                            temperaturas_unidad = Unidades.objects.get(pk=1),

                            flujo_masico = row[21],
                            flujo_vapor_entrada = row[22],
                            flujo_vapor_salida = row[23],
                            flujo_liquido_entrada = row[24],
                            flujo_liquido_salida = row[25],
                            flujos_unidad = Unidades.objects.get(pk=6),

                            cambio_de_fase = row[26],

                            presion_entrada = row[27],
                            caida_presion_max = row[28],
                            caida_presion_min = row[29],
                            unidad_presion = Unidades.objects.get(pk=7), 

                            fouling = row[30],
                        )

                        condiciones_carcasa = CondicionesTuboCarcasa.objects.create(
                            intercambiador = propiedades,
                            lado = 'C',
                            temp_entrada = row[6],
                            temp_salida = row[7],
                            temperaturas_unidad = Unidades.objects.get(pk=1),

                            flujo_masico = row[8],
                            flujo_vapor_entrada = row[9],
                            flujo_vapor_salida = row[10],
                            flujo_liquido_entrada = row[11],
                            flujo_liquido_salida = row[12],
                            flujos_unidad = Unidades.objects.get(pk=6),

                            cambio_de_fase = row[13],

                            presion_entrada = row[14],
                            caida_presion_max = row[15],
                            caida_presion_min = row[16],
                            unidad_presion = Unidades.objects.get(pk=7), 

                            fouling = row[17],
                        )
                except Exception as e:
                    print(str(e))
                    continue
            return HttpResponse("Listo")

# Carga de Temas
class ComponerTemas(View):
    def get(self, request):
        import csv
        from intercambiadores.models import Tema
        with open('./intercambiadores_tubocarcasa.csv','r') as file:
            csvreader = csv.reader(file, delimiter=";")
            for row in csvreader:
                print(row[2])
                if(not Tema.objects.filter(codigo=row[-2]).exists()):
                    Tema.objects.create(
                        codigo = row[-2],
                        descripcion = row[-1]
                    )
        
        return HttpResponse("Listo")