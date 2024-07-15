from .models import *

from django.shortcuts import render, redirect
from django.db.models import Prefetch, F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View
from django.db import transaction
from django.contrib import messages

from simulaciones_pequiven.views import FiltradoSimpleMixin, ConsultaEvaluacion
from usuarios.views import SuperUserRequiredMixin 
from reportes.pdfs import generar_pdf
from reportes.xlsx import reporte_equipos
from .forms import *
from .constants import COMPUESTOS_AIRE
from .evaluacion import evaluar_caldera
from calculos.unidades import *

from datetime import datetime

# Create your views here.
class CargarCalderasMixin():
    """
    Resumen:
        Mixin para optimizar las consultas de calderas.
    """

    def get_caldera(self, prefetch = True, caldera_q = True):
        if(not caldera_q):
            if(self.kwargs.get('pk')):
                caldera = Caldera.objects.filter(pk = self.kwargs['pk'])
            else:
                caldera = Caldera.objects.none()
        else:
            caldera = caldera_q

        if(prefetch):
            caldera = caldera.select_related(
                "creado_por", "planta__complejo",
                "sobrecalentador", "sobrecalentador__temperatura_unidad",
                "sobrecalentador__presion_unidad", "sobrecalentador__flujo_unidad",
                
                "sobrecalentador__dims", "sobrecalentador__dims__area_unidad", 
                "sobrecalentador__dims__diametro_unidad",
               
                "dimensiones", "dimensiones__dimensiones_unidad",
                
                "especificaciones", "especificaciones__area_unidad",
                "especificaciones__calor_unidad", "especificaciones__capacidad_unidad",
                "especificaciones__temperatura_unidad", "especificaciones__presion_unidad",
                "especificaciones__carga_unidad",
                
                "chimenea", "chimenea__dimensiones_unidad", 
                
                "economizador", "economizador__area_unidad", "economizador__diametro_unidad",
            )
            caldera = caldera.prefetch_related(
                Prefetch("corrientes_caldera", Corriente.objects.select_related("flujo_masico_unidad",
                    "densidad_unidad", "temp_operacion_unidad", "presion_unidad")),

                Prefetch("combustible", Combustible.objects.prefetch_related(
                    Prefetch("composicion_combustible_caldera", ComposicionCombustible.objects.select_related(
                        "fluido"
                    ))
                )),

                Prefetch("caracteristicas_caldera", Caracteristica.objects.select_related(
                    'unidad'
                )),

                Prefetch("tambor", Tambor.objects.select_related("temperatura_unidad", "presion_unidad").prefetch_related(
                    Prefetch("secciones_tambor", SeccionTambor.objects.select_related("dimensiones_unidad"))
                ))
            )
        
        if(not caldera_q):
            if(caldera):
                return caldera[0]

        return caldera

class ReportesFichasCalderasMixin():
    '''
    Resumen:
        Mixin para evitar la repetición de código al generar fichas técnicas en las vistas que lo permites.
        También incluye lógica para la generación de la ficha de los parámetros de instalación.
    '''
    def reporte_ficha(self, request):
        if(request.POST.get('ficha')): # FICHA TÉCNICA
            caldera = Caldera.objects.get(pk = request.POST.get('ficha'))
            if(request.POST.get('tipo') == 'pdf'):
                return generar_pdf(request,caldera, f"Ficha Técnica de la Caldera {caldera.tag}", "ficha_tecnica_caldera")
            if(request.POST.get('tipo') == 'xlsx'):
                return ficha_tecnica_caldera(caldera, request)
            
        if(request.POST.get('instalacion')): # FICHA DE INSTALACIÓN
            caldera = Caldera.objects.get(pk = request.POST.get('instalacion'))
            if(request.POST.get('tipo') == 'pdf'):
                return generar_pdf(request,caldera, f"Ficha de Instalación de la caldera {caldera.tag}", "ficha_instalacion_caldera")
            
            if(request.POST.get('tipo') == 'xlsx'):
                return ficha_instalacion_caldera(caldera,request)

# VISTAS DE CALDERAS

