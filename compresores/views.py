from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View
from django.db.models import Prefetch
from django.http import HttpResponseForbidden
from django.db import transaction
from simulaciones_pequiven.views import FiltradoSimpleMixin, DuplicateView
from simulaciones_pequiven.utils import generate_nonexistent_tag
from usuarios.models import PlantaAccesible
from .models import *
from .forms import *
from reportes.pdfs import generar_pdf
from reportes.xlsx import reporte_equipos, ficha_tecnica_compresor
from django.contrib import messages

class ReportesFichasCompresoresMixin():
    '''
    Resumen:
        Mixin para evitar la repetición de código al generar fichas técnicas en las vistas que lo permiten.
        También incluye lógica para la generación de la ficha de los parámetros de instalación.
    '''
    def reporte_ficha(self, request):
        if(request.POST.get('ficha')): # FICHA TÉCNICA
            compresor = Compresor.objects.get(pk = request.POST.get('ficha'))
            if(request.POST.get('tipo') == 'pdf'):
                return generar_pdf(request,compresor, f"Ficha Técnica del Compresor {compresor.tag}", "ficha_tecnica_compresor")
            if(request.POST.get('tipo') == 'xlsx'):
                return ficha_tecnica_compresor(compresor, request)

class CargarCompresorMixin():
    """
    Resumen:
        Mixin para optimizar las consultas de compresores.
    """

    def get_compresor(self, prefetch = True, queryset = True):
        if(not queryset):
            if(self.kwargs.get('pk')):
                compresor = Compresor.objects.filter(pk = self.kwargs['pk'])
            else:
                compresor = Compresor.objects.none()
        else:
            compresor = queryset

        if(prefetch):
            compresor = compresor.select_related(
                'creado_por', 'editado_por', 'planta'
            ).prefetch_related(
                Prefetch(
                    'casos', PropiedadesCompresor.objects.select_related(
                        'tipo_lubricacion', 
                        'unidad_potencia', 
                        'unidad_velocidad'
                    ).prefetch_related(
                        Prefetch(
                            'etapas',
                            EtapaCompresor.objects.select_related(
                                'flujo_masico_unidad',
                                'flujo_molar_unidad',
                                'densidad_unidad',
                                'potencia_unidad',
                                'cabezal_unidad',
                                'volumen_unidad'
                            ).prefetch_related(
                                Prefetch(
                                    'lados',
                                    LadoEtapaCompresor.objects.select_related(
                                        'temp_unidad',
                                        'presion_unidad'
                                    )
                                )
                            )
                        )
                    )
                )
            )
        
        if(not queryset):
            if(compresor):
                return compresor[0]

        return compresor

class ConsultaCompresores(FiltradoSimpleMixin, ReportesFichasCompresoresMixin, CargarCompresorMixin, LoginRequiredMixin, ListView):
    '''
    Resumen:
        Vista para la consulta de los compresores.
        Hereda de ListView.
        Hereda del Mixin para optimizar consultas.
        Pueden acceder usuarios que hayan iniciado sesión.
        Se puede generar una ficha del equipo a través de esta vista.

    Atributos:
        model: Model -> Modelo del cual se extraerán los elementos de la lista.
        template_name: str -> Plantilla a renderizar
        paginate_by: str -> Número de elementos a mostrar a a la vez
        titulo: str -> Título de la vista

    Métodos:
        post(self, request, *args, **kwargs) -> HttpResponse
            Se utiliza para la generación de reportes de ficha o de compresores.

        get_context_data(self, **kwargs) -> dict
            Genera el contexto necesario en la vista para la renderización de la plantilla

        get_queryset(self) -> QuerySet
            Obtiene el QuerySet de la lista de acuerdo al modelo del atributo.
            Hace el filtrado correspondiente y prefetching necesario para reducir las queries.
    '''
    model = Compresor
    template_name = 'compresores/consulta.html'
    paginate_by = 10
    titulo = "SIEVEP - Consulta de Compresores"

    def post(self, request, *args, **kwargs):
        reporte_ficha = self.reporte_ficha(request)
        if(reporte_ficha): # Si se está deseando generar un reporte de ficha, se genera
            return reporte_ficha
        
        print(request.POST)

        if(request.POST.get('tipo') == 'pdf'): # Reporte de turbinas de vapor en PDF
            return generar_pdf(request, self.get_queryset(), 'Reporte de Listado de Compresores', 'compresores')
        
        if(request.POST.get('tipo') == 'xlsx'): # reporte de turbinas de vapor en XLSX
            return reporte_equipos(request, self.get_queryset(), 'Listado de Compresores', 'listado_compresores')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["permisos"] = {
            'creacion': self.request.user.is_superuser or self.request.user.usuario_planta.filter(crear = True).exists(),
            'ediciones':list(self.request.user.usuario_planta.filter(edicion = True).values_list('planta__pk', flat=True)),
            'instalaciones':list(self.request.user.usuario_planta.filter(edicion_instalacion = True).values_list('planta__pk', flat=True)),
            'duplicaciones':list(self.request.user.usuario_planta.filter(duplicacion = True).values_list('planta__pk', flat=True)),
            'evaluaciones': list(self.request.user.usuario_planta.filter(ver_evaluaciones = True).values_list('planta__pk', flat=True)),
        }

        return context

    def get_queryset(self):        
        new_context = self.get_compresor(True, self.filtrar_equipos())

        return new_context

