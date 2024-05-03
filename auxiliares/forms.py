from django import forms
from intercambiadores.models import Complejo
from auxiliares.models import *
from calculos.unidades import transformar_unidades_presion
from simulaciones_pequiven.unidades import *

class FormConUnidades(forms.ModelForm):
    '''
    Resumen:
        Los forms que heredan de este form, pueden filtrar las unidades que requieran.
        Por ejemplo, un campo llamado "diametro" requerirá unidades de longitud ('L'). 
    '''
    def limpiar_campos_unidades(self):
        pass
     
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.limpiar_campos_unidades()

class BombaForm(forms.ModelForm):
    complejo = forms.ModelChoiceField(queryset=Complejo.objects.all(), initial=1)
    class Meta:
        model = Bombas
        fields = [
            "tag", "descripcion", "fabricante", "modelo",
            "planta", "grafica", "tipo_bomba", "creado_por"
        ]

class EspecificacionesBombaForm(FormConUnidades):

    def limpiar_campos_unidades(self):
        self.fields['velocidad_unidad'].empty_label = None
        self.fields['velocidad_unidad'].queryset = Unidades.objects.filter(simbolo = 'RPM')

        self.fields['potencia_unidad'].empty_label = None
        self.fields['potencia_unidad'].queryset = UNIDADES_POTENCIA

        self.fields['npshr_unidad'].empty_label = None
        self.fields['npshr_unidad'].queryset = UNIDADES_LONGITUD

        self.fields['id_unidad'].empty_label = None
        self.fields['id_unidad'].queryset = UNIDADES_LONGITUD

        self.fields['cabezal_unidad'].empty_label = None
        self.fields['cabezal_unidad'].queryset = UNIDADES_LONGITUD

    class Meta:
        model = EspecificacionesBomba
        exclude = (
            "id",
        )

class DetallesConstruccionBombaForm(forms.ModelForm): 
    class Meta:
        model = DetallesConstruccionBomba
        exclude = (
            "id",
        )

class DetallesMotorBombaForm(FormConUnidades):
    def limpiar_campos_unidades(self):
        self.fields['velocidad_motor_unidad'].empty_label = None
        self.fields['velocidad_motor_unidad'].queryset = Unidades.objects.filter(simbolo = 'RPM')

        self.fields['potencia_motor_unidad'].empty_label = None
        self.fields['potencia_motor_unidad'].queryset = UNIDADES_POTENCIA

        self.fields['voltaje_unidad'].empty_label = None
        self.fields['voltaje_unidad'].queryset = Unidades.objects.filter(tipo = 'X')

        self.fields['frecuencia_unidad'].empty_label = None
        self.fields['frecuencia_unidad'].queryset = Unidades.objects.filter(tipo = 'H')

    class Meta:
        model = DetallesMotorBomba
        exclude = (
            "id",
        )

class CondicionesDisenoBombaForm(FormConUnidades):
    def limpiar_campos_unidades(self):
        self.fields['capacidad_unidad'].empty_label = None
        self.fields['capacidad_unidad'].queryset = UNIDADES_FLUJO_VOLUMETRICO

        self.fields['presion_unidad'].empty_label = None
        self.fields['presion_unidad'].queryset = UNIDADES_PRESION

        self.fields['npsha_unidad'].empty_label = None
        self.fields['npsha_unidad'].queryset = UNIDADES_LONGITUD
    
    class Meta:
        model = CondicionesDisenoBomba
        exclude = (
            "id",
            "condiciones_fluido"
        )

class CondicionFluidoBombaForm(FormConUnidades):
    def limpiar_campos_unidades(self):
        self.fields['temperatura_unidad'].empty_label = None
        self.fields['temperatura_unidad'].queryset = UNIDADES_TEMPERATURA

        self.fields['presion_vapor_unidad'].empty_label = None
        self.fields['presion_vapor_unidad'].queryset = UNIDADES_PRESION

        self.fields['viscosidad_unidad'].empty_label = None
        self.fields['viscosidad_unidad'].queryset = UNIDADES_VISCOSIDAD

        self.fields['concentracion_unidad'].empty_label = None
        self.fields['concentracion_unidad'].queryset = Unidades.objects.filter(tipo = '%')

        self.fields['densidad_unidad'].queryset = UNIDADES_DENSIDAD

    def clean_densidad(self):
        if(self.data.get('densidad') in (None, '') and self.data['calculo_propiedades'] == 'M'):
            raise forms.ValidationError('Esta propiedad es requerida. Si no la tiene use el cálculo automático.')
        
        return self.data.get('densidad')
    
    def clean_viscosidad(self):
        if(self.data.get('viscosidad') in (None, '') and self.data['calculo_propiedades'] == 'M'):
            raise forms.ValidationError('Esta propiedad es requerida. Si no la tiene use el cálculo automático.')
        
        return self.data.get('viscosidad')
    
    def clean_presion_vapor(self):
        if(self.data.get('presion_vapor') in (None, '') and self.data['calculo_propiedades'] == 'M'):
            raise forms.ValidationError('Esta propiedad es requerida. Si no la tiene use el cálculo automático.')
        
        return self.data.get('presion_vapor')
    
    def clean_fluido(self):
        fluido = self.data.get('fluido')
        if((fluido == None or fluido == '') and self.data.get('nombre_fluido') == '---------'):
            raise forms.ValidationError('Se debe establecer un fluido para la bomba.')
        elif(fluido.isnumeric()):
            return Fluido.objects.get(pk = int(fluido))
        else:
            return None
        
    def clean_nombre_fluido(self):
        return (self.data.get('nombre_fluido').upper() if self.data.get('nombre_fluido') else self.instance.nombre_fluido) if not self.clean_fluido() else None 

    class Meta:
        model = CondicionFluidoBomba
        exclude = (
            "id",
        )