class ConsultaCalderas(FiltradoSimpleMixin, ReportesFichasCalderasMixin, CargarCalderasMixin, LoginRequiredMixin, ListView):
    '''
    Resumen:
        Vista para la consulta de las calderas.
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
            Se utiliza para la generación de reportes de ficha o de calderas.

        get(self, request, *args, **kwargs) -> HttpResponse
            Se renderiza la página en su página y filtrado correcto.

        get_context_data(self, **kwargs) -> dict
            Genera el contexto necesario en la vista para la renderización de la plantilla

        get_queryset(self) -> QuerySet
            Obtiene el QuerySet de la lista de acuerdo al modelo del atributo.
            Hace el filtrado correspondiente y prefetching necesario para reducir las queries.
    '''
    model = Caldera
    template_name = 'calderas/consulta.html'
    paginate_by = 10
    titulo = "SIEVEP - Consulta de Calderas"

    def post(self, request, *args, **kwargs):
        reporte_ficha = self.reporte_ficha(request)
        if(reporte_ficha): # Si se está deseando generar un reporte de ficha, se genera
            return reporte_ficha

        if(request.POST.get('tipo') == 'pdf'): # Reporte de turbinas de vapor en PDF
            return generar_pdf(request, self.get_queryset(), 'Reporte de Listado de Calderas', 'calderas')
        
        if(request.POST.get('tipo') == 'xlsx'): # reporte de turbinas de vapor en XLSX
            return reporte_equipos(request, self.get_queryset(), 'Listado de Calderas', 'listado_calderas')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["link_creacion"] = "creacion_caldera"

        return context

    def get_queryset(self):        
        new_context = self.get_caldera(True, self.filtrar_equipos())

        return new_context

