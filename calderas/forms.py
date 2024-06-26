from django import forms
from .models import *
from auxiliares.forms import FormConUnidades
from intercambiadores.models import Complejo

# Forms Específicos

class FormConPresionYTemperatura(FormConUnidades):
    def limpiar_campos_unidades(self):
        self.fields["temperatura_unidad"].queryset = Unidades.objects.filter(tipo="T")
        self.fields["presion_unidad"].queryset = Unidades.objects.filter(tipo="P")

class FormConAreaYDiametro(FormConUnidades):
    def limpiar_campos_unidades(self):
        self.fields["area_unidad"].queryset = Unidades.objects.filter(tipo="A")
        self.fields["diametro_unidad"].queryset = Unidades.objects.filter(tipo="L")

# FORMS DE CALDERAS

class TamborForm(FormConPresionYTemperatura):
    class Meta:
        model = Tambor
        exclude = ["id"]

class SeccionTamborForm(FormConUnidades):
    def limpiar_campos_unidades(self):
        self.fields["dimensiones_unidad"].queryset = Unidades.objects.filter(tipo="L")

    class Meta:
        model = SeccionTambor
        exclude = ["id","tambor"]

class SobrecalentadorForm(FormConPresionYTemperatura):
    def limpiar_campos_unidades(self):
        super().limpiar_campos_unidades()
        self.fields["flujo_unidad"].queryset = Unidades.objects.filter(tipo="F")

    class Meta:
        model = Sobrecalentador
        exclude = ["id"]

class DimsSobrecalentadorForm(FormConAreaYDiametro):
    class Meta:
        model = DimsSobrecalentador
        exclude = ["id"]

class DimensionesCalderaForm(FormConUnidades):
    def limpiar_campos_unidades(self):
        self.fields["dimensiones_unidad"].queryset = Unidades.objects.filter(tipo="L")

    class Meta:
        model = DimensionesCaldera
        exclude = ["id"]

class EspecificacionesCalderaForm(FormConPresionYTemperatura):
    def limpiar_campos_unidades(self):
        super().limpiar_campos_unidades()
        self.fields["area_unidad"].queryset = Unidades.objects.filter(tipo="A")
        self.fields["calor_unidad"].queryset = Unidades.objects.filter(tipo="Q")
        self.fields["capacidad_unidad"].queryset = Unidades.objects.filter(tipo="F")
        self.fields["carga_unidad"].queryset = Unidades.objects.filter(tipo="F")

    class Meta:
        model = EspecificacionesCaldera
        exclude = ["id"]

class CombustibleForm(forms.ModelForm):
    class Meta:
        model = Combustible
        exclude = ["id"]

class ComposicionCombustibleForm(forms.ModelForm):
    class Meta:
        model = ComposicionCombustible
        exclude = ["id", "combustible"]

composicion_formset = forms.modelformset_factory(ComposicionCombustible, ComposicionCombustibleForm)

class ChimeneaForm(FormConUnidades):
    def limpiar_campos_unidades(self):
        super().limpiar_campos_unidades()
        self.fields["dimensiones_unidad"].queryset = Unidades.objects.filter(tipo="L")

    class Meta:
        model = Chimenea
        exclude = ["id"]

class EconomizadorForm(FormConAreaYDiametro):
    class Meta:
        model = Economizador
        exclude = ["id"]

class CalderaForm(forms.ModelForm):
    complejo = forms.ModelChoiceField(queryset=Complejo.objects.all(), empty_label=None)

    class Meta:
        model = Caldera
        exclude = ["id", "sobrecalentador", "tambor", "dimensiones",
                   "especificaciones", "combustible", "chimenea",
                   "economizador", "creado_por", "creado_al", 
                   "editado_por", "editado_al"]

class CaracteristicaForm(forms.ModelForm):
    class Meta:
        model = Caracteristica
        exclude = ["id", "caldera"]

class ValorPorCargaForm(forms.ModelForm):
    class Meta:
        model = ValorPorCarga
        exclude = ["id", "caracteristica"]
        
caracteristica_formset = forms.modelformset_factory(ValorPorCarga, ValorPorCargaForm)

class CorrienteForm(FormConUnidades):
    def limpiar_campos_unidades(self):
        self.fields["flujo_masico_unidad"].queryset = Unidades.objects.filter(tipo="F")
        self.fields["densidad_unidad"].queryset = Unidades.objects.filter(tipo="D")
        self.fields["temp_operacion_unidad"].queryset = Unidades.objects.filter(tipo="T")
        self.fields["presion_unidad"].queryset = Unidades.objects.filter(tipo="P")

    class Meta:
        model = Corriente
        exclude = ["id", "caldera"]

corriente_formset = forms.modelformset_factory(Corriente, CorrienteForm)

# FORMS EVALUACIÓN
class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion
        exclude = ["id", "salido_flujos", "salida_balance_molar",
                    "salida_fracciones", "salida_balance_energia",
                    "salida_lado_agua", "caldera", "usuario"]

class EntradasFluidosForm(forms.ModelForm):
    class Meta:
        model = EntradasFluidos
        exclude = ["id", "evaluacion"]

entradas_fluidos_formset = forms.modelformset_factory(EntradasFluidos, EntradasFluidosForm)

class EntradaComposicionForm(forms.ModelForm):
    class Meta:
        model = EntradaComposicion
        exclude = ["id", "composicion", "evaluacion"]