class DuplicarCompresores(CargarCompresorMixin, DuplicateView):
    """
    Resumen:
        Vista para crear una copia temporal duplicada de una compresor para hacer pruebas en los equipos.
    """

    def post(self, request, pk):
        compresor_original = Compresor.objects.select_related(
            'creado_por', 'editado_por', 'planta'
        ).prefetch_related(
            "casos", "casos__etapas", "casos__etapas__lados",
            "casos__etapas__composiciones"
        ).get(pk=pk)

        if(self.request.user.is_superuser or PlantaAccesible.objects.filter(usuario = request.user, planta = compresor_original.planta, duplicacion = True).exists()):
            compresor = compresor_original
            compresor.tag = generate_nonexistent_tag(Compresor, compresor.tag)
            compresor.descripcion = f"COPIA DEL COMPRESOR {compresor_original.tag}"
            compresor = self.copy(compresor)

            for caso in compresor_original.casos.all():
                caso.compresor = compresor
                for etapa in caso.etapas.all():
                    etapa.caso = caso
                    for lado in etapa.lados.all():
                        lado.etapa = etapa
                        self.copy(lado)
                    
                    for compuesto in etapa.composiciones.all():
                        compuesto.etapa = etapa
                        self.copy(compuesto)
                    
                    self.copy(etapa)
                self.copy(caso)

            compresor_original = Compresor.objects.get(pk=pk)
            messages.success(request, f"Se ha creado la copia de la compresor {compresor_original.tag} como {compresor.tag}. Recuerde que todas las copias serán eliminadas junto a sus datos asociados al día siguiente a las 7:00am.")
            return redirect("/compresores")
        else:
            return HttpResponseForbidden()
        
class ProcesarFichaSegunCaso(CargarCompresorMixin, View):
    template_name = 'compresores/partials/ficha_caso.html'

    def get(self, request, pk, *args, **kwargs):
        caso = request.GET.get('caso')

        return render(
            request,
            self.template_name,
            context={
                'caso': self.get_compresor(
                    True, 
                    Compresor.objects.filter(pk=pk)
                ).first().casos.get(pk=caso),
                'compresor': Compresor.objects.get(pk=pk)
            }
        )