class CreacionCaldera(SuperUserRequiredMixin, View):
    """
    Resumen:
        Vista para el registro de nuevas calderas en el sistema.
        Solo puede ser accedido por superusuarios.

    Atributos:
        success_message: str -> Mensaje al realizarse correctamente la creación.
        titulo: str -> Título a mostrar en la vista.
        template_name: str -> Dirección de la plantilla.
    
    Métodos:
        get_context(self) -> dict
            Crea instancias de los formularios a ser utilizados y define el título de la vista.

        get(self, request, **kwargs) -> HttpResponse
            Renderiza el formulario con la plantilla correspondiente.

        almacenar_datos(self) -> HttpResponse
            Valida y almacena los datos de acuerdo a la lógica requerida para el almacenamiento de calderas por medio de los formularios.
            Si hay errores se levantará una Exception.

        post(self) -> HttpResponse
            Envía el request a los formularios y envía la respuesta al cliente.
    """

    success_message = "La nueva caldera ha sido registrada exitosamente. Los datos adicionales ya pueden ser cargados."
    titulo = 'SIEVEP - Creación de Caldera'
    template_name = 'calderas/creacion.html'

    def get_context(self):
        combustibles = ComposicionCombustible.objects.values('fluido').distinct()
        combustible_forms = []

        for i,x in enumerate(combustibles):
            form = ComposicionCombustibleForm(prefix=f'combustible-{i}', initial={'fluido': x['fluido']})
            combustible_forms.append({
                'combustible': Fluido.objects.get(pk=x['fluido']),
                'form': form
            })
            
        return {
            'form_caldera': CalderaForm(), 
            'form_tambor': TamborForm(prefix="tambor"), 
            'form_chimenea': ChimeneaForm(prefix="chimenea"),
            'form_economizador': EconomizadorForm(prefix="economizador"),
            'form_tambor_superior': SeccionTamborForm(prefix="tambor-superior"), 
            'form_tambor_inferior': SeccionTamborForm(prefix="tambor-inferior"), 
            'form_sobrecalentador': SobrecalentadorForm(prefix="sobrecalentador"),
            'form_dimensiones_sobrecalentador': DimsSobrecalentadorForm(prefix="dimensiones-sobrecalentador"),
            'form_especificaciones': EspecificacionesCalderaForm(prefix="especificaciones-caldera"),
            'form_dimensiones_caldera': DimensionesCalderaForm(prefix="dimensiones-caldera"),
            'form_combustible': CombustibleForm(prefix="combustible"),
            'composicion_combustible_forms': combustible_forms,
            'compuestos_aire': COMPUESTOS_AIRE,
            'titulo': self.titulo
        }

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context())
    
    def almacenar_datos(self, form_caldera, form_tambor, form_chimenea, form_economizador, form_tambor_superior, form_tambor_inferior,
                            form_sobrecalentador, form_dimensiones_caldera, form_dimensiones_sobrecalentador, form_especificaciones,
                            form_combustible, forms_composicion):
        error = ""
        with transaction.atomic(): 
            # Se validan los formularios
            valid = form_especificaciones.is_valid()            
            valid = valid and form_tambor.is_valid()
            valid = valid and form_chimenea.is_valid()
            valid = valid and form_economizador.is_valid()
            valid = valid and form_tambor_superior.is_valid()
            valid = valid and form_tambor_inferior.is_valid()
            valid = valid and form_sobrecalentador.is_valid()
            valid = valid and form_dimensiones_sobrecalentador.is_valid()
            valid = valid and form_dimensiones_caldera.is_valid()
            valid = valid and form_combustible.is_valid()
            valid = valid and form_caldera.is_valid()

            x_aire, x_volumen = 0,0
            for form in forms_composicion:
                valid = valid and form.is_valid()
                x_volumen += form.instance.porc_vol
                x_aire += form.instance.porc_aire if form.instance.porc_aire else 0

            if(round(x_volumen,2) != 100 or round(x_aire, 2) != 100):
                valid = False
                error = "La suma del porcentaje de las composiciones del combustible y del aire debe ser igual a 100." 
            
            if(valid):
                combustible = form_combustible.save()
                for form in forms_composicion:
                    form.instance.combustible = combustible
                    form.save()

                tambor = form_tambor.save()
                form_tambor_superior.instance.seccion = "S"
                form_tambor_superior.instance.tambor = tambor
                form_tambor_superior.save()
                form_tambor_inferior.instance.seccion = "I"
                form_tambor_inferior.instance.tambor = tambor
                form_tambor_inferior.save()

                chimenea = form_chimenea.save()
                economizador = form_economizador.save()
                form_dimensiones_sobrecalentador.instance.sobrecalentador = form_sobrecalentador.instance
                sobrecalentador_dimensiones = form_dimensiones_sobrecalentador.save()
                form_sobrecalentador.instance.dims = sobrecalentador_dimensiones
                form_sobrecalentador.save()

                especificaciones = form_especificaciones.save()
                dimensiones_caldera = form_dimensiones_caldera.save()
                
                form_caldera.instance.especificaciones = especificaciones
                form_caldera.instance.tambor = tambor
                form_caldera.instance.chimenea = chimenea
                form_caldera.instance.economizador = economizador
                form_caldera.instance.sobrecalentador = form_sobrecalentador.instance
                form_caldera.instance.dimensiones = dimensiones_caldera
                form_caldera.instance.combustible = combustible
                form_caldera.instance.creado_por = self.request.user

                form_caldera.save()

                messages.success(self.request, self.success_message)
                return redirect("/calderas")
            else:
                print([
                    form_especificaciones.errors,
                    form_tambor.errors,
                    form_chimenea.errors,
                    form_economizador.errors,
                    form_tambor_superior.errors,
                    form_tambor_inferior.errors,
                    form_sobrecalentador.errors,
                    form_dimensiones_sobrecalentador.errors,
                    form_dimensiones_caldera.errors,
                    form_combustible.errors,
                    form_caldera.errors
                ])
                raise Exception("Ocurrió un error. Verifique los datos e intente de nuevo." if error == "" else error)

    def post(self, request):
        # FORMS
        form_caldera = CalderaForm(request.POST) 
        form_tambor = TamborForm(request.POST, prefix="tambor") 
        form_chimenea = ChimeneaForm(request.POST, prefix="chimenea")
        form_economizador = EconomizadorForm(request.POST, prefix="economizador")
        form_tambor_superior = SeccionTamborForm(request.POST, prefix="tambor-superior") 
        form_tambor_inferior = SeccionTamborForm(request.POST, prefix="tambor-inferior") 
        form_sobrecalentador = SobrecalentadorForm(request.POST, prefix="sobrecalentador")
        form_dimensiones_sobrecalentador = DimsSobrecalentadorForm(request.POST, prefix="dimensiones-sobrecalentador")
        form_especificaciones = EspecificacionesCalderaForm(request.POST, prefix="especificaciones-caldera")
        form_dimensiones_caldera = DimensionesCalderaForm(request.POST, prefix="dimensiones-caldera")
        form_combustible = CombustibleForm(request.POST, prefix="combustible")
        forms_composicion = []

        for i in range(0,14):
            forms_composicion.append(ComposicionCombustibleForm(request.POST, prefix=f"combustible-{i}"))
        
        try:
            return self.almacenar_datos(form_caldera, form_tambor, form_chimenea, form_economizador, form_tambor_superior, form_tambor_inferior,
                                            form_sobrecalentador, form_dimensiones_caldera, form_dimensiones_sobrecalentador, form_especificaciones,
                                            form_combustible, forms_composicion)
        except Exception as e:
            print(str(e))

            combustible_forms = []
            for i,form in enumerate(forms_composicion):
                combustible_forms.append({
                    'combustible': form.instance.fluido,
                    'form': form
                })

            form_caldera.fields["planta"].queryset = Planta.objects.filter(complejo=form_caldera.instance.planta.complejo)

            return render(request, self.template_name, context={
                'form_caldera': form_caldera, 
                'form_tambor': form_tambor, 
                'form_chimenea': form_chimenea,
                'form_economizador': form_economizador,
                'form_tambor_superior': form_tambor_superior, 
                'form_tambor_inferior': form_tambor_inferior, 
                'form_sobrecalentador': form_sobrecalentador,
                'form_dimensiones_sobrecalentador': form_dimensiones_sobrecalentador,
                'form_especificaciones': form_especificaciones,
                'form_dimensiones_caldera': form_dimensiones_caldera,
                'form_combustible': form_combustible,
                'composicion_combustible_forms': combustible_forms,
                'compuestos_aire': COMPUESTOS_AIRE,
                'recargo': True,
                'titulo': self.titulo,
                'error': str(e)
            })

