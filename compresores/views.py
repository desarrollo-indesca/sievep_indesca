from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Prefetch
from simulaciones_pequiven.views import FiltradoSimpleMixin, DuplicateView
from .models import *
from reportes.pdfs import generar_pdf
from reportes.xlsx import reporte_equipos

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

class ReportesFichasCompresoresMixin():
    '''
    Resumen:
        Mixin para evitar la repetición de código al generar fichas técnicas en las vistas que lo permiten.
        También incluye lógica para la generación de la ficha de los parámetros de instalación.
    '''
    def reporte_ficha(self, request):
        if(request.POST.get('ficha')): # FICHA TÉCNICA
            caldera = Caldera.objects.get(pk = request.POST.get('ficha'))
            if(request.POST.get('tipo') == 'pdf'):
                return generar_pdf(request,caldera, f"Ficha Técnica de la Caldera {caldera.tag}", "ficha_tecnica_caldera")
            if(request.POST.get('tipo') == 'xlsx'):
                return ficha_tecnica_caldera(caldera, request)

# Create your views here.

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


class DuplicarCaldera(CargarCompresorMixin, DuplicateView):
    """
    Resumen:
        Vista para crear una copia temporal duplicada de una caldera para hacer pruebas en los equipos.
    """

    def post(self, request, pk):
        compresor_original = Compresor.objects.select_related(
            "sobrecalentador", "sobrecalentador__dims", "tambor",
            "dimensiones", "especificaciones", "combustible", 
            "chimenea", "economizador"
        ).prefetch_related(
            "tambor__secciones_tambor", "combustible__composicion_combustible_caldera",
            "caracteristicas_caldera", "corrientes_caldera"
        ).get(pk=pk)

        if(self.request.user.is_superuser or PlantaAccesible.objects.filter(usuario = request.user, planta = caldera_original.planta, duplicacion = True).exists()):
            caldera = caldera_original
            caldera.copia = True
            caldera.tag = generate_nonexistent_tag(Caldera, caldera.tag)
            dims = self.copy(caldera_original.sobrecalentador.dims)
            sobrecalentador = caldera_original.sobrecalentador
            sobrecalentador.dims = dims
            caldera.sobrecalentador = self.copy(caldera_original.sobrecalentador)
            caldera.tambor = self.copy(caldera_original.tambor)
            caldera.dimensiones = self.copy(caldera_original.dimensiones)
            caldera.especificaciones = self.copy(caldera_original.especificaciones)
            caldera.chimenea = self.copy(caldera_original.chimenea)
            caldera.economizador = self.copy(caldera_original.economizador)
            caldera.combustible = self.copy(caldera_original.combustible)
            caldera.descripcion = f"COPIA DE LA CALDERA {caldera_original.tag}"
            caldera = self.copy(caldera)

            for caracteristica in caldera_original.caracteristicas_caldera.all():
                caracteristica.caldera = caldera
                self.copy(caracteristica)

            for seccion in caldera_original.tambor.secciones_tambor.all():
                seccion.tambor = caldera.tambor
                self.copy(seccion)

            for corriente in caldera_original.corrientes_caldera.all():
                corriente.caldera = caldera
                self.copy(corriente)

            for compuesto in caldera_original.combustible.composicion_combustible_caldera.all():
                compuesto.combustible = caldera.combustible
                self.copy(compuesto)

            caldera_original = Caldera.objects.get(pk=pk)
            messages.success(request, f"Se ha creado la copia de la caldera {caldera_original.tag} como {caldera.tag}. Recuerde que todas las copias serán eliminadas junto a sus datos asociados al día siguiente a las 7:00am.")
            return redirect("/calderas")
        else:
            return HttpResponseForbidden()