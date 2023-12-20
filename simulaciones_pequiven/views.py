from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, get_user_model
from django.http import HttpResponse
from intercambiadores.models import Fluido, Unidades, TiposDeTubo, Tema, Intercambiador, PropiedadesTuboCarcasa, CondicionesIntercambiador
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django import template
from django.utils.http import urlencode

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)

class Bienvenida(View):
    context = {
        'titulo': "SIEVEP"
    }
    
    def get(self, request):
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
            self.context['errores'] = 'Usuario no encontrado.'
            return redirect('/')
        else:
            if user.check_password(password):
                user = user
            else:
                user = None
            
        if user and user.is_active:
            login(request, user)
            if(self.context.get('errores')):
                del(self.context['errores'])

            return redirect('/')
        elif(user and not user.is_active):
            self.context['errores'] = 'Usuario inactivo.'            
        else:
            self.context['errores'] = 'Datos Incorrectos.'
            return redirect('/')
        
class CerrarSesion(LoginRequiredMixin, View):
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

# Carga de Intercambiadores -- Vista temporal para carga de intercambiadores. Actualmente dará error.
class ComponerIntercambiadores(View):
    def get(self, request):
        import csv, random
        from intercambiadores.models import TipoIntercambiador, Planta
        from intercambiadores.views import calcular_cp
        with open('./intercambiadores.csv','r') as file:
            csvreader = csv.reader(file, delimiter=";")
            for row in csvreader:
                for n,col in enumerate(row):
                    if(col == '*' or col == '-' or col == '/' or col == 'NIL'):
                        row[n] = ''
                    
                if(row[0] == 'AMC' and row[1] == 'OLEFINAS I'):
                    row[0] = Planta.objects.get(pk=1)
                elif(row[0] == 'AMC' and row[1] == 'OLEFINAS II'):
                    row[0] = Planta.objects.get(pk=1)
                
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
                except Exception as e:
                    print(str(e))
                    print(f"SKIP {row[2]}")
                    continue
                
                row[9] = float(row[9].replace(',','.')) if len(row[9]) else 0
                row[10] = float(row[10].replace(',','.')) if len(row[10]) else 0
                row[11] = float(row[11].replace(',','.')) if len(row[11]) else 0
                row[12] = float(row[12].replace(',','.')) if len(row[12]) else 0

                row[13] = 'P' if 'Parcial' in row[13] else 'S' if 'Sin' in row[13] else 'T'
                row[14] = float(row[14].replace(',','.')) if len(row[14]) else ''
                row[15] = float(row[15].replace(',','.')) if len(row[15]) else ''
                row[16] = float(row[16].replace(',','.')) if len(row[16]) else ''
                row[17] = float(row[17].replace(',','.')) if len(row[17]) else ''
                
                row[22] = float(row[22].replace(',','.')) if len(row[22]) else 0
                row[23] = float(row[23].replace(',','.')) if len(row[23]) else 0
                row[24] = float(row[24].replace(',','.')) if len(row[24]) else 0
                row[25] = float(row[25].replace(',','.')) if len(row[25]) else 0

                row[26] = 'P' if 'Parcial' in row[26] else 'S' if 'Sin' in row[26] else 'T'
                row[27] = float(row[27].replace(',','.')) if len(row[27]) else ''
                row[28] = float(row[28].replace(',','.')) if len(row[28]) else ''
                row[29] = float(row[29].replace(',','.')) if len(row[29]) else ''
                row[30] = float(row[30].replace(',','.')) if len(row[30]) else ''

                # 31 Ensuciamiento

                row[32] = float(row[32].replace(',','.')) if len(row[32]) else ''

                # 33 U

                print(row[35])
                row[34] = float(row[34].replace(',','.')) if len(row[34]) else ''
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
                    row[51] = Tema.objects.create(codigo = row[51].upper())

                # Fluidos (Caso Especial) 5,18
                etiqueta_carcasa = None

                if(Fluido.objects.filter(nombre = row[5].upper()).exists()):
                    row[5] = Fluido.objects.get(nombre = row[5].upper())
                    cp_carcasa = calcular_cp(row[5].cas, row[6]+273.15, row[7]+273.15)
                elif(row[5] == 'Vapor' or 'AGUA' in row[5].upper()):
                    row[5] = Fluido.objects.get(nombre = 'AGUA')
                    cp_carcasa = calcular_cp(row[5].cas, row[6]+273.15, row[7]+273.15)
                else:
                    bandera = False
                    for fluido in Fluido.objects.all():
                        if(fluido.nombre.upper() in row[5].upper()):
                            row[5] = fluido
                            bandera = True
                            break
                    if not bandera:
                        etiqueta_carcasa = row[5].upper()
                        cp_carcasa = random.uniform(-500, 500)

                etiqueta_tubo = None
                if(Fluido.objects.filter(nombre = row[18].upper()).exists()):
                    row[18] = Fluido.objects.get(nombre = row[18].upper())
                    cp_tubo = calcular_cp(row[18].cas, row[19]+273.15, row[20]+273.15)
                elif(row[18] == 'Vapor' or 'AGUA' in row[18].upper()):
                    row[18] = Fluido.objects.get(nombre = 'AGUA')
                    cp_tubo = calcular_cp(row[18].cas, row[19]+273.15, row[20]+273.15)
                else:
                    bandera = False
                    for fluido in Fluido.objects.all():
                        if(fluido.nombre.upper() in row[18].upper()):
                            row[18] = fluido
                            cp_tubo = calcular_cp(row[18].cas, row[19]+273.15, row[20]+273.15)
                            bandera = True
                            break
                    if not bandera:
                        etiqueta_tubo = row[18].upper()
                        cp_tubo = random.uniform(-500, 500)

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
                            diametro_externo_tubos = float(row[-15]),
                            diametro_interno_carcasa = float(row[-14]),
                            diametro_tubos_unidad = Unidades.objects.get(pk=5),
                            fluido_carcasa = row[5] if type(row[5]) == Fluido else None,
                            material_carcasa = row[-13],
                            conexiones_entrada_carcasa = row[-9],
                            conexiones_salida_carcasa = row[-8],
                            numero_tubos = row[35],

                            material_tubo = row[-12],
                            fluido_tubo = row[18] if type(row[18]) == Fluido else None,
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

                        condiciones_tubo = CondicionesIntercambiador.objects.create(
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
                            fluido_cp = cp_tubo,
                            fluido_etiqueta = etiqueta_tubo,

                            cambio_de_fase = row[26],

                            presion_entrada = row[27],
                            caida_presion_max = row[28],
                            caida_presion_min = row[29],
                            unidad_presion = Unidades.objects.get(pk=7), 

                            fouling = row[30],
                        )

                        condiciones_carcasa = CondicionesIntercambiador.objects.create(
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
                            fluido_cp = cp_carcasa,
                            fluido_etiqueta = etiqueta_carcasa,

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

# Carga de Temas -- Vista Temporal
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

# Carga de Fluidos -- Vista Temporal
class ComponerFluidos(View):
    def get(self, request):
        import csv
        from intercambiadores.models import Fluido
        with open('./fluidos.csv','r', encoding='Latin1') as file:
            csvreader = csv.reader(file, delimiter=";")
            for row in csvreader:
                if(not Fluido.objects.filter(cas=row[2]).exists()):
                    Fluido.objects.create(
                        nombre = row[1],
                        cas = row[2]
                    )
        
        return HttpResponse("Listo")