class EdicionCaldera(CargarCalderasMixin, CreacionCaldera):
    """
    Resumen:
        Vista para la creación o registro de nuevas calderas.
        Solo puede ser accedido por superusuarios.
        Hereda de CreacionCaldera debido a la gran similitud de los procesos de renderización y almacenamiento.

    Atributos:
        success_message: str -> Mensaje a ser enviado al usuario al editar exitosamente una caldera.
        titulo: str -> Título de la vista
    
    Métodos:
        get_context(self) -> dict
            Crea instancias de los formularios a ser utilizados y define el título de la vista.
            Asimismo define las instancias con las que serán cargados los formularios.

        post(self) -> HttpResponse
            Envía el request a los formularios y envía la respuesta al cliente.
    """

    success_message = "La caldera ha sido modificada exitosamente."
    titulo = 'SIEVEP - Edición de Caldera'
    
    def get_context(self):
        combustibles = ComposicionCombustible.objects.values('fluido').distinct()
        combustible_forms = []

        caldera = self.get_caldera(caldera_q=False)
        combustibles = caldera.combustible.composicion_combustible_caldera

        for i,composicion in enumerate(combustibles.all()):
            form = ComposicionCombustibleForm(prefix=f'combustible-{i}', instance=composicion)
            combustible_forms.append({
                'combustible': composicion.fluido,
                'form': form
            })

        planta = caldera.planta
            
        return {
            'form_caldera': CalderaForm(instance=caldera, initial={'complejo': planta.complejo, 'planta': planta}), 
            'form_tambor': TamborForm(prefix="tambor", instance=caldera.tambor), 
            'form_chimenea': ChimeneaForm(prefix="chimenea", instance=caldera.chimenea),
            'form_economizador': EconomizadorForm(prefix="economizador", instance=caldera.economizador),
            'form_tambor_superior': SeccionTamborForm(prefix="tambor-superior", instance=caldera.tambor.secciones_tambor.get(seccion="S")), 
            'form_tambor_inferior': SeccionTamborForm(prefix="tambor-inferior", instance=caldera.tambor.secciones_tambor.get(seccion="I")), 
            'form_sobrecalentador': SobrecalentadorForm(prefix="sobrecalentador", instance=caldera.sobrecalentador),
            'form_dimensiones_sobrecalentador': DimsSobrecalentadorForm(prefix="dimensiones-sobrecalentador", instance=caldera.sobrecalentador.dims),
            'form_especificaciones': EspecificacionesCalderaForm(prefix="especificaciones-caldera", instance=caldera.especificaciones),
            'form_dimensiones_caldera': DimensionesCalderaForm(prefix="dimensiones-caldera", instance=caldera.dimensiones),
            'form_combustible': CombustibleForm(prefix="combustible", instance=caldera.combustible),
            'composicion_combustible_forms': combustible_forms,
            'compuestos_aire': COMPUESTOS_AIRE,
            'edicion': True,
            'titulo': self.titulo + f" {caldera.tag}"
        }

    def post(self, request, pk):
        # FORMS
        caldera = self.get_caldera(caldera_q=False)
        
        planta = Planta.objects.get(pk=request.POST.get('planta'))
        form_caldera = CalderaForm(request.POST, instance=caldera, initial={'complejo': planta.complejo, 'planta': planta}) 
        
        form_caldera.instance.editado_por = request.user
        form_caldera.instance.editado_al = datetime.now()
        form_tambor = TamborForm(request.POST, prefix="tambor", instance=caldera.tambor) 
        form_chimenea = ChimeneaForm(request.POST, prefix="chimenea", instance=caldera.chimenea)
        form_economizador = EconomizadorForm(request.POST, prefix="economizador", instance=caldera.economizador)
        form_tambor_superior = SeccionTamborForm(request.POST, prefix="tambor-superior", instance=caldera.tambor.secciones_tambor.get(seccion="S")) 
        form_tambor_inferior = SeccionTamborForm(request.POST, prefix="tambor-inferior", instance=caldera.tambor.secciones_tambor.get(seccion="I")) 
        form_sobrecalentador = SobrecalentadorForm(request.POST, prefix="sobrecalentador", instance=caldera.sobrecalentador)
        form_dimensiones_sobrecalentador = DimsSobrecalentadorForm(request.POST, prefix="dimensiones-sobrecalentador", instance=caldera.sobrecalentador.dims)
        form_especificaciones = EspecificacionesCalderaForm(request.POST, prefix="especificaciones-caldera", instance=caldera.especificaciones)
        form_dimensiones_caldera = DimensionesCalderaForm(request.POST, prefix="dimensiones-caldera", instance=caldera.dimensiones)
        form_combustible = CombustibleForm(request.POST, prefix="combustible", instance=caldera.combustible)
        forms_composicion = []

        for i,x in enumerate(caldera.combustible.composicion_combustible_caldera.all()):
            forms_composicion.append(ComposicionCombustibleForm(request.POST, prefix=f"combustible-{i}", instance=x))

        try:
            return self.almacenar_datos(form_caldera, form_tambor, form_chimenea, form_economizador, form_tambor_superior, form_tambor_inferior,
                                            form_sobrecalentador, form_dimensiones_caldera, form_dimensiones_sobrecalentador, form_especificaciones,
                                            form_combustible, forms_composicion)
        except Exception as e:
            print(str(e))

            combustible_forms = []
            for i,form in enumerate(forms_composicion):
                combustible_forms.append({
                    'combustible': form.instance.fluido,
                    'form': form
                })

            return render(request, self.template_name, context={
                'form_caldera': form_caldera, 
                'form_tambor': form_tambor, 
                'form_chimenea': form_chimenea,
                'form_economizador': form_economizador,
                'form_tambor_superior': form_tambor_superior, 
                'form_tambor_inferior': form_tambor_inferior, 
                'form_sobrecalentador': form_sobrecalentador,
                'form_dimensiones_sobrecalentador': form_dimensiones_sobrecalentador,
                'form_especificaciones': form_especificaciones,
                'form_dimensiones_caldera': form_dimensiones_caldera,
                'form_combustible': form_combustible,
                'composicion_combustible_forms': combustible_forms,
                'compuestos_aire': COMPUESTOS_AIRE,
                'edicion': True,
                'titulo': self.titulo + f" {caldera.tag}",
                'error': str(e)
            })
        
