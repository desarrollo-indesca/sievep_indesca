from django.db import models

class Planta(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "planta"

class Area(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    planta = models.ForeignKey(Planta, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "area"

class Intercambiador(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=50)

    class Meta:
        db_table = "intercambiador"

class Fluido(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=5, unique=True)

    class Meta:
        db_table = "fluido"

class CondicionesDiseno(models.Model):
    id = models.AutoField(primary_key=True)
    intercambiador = models.OneToOneField(Intercambiador, on_delete=models.DO_NOTHING)

    fluido_servicio = models.ForeignKey(Fluido, verbose_name="Fluido Lado Servicio", on_delete=models.DO_NOTHING)
    temp_in_carcasa = models.DecimalField(max_digits=7, decimal_places=4, verbose_name="Temp. IN [°C] - Lado Carcasa")
    temp_out_carcasa = models.DecimalField(max_digits=7, decimal_places=4, verbose_name="Temp. OUT [°C] - Lado Carcasa")
    temp_in_tubo = models.DecimalField(max_digits=7, decimal_places=4, verbose_name="Temp. IN [°C] - Lado Tubo")
    temp_out_tubo = models.DecimalField(max_digits=7, decimal_places=4, verbose_name="Temp. OUT [°C] - Lado tubo")
    cp_carcasa = models.DecimalField(max_digits=6, decimal_places=4,null=True, verbose_name="cp [Kcal/Kg°C] - Lado Carcasa")
    cp_tubo = models.DecimalField(max_digits=5, decimal_places=4, verbose_name="cp [Kcal/Kg°C] - Lado Tubo")
    q = models.DecimalField(max_digits=11, decimal_places=4, verbose_name="Q [Kcal/h]")
    lmtd = models.DecimalField(max_digits=7, decimal_places=4, verbose_name="LMTD")
    ua = models.DecimalField(max_digits=11, decimal_places=4, verbose_name="UA [kcal/h.C]")
    area = models.DecimalField(max_digits=7, decimal_places=4, verbose_name="Área m²")
    u = models.DecimalField(max_digits=9, decimal_places=4, verbose_name="U [kcal/h.C.m²]")
    ntu = models.DecimalField(max_digits=5, decimal_places=4, verbose_name="NTU")
    efectividad = models.DecimalField(max_digits=5, decimal_places=4, verbose_name="Efectividad [ԑ]")
    eficiencia = models.DecimalField(max_digits=8, decimal_places=4, verbose_name="Eficiencia [Ѱ] [%]")
    flujo_agua = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Flujo de agua/unidad [Kg/h]")
    flujo_proceso = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Flujo de proceso/unidad [Kg/h]")
    
    numero_carcasas = models.DecimalField(max_digits=4, decimal_places=2,verbose_name="No. carcasas/unidad")
    area_carcasas = models.DecimalField(max_digits=4, decimal_places=2,verbose_name="Área/carcasa")
    carcasas_calculadas = models.DecimalField(max_digits=4, decimal_places=2,verbose_name="Carcasas Calculadas")
    pasos_carcasa = models.DecimalField(max_digits=4, decimal_places=2,verbose_name="No. Pasos/Carcasa")
    entradas_agua = models.DecimalField(max_digits=4, decimal_places=2,verbose_name="No. Entradas de Agua/Unidad")

    class Meta:
        db_table = "condiciones_diseno"

class CondicionesMaximas(models.Model):
    id = models.AutoField(primary_key=True)
    intercambiador = models.OneToOneField(Intercambiador, on_delete=models.DO_NOTHING)

    fluido_servicio = models.ForeignKey(Fluido, verbose_name="Fluido Lado Servicio", on_delete=models.DO_NOTHING)
    temp_in_carcasa = models.DecimalField(max_digits=7, decimal_places=4, verbose_name="Temp. IN [°C] - Lado Carcasa")
    temp_out_carcasa = models.DecimalField(max_digits=7, decimal_places=4, verbose_name="Temp. OUT [°C] - Lado Carcasa")
    temp_in_tubo = models.DecimalField(max_digits=7, decimal_places=4, verbose_name="Temp. IN [°C] - Lado Tubo")
    temp_out_tubo = models.DecimalField(max_digits=7, decimal_places=4, verbose_name="Temp. OUT [°C] - Lado tubo")
    cp_prom_carcasa = models.DecimalField(max_digits=6, decimal_places=4,null=True, verbose_name="cp prom. [Kcal/Kg°C] - Lado Carcasa")
    cp_prom_tubo = models.DecimalField(max_digits=5, decimal_places=4, verbose_name="cp prom. [Kcal/Kg°C] - Lado Tubo")
    q = models.DecimalField(max_digits=11, decimal_places=4, verbose_name="Q [Kcal/h]")
    lmtd = models.DecimalField(max_digits=7, decimal_places=4, verbose_name="LMTD")
    ua = models.DecimalField(max_digits=11, decimal_places=4, verbose_name="UA [kcal/h.C]")
    area = models.DecimalField(max_digits=7, decimal_places=4, verbose_name="Área m²")
    u = models.DecimalField(max_digits=9, decimal_places=4, verbose_name="U [kcal/h.C.m²]")
    ntu = models.DecimalField(max_digits=5, decimal_places=4, verbose_name="NTU")
    efectividad = models.DecimalField(max_digits=5, decimal_places=4, verbose_name="Efectividad [ԑ]")
    eficiencia = models.DecimalField(max_digits=8, decimal_places=4, verbose_name="Eficiencia [Ѱ] [%]")
    flujo_agua = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Flujo de agua/unidad [Kg/h]")
    flujo_proceso = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Flujo de proceso/unidad [Kg/h]")
    
    numero_carcasas = models.DecimalField(max_digits=4, decimal_places=2,verbose_name="No. carcasas/unidad")
    area_carcasas = models.DecimalField(max_digits=4, decimal_places=2,verbose_name="Área/carcasa")
    carcasas_calculadas = models.DecimalField(max_digits=4, decimal_places=2,verbose_name="Carcasas Calculadas")
    pasos_carcasa = models.DecimalField(max_digits=4, decimal_places=2,verbose_name="No. Pasos/Carcasa")
    entradas_agua = models.DecimalField(max_digits=4, decimal_places=2,verbose_name="No. Entradas de Agua/Unidad")

    class Meta:
        db_table = "condiciones_maximas"

class ParametrosDiseno(models.Model):
    id = models.AutoField(primary_key=True)
    intercambiador = models.OneToOneField(Intercambiador, on_delete=models.DO_NOTHING)

    longitud_tubo = models.DecimalField(max_digits=8, decimal_places=2,verbose_name="Longitud del tubo (m)")
    factor_ensuciamiento = models.DecimalField(max_digits=8, decimal_places=7,verbose_name="Factor de ensuciamiento [h.m2.ºC/Kcal] (Lado Tubo y Carcasa)")
    diametro_in_carcasa = models.DecimalField(max_digits=5, decimal_places=2,verbose_name="Diámetro interno carcasa [mm]")
    diametro_ex_carcasa = models.DecimalField(max_digits=5, decimal_places=2,verbose_name="Diámetro externo carcasa [mm]")
    usucio = models.DecimalField(max_digits=6, decimal_places=2,verbose_name="Usucio  [kcal/h.C.m2] (condiciones de diseño)")
    efectividad = models.DecimalField(max_digits=6, decimal_places=5,verbose_name="Efectividad [ԑ] (condiciones de diseño)")
    ntu = models.DecimalField(max_digits=6, decimal_places=5,verbose_name="NTU (condiciones máximas)")
    eficiencia = models.DecimalField(max_digits=5, decimal_places=2,verbose_name="Eficiencia [Ѱ] (condiciones máximas) [%]")
    material_tubos = models.CharField(max_length=50, verbose_name="Material de los Tubos")
    conductividad = models.DecimalField(max_digits=8, decimal_places=2, null=True, verbose_name="Conductividad")
    diametro_ex_tubos = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Diámetro externo tubos [mm]")
    diametro_in_tubos = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Diámetro interno tubos [mm]")
    espesor_tubos = models.DecimalField(max_digits=8, decimal_places=4, verbose_name="Espesor de los Tubos [mm]")
    numero_tubos = models.DecimalField(max_digits=8, decimal_places=2, null=True, verbose_name="Número de tubos")
    arreglo_tubos = models.DecimalField(max_digits=8, decimal_places=2, null=True, verbose_name="Arreglo de los tubos [mm]")
    pitch = models.DecimalField(max_digits=8, decimal_places=2, null=True, verbose_name="Pitch [mm]")
    ensuciamiento_calculado = models.DecimalField(max_digits=8, decimal_places=4, null=True, verbose_name="Ensuciamiento Calculado")

    class Meta:
        db_table = "parametros_diseno"