class EspecificacionesInstalacionForm(FormConUnidades):
    def limpiar_campos_unidades(self):
        self.fields['elevacion_unidad'].empty_label = None
        self.fields['elevacion_unidad'].queryset = UNIDADES_LONGITUD

    class Meta:
        model = EspecificacionesInstalacion
        exclude = (
            "pk",
            "usuario"
        )

class TuberiaInstalacionBombaForm(FormConUnidades):
    def limpiar_campos_unidades(self):
        self.fields['diametro_tuberia_unidad'].empty_label = None
        self.fields['diametro_tuberia_unidad'].queryset = UNIDADES_LONGITUD

        self.fields['longitud_tuberia_unidad'].empty_label = None
        self.fields['longitud_tuberia_unidad'].queryset = UNIDADES_LONGITUD

    class Meta:
        model = TuberiaInstalacionBomba
        exclude = (
            "pk",
            "instalacion"
        )

class EvaluacionBombaForm(forms.ModelForm):
    class Meta:
        model = EvaluacionBomba
        fields = ('nombre',)

class EntradaEvaluacionBombaForm(FormConUnidades):
    def limpiar_campos_unidades(self):
        self.fields['altura_unidad'].empty_label = None
        self.fields['altura_unidad'].queryset = UNIDADES_LONGITUD

        self.fields['presion_unidad'].empty_label = None
        self.fields['presion_unidad'].queryset = UNIDADES_PRESION
        
        self.fields['presion_vapor_unidad'].empty_label = None
        self.fields['presion_vapor_unidad'].queryset = UNIDADES_PRESION

        self.fields['temperatura_unidad'].empty_label = None
        self.fields['temperatura_unidad'].queryset = UNIDADES_TEMPERATURA

        self.fields['viscosidad_unidad'].empty_label = None
        self.fields['viscosidad_unidad'].queryset = UNIDADES_VISCOSIDAD

        self.fields['potencia_unidad'].empty_label = None
        self.fields['potencia_unidad'].queryset = UNIDADES_POTENCIA

        self.fields['flujo_unidad'].empty_label = None
        self.fields['flujo_unidad'].queryset = UNIDADES_FLUJO_VOLUMETRICO

        self.fields['npshr_unidad'].empty_label = None
        self.fields['npshr_unidad'].queryset = UNIDADES_LONGITUD

        self.fields['densidad_unidad'].queryset = UNIDADES_DENSIDAD

        self.fields['calculo_propiedades'].choices = (('A', 'Automático'), ('M', 'Manual'), ('F', 'Ficha'))

    class Meta:
        model = EntradaEvaluacionBomba
        exclude = ('id', 'evaluacion', 'diametro_succion', 'diametro_descarga', 'diametro_unidad', 'velocidad', 'velocidad_unidad')

EspecificacionesInstalacionFormSet = forms.modelformset_factory(EspecificacionesInstalacion, form=EspecificacionesInstalacionForm, min_num=2, max_num=2)
TuberiaFormSet = forms.modelformset_factory(TuberiaInstalacionBomba, form=TuberiaInstalacionBombaForm, min_num=1, extra=0)

# FORMS DE VENTILADORES

class VentiladorForm(forms.ModelForm):
    complejo = forms.ModelChoiceField(queryset=Complejo.objects.all(), initial=1)

    class Meta:
        model = Ventilador
        exclude = ('id','condiciones_trabajo','condiciones_adicionales',
                   'condiciones_generales','especificaciones', 'creado_al','editado_al',
                   'creado_por','editado_por')
        