class RegistroDatosAdicionales(SuperUserRequiredMixin, CargarCalderasMixin, View):
    """
    Resumen:
        Vista para el registro de datos adicionales de una caldera.
        Solo puede ser accedido por superusuarios.

    Atributos:
        success_message: str -> Mensaje al realizarse correctamente el registro.
        titulo: str -> Título a mostrar en la vista.
        template_name: str -> Dirección de la plantilla.
    
    Métodos:
        get_context(self) -> dict
            Crea instancias de los formularios a ser utilizados y define el título de la vista.

        get(self, request, **kwargs) -> HttpResponse
            Renderiza el formulario con la plantilla correspondiente.

        almacenar_datos(self) -> HttpResponse
            Valida y almacena los datos de acuerdo a la lógica requerida para el almacenamiento de calderas por medio de los formularios.
            Si hay errores se levantará una Exception.

        post(self) -> HttpResponse
            Envía el request a los formularios y envía la respuesta al cliente.
    """

    success_message = "Se han registrado los datos adicionales a la caldera."
    titulo = 'SIEVEP - Registro de Datos Adicionales de Caldera'
    template_name = 'calderas/creacion_adicionales.html'

    def get_context(self):
        caldera = self.get_caldera(caldera_q=False)
        corrientes = caldera.corrientes_caldera.all()
        corrientes_requeridas = ["A","B","W","P"]
        forms_corrientes = []

        for i,corriente in enumerate(corrientes):
            forms_corrientes.append(CorrienteForm(instance=corriente, prefix=f"corriente-{i}"))
            corrientes_requeridas = [x for x in corrientes_requeridas if corriente.tipo != x]
        
        for tipo in corrientes_requeridas:
            forms_corrientes.append(CorrienteForm(initial={'tipo': tipo}, prefix=f"corriente-{len(forms_corrientes)}"))

        caracteristicas = caldera.caracteristicas_caldera.select_related('tipo_unidad','unidad').all()
        formset_caracteristicas = forms.modelformset_factory(model=Caracteristica, form=CaracteristicaForm, extra=0 if len(caracteristicas) else 1, min_num=0)
        formset_caracteristicas = formset_caracteristicas(queryset=caracteristicas)

        return {
            'unidades': Unidades.objects.all().values('pk', 'simbolo', 'tipo'),
            'tipo_unidades': ClasesUnidades.objects.all().values('pk', 'nombre'),
            'forms_corrientes': forms_corrientes,
            'forms_caracteristicas': formset_caracteristicas,
            'caldera': caldera,
            'titulo': self.titulo
        }
    
    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context())
         
    def almacenar_datos(self, form_corrientes, form_caracteristicas):
        caldera = self.get_caldera(False, False)

        with transaction.atomic():
            all_valid = True

            for form in form_corrientes:
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.caldera = caldera
                    instance.save(update_fields=form.changed_data)
                else:
                    all_valid = False

            if form_caracteristicas.is_valid():
                for form in form_caracteristicas:
                    if form.is_valid() and form.cleaned_data:
                        instance = form.save(commit=False)
                        instance.caldera = caldera
                        instance.save()
                    else:
                        all_valid = False
            else:
                raise Exception("Ocurrió un Error de Validación General.")

            if all_valid:
                messages.success(self.request, self.success_message)
            else:
                messages.warning(self.request, "Los datos adicionales fueron guardados pero no todos fueron validados.")

            return redirect('/calderas')
        
    def post(self, request, pk):
        # FORMS
        caldera = self.get_caldera(caldera_q=False)
        corrientes = caldera.corrientes_caldera.all()
        form_corrientes = []

        for i in range(0,4):
            prefix = f"corriente-{i}"
            tipo = request.POST[f"{prefix}-tipo"]

            if(corrientes.filter(tipo=tipo).exists()):
                form_corrientes.append(CorrienteForm(request.POST, instance=corrientes.get(tipo=tipo), prefix=prefix))
            else:
                form_corrientes.append(CorrienteForm(request.POST, prefix=prefix))
        
        form_caracteristicas = forms.modelformset_factory(model=Caracteristica, form=CaracteristicaForm)
        form_caracteristicas = form_caracteristicas(request.POST, prefix="form")
        
        try:
            return self.almacenar_datos(form_corrientes, form_caracteristicas)

        except Exception as e:
            print(str(e))
            print([form.errors for form in form_corrientes])
            print(len(form_caracteristicas.errors))
            return render(request, self.template_name, context={
                'error': str(e),
                'forms_corrientes': form_corrientes,
                'forms_caracteristicas': form_caracteristicas,
                'caldera': caldera,
                'unidades': Unidades.objects.all().values('pk', 'simbolo', 'tipo'),
            })