class CreacionCompresor(LoginRequiredMixin, View):
    template_name = 'compresores/creacion.html'

    def almacenar_datos(self, form_compresor, form_caso):
        try:
            form_compresor.is_valid()
            form_caso.is_valid()
            with transaction.atomic():
                if(form_compresor.is_valid()):
                    form_compresor.instance.creado_por = self.request.user
                    form_compresor.instance.creado_al = self.request.user      
                    form_compresor.save()
                else:
                    print(form_compresor.errors)
                    raise Exception("Información Inválida.")

                if form_caso.is_valid():
                    form_caso.instance.compresor = form_compresor.instance
                    form_caso.save()

                    numero_etapas = form_compresor.cleaned_data.get('numero_etapas', 0)
                    for i in range(1, numero_etapas + 1):
                        etapa = EtapaCompresor(compresor=form_caso.instance, numero=i)
                        etapa.save()
                else:
                    print(form_caso.errors)
                    raise Exception("Información Inválida.")
                
            messages.success(self.request, "Información almacenada correctamente.")
            return redirect('/compresores/')
        except Exception as e:
            print(str(e))
            return render(self.request, self.template_name, {
                'unidades': Unidades.objects.all().values(),
                'form_compresor': form_compresor,
                'form_caso': form_caso,
                'titulo': "SIEVEP - Creación de Compresores"
            })

    def post(self, request, *args, **kwargs):
        form_compresor = CompresorForm(request.POST)
        form_caso = PropiedadesCompresorForm(request.POST)

        return self.almacenar_datos(form_compresor, form_caso)

    def get_context_data(self, **kwargs):
        context = {}
        context["form_compresor"]  = CompresorForm()
        context["form_caso"]  = PropiedadesCompresorForm()
        context['unidades'] = Unidades.objects.all().values()
        context['titulo'] = "SIEVEP - Creación de Compresores"

        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
    
class CreacionNuevoCaso(LoginRequiredMixin, View):
    template_name = 'compresores/creacion.html'

    def almacenar_datos(self, form_caso):
        try:
            compresor = Compresor.objects.get(pk=self.kwargs.get('pk'))
            form_caso.is_valid()
            with transaction.atomic():
                if form_caso.is_valid():
                    form_caso.instance.compresor = compresor
                    form_caso.save()

                    numero_etapas = compresor.casos.first().etapas.count()
                    for i in range(1, numero_etapas + 1):
                        etapa = EtapaCompresor(compresor=form_caso.instance, numero=i)
                        etapa.save()
                else:
                    print(form_caso.errors)
                    raise Exception("Información Inválida.")
                
            messages.success(self.request, "Información almacenada correctamente.")
            return redirect('/compresores/')
        except Exception as e:
            print(str(e))
            return render(self.request, self.template_name, {
                'unidades': Unidades.objects.all().values(),
                'form_caso': form_caso,
                'titulo': "SIEVEP - Creación de Caso de Compresor"
            })

    def post(self, request, *args, **kwargs):
        form_caso = PropiedadesCompresorForm(request.POST)
        return self.almacenar_datos(form_caso)

    def get_context_data(self, **kwargs):
        context = {}
        context["form_caso"]  = PropiedadesCompresorForm()
        context['unidades'] = Unidades.objects.all().values()
        context['titulo'] = "SIEVEP - Creación de Caso"

        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

