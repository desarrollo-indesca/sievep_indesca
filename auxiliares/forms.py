from django import forms
from intercambiadores.models import Complejo
from auxiliares.models import *

class FormConUnidades(forms.ModelForm):
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
        self.fields['potencia_unidad'].queryset = Unidades.objects.filter(tipo = 'B')

        self.fields['npshr_unidad'].empty_label = None
        self.fields['npshr_unidad'].queryset = Unidades.objects.filter(tipo = 'L')

        self.fields['id_unidad'].empty_label = None
        self.fields['id_unidad'].queryset = Unidades.objects.filter(tipo = 'L')

        self.fields['cabezal_unidad'].empty_label = None
        self.fields['cabezal_unidad'].queryset = Unidades.objects.filter(tipo = 'L')

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
        self.fields['potencia_motor_unidad'].queryset = Unidades.objects.filter(tipo = 'B')

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
        self.fields['capacidad_unidad'].queryset = Unidades.objects.filter(tipo = 'k')

        self.fields['presion_unidad'].empty_label = None
        self.fields['presion_unidad'].queryset = Unidades.objects.filter(tipo = 'P')

        self.fields['npsha_unidad'].empty_label = None
        self.fields['npsha_unidad'].queryset = Unidades.objects.filter(tipo = 'L')
    
    class Meta:
        model = CondicionesDisenoBomba
        exclude = (
            "id",
            "condiciones_fluido"
        )

class CondicionFluidoBombaForm(FormConUnidades):
    def limpiar_campos_unidades(self):
        self.fields['temperatura_unidad'].empty_label = None
        self.fields['temperatura_unidad'].queryset = Unidades.objects.filter(tipo = 'T')

        self.fields['presion_vapor_unidad'].empty_label = None
        self.fields['presion_vapor_unidad'].queryset = Unidades.objects.filter(tipo = 'P')

        self.fields['viscosidad_unidad'].empty_label = None
        self.fields['viscosidad_unidad'].queryset = Unidades.objects.filter(tipo = 'v')

        self.fields['concentracion_unidad'].empty_label = None
        self.fields['concentracion_unidad'].queryset = Unidades.objects.filter(tipo = '%')

        self.fields['densidad_unidad'].queryset = Unidades.objects.filter(tipo = 'd')

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
        return self.data.get('nombre_fluido').upper() if not self.clean_fluido() else None 

    class Meta:
        model = CondicionFluidoBomba
        exclude = (
            "id",
        )

class EspecificacionesInstalacionForm(FormConUnidades):
    def limpiar_campos_unidades(self):
        self.fields['elevacion_unidad'].empty_label = None
        self.fields['elevacion_unidad'].queryset = Unidades.objects.filter(tipo = 'L')

    class Meta:
        model = EspecificacionesInstalacion
        exclude = (
            "pk",
            "usuario"
        )

class TuberiaInstalacionBombaForm(FormConUnidades):
    def limpiar_campos_unidades(self):
        self.fields['diametro_tuberia_unidad'].empty_label = None
        self.fields['diametro_tuberia_unidad'].queryset = Unidades.objects.filter(tipo = 'L')

        self.fields['longitud_tuberia_unidad'].empty_label = None
        self.fields['longitud_tuberia_unidad'].queryset = Unidades.objects.filter(tipo = 'L')

    class Meta:
        model = TuberiaInstalacionBomba
        exclude = (
            "pk",
            "instalacion"
        )

EspecificacionesInstalacionFormSet = forms.modelformset_factory(EspecificacionesInstalacion, form=EspecificacionesInstalacionForm, min_num=2, max_num=2)
TuberiaFormSet = forms.modelformset_factory(TuberiaInstalacionBomba, form=TuberiaInstalacionBombaForm, min_num=1, extra=0)