# VISTAS DE EVALUACIONES

class ConsultaEvaluacionCaldera(ConsultaEvaluacion, CargarCalderasMixin, ReportesFichasCalderasMixin):
    """
    Resumen:
        Vista para la creación o registro de nuevas calderas.
        Solo puede ser accedido por superusuarios.
        Hereda de ConsultaEvaluacion.

    Atributos:
        model: EvaluacionBomba -> Modelo de la vista
        model_equipment -> Modelo del equipo
        clase_equipo -> Complemento del título de la vista
    
    Métodos:
        get_context_data(self) -> dict
            Añade al contexto original el equipo.

        get_queryset(self) -> QuerySet
            Hace el prefetching correspondiente al queryset de las evaluaciones

        post(self) -> HttpResponse
            Contiene la lógica de eliminación (ocultación) de una evaluación.
    """
    model = Evaluacion
    model_equipment = Caldera
    clase_equipo = " la Caldera"
    template_name = 'calderas/consulta_evaluaciones.html'

    def post(self, request, **kwargs):
        if(request.user.is_superuser and request.POST.get('evaluacion')): # Lógica de "Eliminación"
            evaluacion = self.model.objects.get(pk=request.POST['evaluacion'])
            evaluacion.activo = False
            evaluacion.save()
            messages.success(request, "Evaluación eliminada exitosamente.")
        elif(request.POST.get('evaluacion') and not request.user.is_superuser):
            messages.warning(request, "Usted no tiene permiso para eliminar evaluaciones.")

        reporte_ficha = self.reporte_ficha(request)
        if(reporte_ficha):
            return reporte_ficha

        if(request.POST.get('tipo') == 'pdf'):
            return generar_pdf(request, self.get_queryset(), f"Evaluaciones de la Bomba {self.get_bomba().tag}", "evaluaciones_bombas")
        elif(request.POST.get('tipo') == 'xlsx'):
            return historico_evaluaciones_caldera(self.get_queryset(), request)

        if(request.POST.get('detalle')):
            return generar_pdf(request, self.model.objects.get(pk=request.POST.get('detalle')), "Detalle de Evaluación de Bomba", "detalle_evaluacion_bomba")

        return self.get(request, **kwargs)
    
    def get_queryset(self):
        new_context = super().get_queryset()

        new_context = new_context.select_related(
            'usuario',             
            'salida_flujos',  
            'salida_fracciones', 
            'salida_balance_energia',
            'salida_lado_agua'
        )

        new_context = new_context.prefetch_related(
            'entradas_fluidos_caldera', 'composiciones_evaluacion'
        )

        return new_context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipo'] = self.get_caldera(True, False)

        return context