class EspecificacionesVentiladorForm(FormConUnidades):
    def limpiar_campos_unidades(self):
        self.fields['espesor_unidad'].empty_label = None
        self.fields['espesor_unidad'].queryset = UNIDADES_LONGITUD

        self.fields['potencia_motor_unidad'].empty_label = None
        self.fields['potencia_motor_unidad'].queryset = UNIDADES_POTENCIA
        
        self.fields['velocidad_motor_unidad'].empty_label = None
        self.fields['velocidad_motor_unidad'].queryset = UNIDADES_VELOCIDAD_ANGULAR

    class Meta:
        model = EspecificacionesVentilador
        exclude = ('id',)

class CondicionesGeneralesVentiladorForm(FormConUnidades):
    def limpiar_campos_unidades(self):
        self.fields['presion_barometrica_unidad'].empty_label = None
        self.fields['presion_barometrica_unidad'].queryset = UNIDADES_PRESION

        self.fields['temp_ambiente_unidad'].empty_label = None
        self.fields['temp_ambiente_unidad'].queryset = UNIDADES_TEMPERATURA
        
        self.fields['velocidad_diseno_unidad'].empty_label = None
        self.fields['velocidad_diseno_unidad'].queryset = UNIDADES_VELOCIDAD_ANGULAR

    class Meta:
        model = CondicionesGeneralesVentilador
        exclude = ('id',)

class CondicionesTrabajoVentiladorForm(FormConUnidades):
    def clean_presion_entrada(self):
        prefix = self.prefix + '-' if self.prefix else ''
        presion_entrada = self.data[f'{prefix}presion_entrada']
        
        if(presion_entrada != ''):
            presion_unidad = int(self.data[f'{prefix}presion_unidad'])
            presion_entrada_calculada = transformar_unidades_presion([float(presion_entrada)], presion_unidad)[0]

            if(presion_entrada_calculada < -101325):
                raise forms.ValidationError("La presión no puede ser menor a la presión atmosférica negativa.")
        
        return float(presion_entrada) if presion_entrada != '' else None
            
    def clean_presion_salida(self):
        prefix = self.prefix + '-' if self.prefix else ''
        presion_salida = self.data[f'{prefix}presion_salida']
        
        if(presion_salida != ''):
            presion_unidad = int(self.data[f'{prefix}presion_unidad'])
            presion_salida_calculada = transformar_unidades_presion([float(presion_salida)], presion_unidad)[0]

            if(presion_salida_calculada < -101325):
                raise forms.ValidationError("La presión no puede ser menor a la presión atmosférica negativa.")
            
        return float(presion_salida) if presion_salida != '' else None

    def limpiar_campos_unidades(self):
        self.fields['flujo_unidad'].empty_label = None
        self.fields['flujo_unidad'].queryset = UNIDADES_FLUJOS

        self.fields['presion_unidad'].empty_label = None
        self.fields['presion_unidad'].queryset = UNIDADES_PRESION
        
        self.fields['densidad_unidad'].empty_label = None
        self.fields['densidad_unidad'].queryset = UNIDADES_DENSIDAD

        self.fields['temperatura_unidad'].empty_label = None
        self.fields['temperatura_unidad'].queryset = UNIDADES_TEMPERATURA

        self.fields['velocidad_funcionamiento_unidad'].empty_label = None
        self.fields['velocidad_funcionamiento_unidad'].queryset = UNIDADES_VELOCIDAD_ANGULAR

        self.fields['potencia_freno_unidad'].empty_label = None
        self.fields['potencia_freno_unidad'].queryset = UNIDADES_POTENCIA

    class Meta:
        model = CondicionesTrabajoVentilador
        exclude = ('id','eficiencia','tipo_flujo')

class EvaluacionVentiladorForm(forms.ModelForm):
    class Meta:
        model = EvaluacionVentilador
        fields = ('nombre',)

class EntradaEvaluacionVentiladorForm(FormConUnidades):
    def limpiar_campos_unidades(self):
        self.fields['flujo_unidad'].empty_label = None
        self.fields['flujo_unidad'].queryset = UNIDADES_FLUJOS

        self.fields['presion_salida_unidad'].empty_label = None
        self.fields['presion_salida_unidad'].queryset = UNIDADES_PRESION
        
        self.fields['densidad_evaluacion_unidad'].empty_label = None
        self.fields['densidad_evaluacion_unidad'].queryset = UNIDADES_DENSIDAD

        self.fields['temperatura_operacion_unidad'].empty_label = None
        self.fields['temperatura_operacion_unidad'].queryset = UNIDADES_TEMPERATURA

        self.fields['potencia_ventilador_unidad'].empty_label = None
        self.fields['potencia_ventilador_unidad'].queryset = UNIDADES_POTENCIA
        
    class Meta:
        model = EntradaEvaluacionVentilador
        exclude = ('id','tipo_flujo','densidad_ficha', 'densidad_ficha_unidad')