class EdicionEtapa(LoginRequiredMixin, View):
    template_name = 'compresores/edicion_etapa.html'
    
    def almacenar_datos(self, form_etapa, form_entrada, form_salida):
        try:
            form_etapa.is_valid()
            form_entrada.is_valid()
            form_salida.is_valid()
            with transaction.atomic():
                if form_etapa.is_valid():
                    form_etapa.save()
                else:
                    print(form_etapa.errors)
                    raise Exception("Información Inválida.")
                
                if form_entrada.is_valid():
                    form_entrada.instance.etapa = form_etapa.instance
                    form_entrada.save()
                else:
                    print(form_entrada.errors)
                    raise Exception("Información Inválida Entrada.")
                
                if form_salida.is_valid():
                    form_salida.instance.etapa = form_etapa.instance
                    form_salida.save()
                else:
                    print(form_salida.errors)
                    raise Exception("Información Inválida Salida.")
                
            messages.success(self.request, "Información almacenada correctamente.")
            return redirect('/compresores/')
        except Exception as e:
            print(str(e))
            return render(self.request, self.template_name, {
                'unidades': Unidades.objects.all().values('pk', 'simbolo', 'tipo'),
                'form_etapa': form_etapa,
                'form_entrada': form_entrada,
                'form_salida': form_salida,
                'titulo': "SIEVEP - Edición de Etapa",
                "etapa": form_etapa.instance
            })

    def get_context_data(self, **kwargs):
        etapa = EtapaCompresor.objects.get(pk=self.kwargs.get('pk'))
        lado_entrada = etapa.lados.first()
        lado_salida = etapa.lados.last()

        context = {}
        context['etapa'] = etapa
        context['compresor'] = etapa.compresor.compresor
        context["form_etapa"] = EtapaCompresorForm(instance=etapa)
        context["form_entrada"] = LadoEtapaCompresorForm(instance=lado_entrada, prefix="entrada")
        context["form_salida"] = LadoEtapaCompresorForm(instance=lado_salida, prefix="salida")
        context['unidades'] = Unidades.objects.all().values('pk', 'simbolo', 'tipo')
        context['titulo'] = "SIEVEP - Edición de Etapa"

        return context
    
    def post(self, request, *args, **kwargs):
        etapa_previa = EtapaCompresor.objects.get(pk=self.kwargs.get('pk'))
        form_caso = EtapaCompresorForm(request.POST, instance=etapa_previa)
        form_entrada = LadoEtapaCompresorForm(request.POST, instance=etapa_previa.lados.first(), prefix="entrada")
        form_salida = LadoEtapaCompresorForm(request.POST, instance=etapa_previa.lados.last(), prefix="salida")
        return self.almacenar_datos(form_caso, form_entrada, form_salida)

    def get(self, request, pk, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

class EdicionCompresor(LoginRequiredMixin, View):
    template_name = "compresores/creacion.html"
    titulo = "Edición de Compresor"

    def get_context_data(self, **kwargs):
        context = {}
        compresor = Compresor.objects.get(pk=self.kwargs.get('pk'))
        context['compresor'] = compresor
        context['form_compresor'] = CompresorForm(instance=compresor, initial={
            'numero_etapas': compresor.casos.first().etapas.count()
        })
        context['titulo'] = self.titulo
        context['edicion'] = True
        return context
    
    def post(self, request, *args, **kwargs):
        compresor_previo = Compresor.objects.get(pk=self.kwargs.get('pk'))
        form = CompresorForm(request.POST, instance=compresor_previo)
        if form.is_valid():
            form.save()
            numero_etapas_previo = compresor_previo.casos.first().etapas.count()
            numero_etapas_nuevo = form.cleaned_data['numero_etapas']
            if numero_etapas_previo != numero_etapas_nuevo:
                for caso in form.instance.casos.all():
                    if numero_etapas_previo > numero_etapas_nuevo:
                        etapas_a_eliminar = caso.etapas.all()[numero_etapas_nuevo:]
                        for etapa in etapas_a_eliminar:
                            for lado in etapa.lados.all():
                                lado.delete()
                            etapa.delete()
                    elif numero_etapas_previo < numero_etapas_nuevo:
                        for i in range(numero_etapas_previo, numero_etapas_nuevo):
                            etapa = EtapaCompresor.objects.create(
                                numero=i+1,
                                compresor=caso,
                            )
                            for lado in ['entrada', 'salida']:
                                LadoEtapaCompresor.objects.create(
                                    etapa=etapa,
                                    lado=lado[0].upper()
                                )
            return redirect('/compresores/')
        else:
            return render(self.request, self.template_name, self.get_context_data())

    def get(self, request, pk, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

class EdicionCaso(EdicionCompresor):
    template_name = 'compresores/creacion.html'
    titulo = "Edición de Caso"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        compresor = self.get_object().compresor
        context['compresor'] = compresor
        context['form_caso'] = PropiedadesCompresorForm(instance=self.get_object())
        context['unidades'] = Unidades.objects.all().values('pk', 'simbolo', 'tipo')
        context['numero_caso'] = list(compresor.casos.all().values_list('pk', flat=True)).index(self.get_object().pk) + 1

        del(context['form_compresor'])
        return context

    def get_object(self):
        return PropiedadesCompresor.objects.get(pk=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        caso = self.get_object()
        form = PropiedadesCompresorForm(request.POST, instance=caso)
        if form.is_valid():
            form.save()
            return redirect('/compresores/')
        else:
            return render(self.request, self.template_name, self.get_context_data())