class CreacionEvaluacionCaldera(LoginRequiredMixin, CargarCalderasMixin, View):
    def make_forms(self, caldera, composiciones, corrientes):
        formset_composicion = [
            {
                'form': EntradaComposicionForm(prefix=f'composicion-{i}', initial = {'parc_vol': composicion.porc_vol, 'composicion': composicion, 'parc_aire': composicion.porc_aire}),
                'composicion': composicion
            } for i,composicion in enumerate(composiciones)
        ]

        corriente_agua = corrientes.get(tipo='W') if corrientes.filter(tipo="W").exists() else None
        corriente_vapor = corrientes.get(tipo='A') if corrientes.filter(tipo="W").exists() else None

        forms = {
            'form_gas': EntradasFluidosForm(prefix='gas', initial={
                'tipo': 'G',
                'flujo': caldera.especificaciones.carga,
                'flujo_unidad': caldera.especificaciones.carga_unidad
            }),
            'form_aire': EntradasFluidosForm(prefix='aire', initial={
                'tipo': 'A'
            }),
            'form_horno': EntradasFluidosForm(prefix='horno', initial={
                'tipo': 'H'
            }), 
            'form_agua': EntradasFluidosForm(prefix='agua', initial={
                'tipo': 'W',
                'flujo': corriente_agua.flujo_masico if corriente_agua else None,
                'flujo_unidad': corriente_agua.flujo_masico_unidad if corriente_agua else None,
                'presion': corriente_agua.presion if corriente_agua else None,
                'presion_unidad': corriente_agua.presion_unidad if corriente_agua else None,
                'temperatura': corriente_agua.temp_operacion if corriente_agua else None,
                'temperatura_unidad': corriente_agua.temp_operacion_unidad if corriente_agua else None
            }),
            'form_vapor': EntradasFluidosForm(prefix='vapor', initial={
                'tipo': 'V',
                'flujo': corriente_vapor.flujo_masico if corriente_vapor else None,
                'flujo_unidad': corriente_vapor.flujo_masico_unidad if corriente_vapor else None,
                'presion': corriente_vapor.presion if corriente_vapor else None,
                'presion_unidad': corriente_vapor.presion_unidad if corriente_vapor else None,
                'temperatura': corriente_vapor.temp_operacion if corriente_vapor else None,
                'temperatura_unidad': corriente_vapor.temp_operacion_unidad if corriente_vapor else None
            }), 

            'form_evaluacion': EvaluacionForm(prefix='evaluacion'),
            'formset_composicion': formset_composicion
        }

        return forms

    def get_context_data(self, **kwargs):
        context = {}
        context['equipo'] = self.get_caldera(True, False)

        composiciones = ComposicionCombustible.objects.filter(combustible= context['equipo'].combustible).select_related('fluido')
        corrientes = context['equipo'].corrientes_caldera.select_related('flujo_masico_unidad', 'presion_unidad', 'temp_operacion_unidad')        
        unidades = Unidades.objects.all().values('pk', 'simbolo', 'tipo')

        context['forms'] = self.make_forms(context['equipo'], composiciones, corrientes)
        context['unidades'] = unidades
        context['fluidos_composiciones'] = COMPUESTOS_AIRE

        return context

    def get(self, *args, **kwargs):
        return render(self.request, 'calderas/evaluacion.html', context=self.get_context_data())
    
    def evaluar(self):
        resultados = self.calcular_resultados()
        return render(self.request, 'calderas/partials/resultados.html', context={
            'resultados': resultados
        })
    
    def almacenamiento_fallido(self):
        return render(self.request, 'calderas/partials/almacenamiento_fallido.html')
    
    def almacenamiento_exitoso(self):
        return render(self.request, 'calderas/partials/almacenamiento_exitoso.html', context={
            'caldera': self.get_caldera(False, False)
        })

    def almacenar(self):
        request = self.request

        composiciones = ComposicionCombustible.objects.filter(
            combustible= self.get_caldera(True, False).combustible
        ).select_related(
            'fluido'
        )
        
        forms_composicion = [
            EntradaComposicionForm(request.POST, prefix=f'composicion-{i}') 
            for i,composicion in enumerate(composiciones)
        ]

        form_vapor = EntradasFluidosForm(request.POST, prefix='vapor')
        form_gas = EntradasFluidosForm(request.POST, prefix='gas')
        form_aire = EntradasFluidosForm(request.POST, prefix='aire')
        form_horno = EntradasFluidosForm(request.POST, prefix='horno')
        form_agua = EntradasFluidosForm(request.POST, prefix='agua')

        resultado = self.calcular_resultados()

        with transaction.atomic():
            if all([form_vapor.is_valid(), form_gas.is_valid(), form_aire.is_valid(), form_horno.is_valid(), form_agua.is_valid()]):
                salida_fracciones = SalidaFracciones.objects.create(
                    h2o = resultado['fraccion_h2o_gas'],
                    co2 = resultado['fraccion_n2_gas'],
                    n2 = resultado['fraccion_o2_gas'],
                    so2 = resultado['fraccion_o2_gas']
                )

                salida_lado_agua = SalidaLadoAgua.objects.create(
                    flujo_purga = resultado['flujo_purga'],
                    energia_vapor = resultado['energia_vapor'],
                )

                salida_flujos = SalidaFlujosEntrada.objects.create(
                    flujo_m_gas_entrada = resultado['balance_gas']['masico'],
                    flujo_n_gas_entrada = resultado['balance_gas']['molar'],
                    flujo_m_aire_entrada = resultado['balance_aire']['masico'],
                    flujo_n_aire_entrada = resultado['balance_aire']['molar'],
                    flujo_combustion = resultado['flujo_combustion_masico'],
                    flujo_combustion_vol = resultado['flujo_combustion'],
                    porc_o2_exceso = resultado['oxigeno_exceso'],
                )

                salida_balance_energia = SalidaBalanceEnergia.objects.create(
                    energia_entrada_gas = resultado['energia_gas_entrada'],
                    energia_entrada_aire = resultado['energia_aire_entrada'],
                    energia_total_entrada = resultado['energia_total_entrada'],
                    energia_total_reaccion = resultado['energia_total_reaccion'],
                    energia_horno = resultado['energia_horno']
                )
                
                evaluacion = Evaluacion.objects.create(
                    nombre = request.POST['evaluacion-nombre'],
                    equipo = self.get_caldera(True, False),
                    usuario = request.user,
                    eficiencia = resultado['eficiencia'],

                    salida_flujos = salida_flujos,
                    salida_fracciones = salida_fracciones,
                    salida_lado_agua = salida_lado_agua,
                    salida_balance_energia = salida_balance_energia
                )

                form_vapor.instance.evaluacion = evaluacion                
                form_vapor.save()

                form_gas.instance.evaluacion = evaluacion
                form_gas.save()

                form_aire.instance.evaluacion = evaluacion
                form_aire.save()

                form_horno.instance.evaluacion = evaluacion
                form_horno.save()

                form_agua.instance.evaluacion = evaluacion
                form_agua.save()

                for form_composicion in forms_composicion:
                    if form_composicion.is_valid():
                        form_composicion.instance.evaluacion = evaluacion
                        form_composicion.save()
                    else:
                        print(form_composicion.errors)
                        return self.almacenamiento_fallido()

                return self.almacenamiento_exitoso()
            else:
                print([form.errors for form in [form_vapor, form_gas, form_aire, form_horno, form_agua]])
                return self.almacenamiento_fallido()

    def calcular_resultados(self):
        request = self.request

        variables = {
            'gas-flujo': 'gas-flujo_unidad',
            'gas-temperatura': 'gas-temperatura_unidad',
            'gas-presion': 'gas-presion_unidad',
            'aire-flujo': 'aire-flujo_unidad',
            'aire-temperatura': 'aire-temperatura_unidad',
            'aire-presion': 'aire-presion_unidad',
            'aire-humedad_relativa': None,
            'horno-temperatura': 'horno-temperatura_unidad',
            'horno-presion': 'horno-presion_unidad',
            'agua-flujo': 'agua-flujo_unidad',
            'agua-temperatura': 'agua-temperatura_unidad',
            'agua-presion': 'agua-presion_unidad',
            'vapor-flujo': 'vapor-flujo_unidad',
            'vapor-temperatura': 'vapor-temperatura_unidad',
            'vapor-presion': 'vapor-presion_unidad',
        }

        variables_eval = {}

        for valor,u in variables.items():
            unidad = int(request.POST.get(u)) if u else None
            valor_num = float(request.POST.get(valor))
            funcion = transformar_unidades_presion if u and ('presion' in u) else \
                transformar_unidades_temperatura if u and ('temperatura' in u) else \
                transformar_unidades_flujo_volumetrico if u and ('gas' in u or 'aire' in u) else \
                transformar_unidades_flujo

            if unidad:
                valor_num = funcion([valor_num], unidad)[0]

            llave = "_".join(valor.split('-')[::-1])
            variables_eval[llave] = valor_num

        composiciones = []
        fluidos = []
        for i in range(15):
            fluidos.append(request.POST.get(f'composicion-{i}-composicion'))

        fluidos = ComposicionCombustible.objects.select_related(
            'fluido'
        ).filter(pk__in=fluidos).annotate(
            cas=F('fluido__cas'), 
            nombre=F('fluido__nombre')
        ).values('cas', 'nombre')

        for i in range(15):
            fluido = fluidos[i]
            parc_vol = request.POST.get(f'composicion-{i}-parc_vol')
            parc_aire = request.POST.get(f'composicion-{i}-parc_aire')
            
            if fluido:
                composiciones.append({
                    'fluido': fluido,
                    'porc_vol': parc_vol,
                    'porc_aire': parc_aire
                })
        
        resultados = evaluar_caldera(**variables_eval, composiciones_combustible=composiciones)
        return resultados

    def post(self, request, pk, *args, **kwargs):
        if(request.POST.get('accion')):
            try:
                return self.almacenar()
            except Exception as e:
                return self.almacenamiento_fallido()
        else:
            return self.evaluar()

# VISTAS PARA LA GENERACIÓN DE PLANTILLAS PARCIALES
def unidades_por_clase(request):
    return render(request, 'calderas/partials/unidades_por_clase.html', context={
        'unidades': Unidades.objects.filter(
            tipo = request.GET.get('clase')
        ),
        'form': int(request.GET.get('form'))
    })