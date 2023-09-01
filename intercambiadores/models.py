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

class Fluido(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=5, unique=True)
    nombre = models.CharField(max_length=25)

    class Meta:
        db_table = "fluido"

class Intercambiador(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    area = models.ForeignKey(Area, on_delete=models.DO_NOTHING)

    longitud_tubo = models.DecimalField(max_digits=8, decimal_places=2,verbose_name="Longitud del tubo (m)", null = True)
    factor_ensuciamiento = models.DecimalField(max_digits=8, decimal_places=7,verbose_name="Factor de ensuciamiento [h.m2.ºC/Kcal] (Lado Tubo y Carcasa)", null = True)
    diametro_in_carcasa = models.DecimalField(max_digits=5, decimal_places=2,verbose_name="Diámetro interno carcasa [mm]", null = True)
    diametro_ex_carcasa = models.DecimalField(max_digits=5, decimal_places=2,verbose_name="Diámetro externo carcasa [mm]", null = True)

    material_tubos = models.CharField(max_length=50, verbose_name="Material de los Tubos", null = True)
    conductividad = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Conductividad", null = True)
    diametro_ex_tubos = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Diámetro externo tubos [mm]", null = True)
    diametro_in_tubos = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Diámetro interno tubos [mm]", null = True)
    espesor_tubos = models.DecimalField(max_digits=8, decimal_places=4, verbose_name="Espesor de los Tubos [mm]", null = True)
    numero_tubos = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Número de tubos", null = True)
    arreglo_tubos = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Arreglo de los tubos [mm]", null = True)
    pitch = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Pitch [mm]", null = True)

    class Meta:
        db_table = "intercambiador"

class CondicionesSimulacionTubos(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=1, choices=(('D', 'Diseño'), ('M', 'Máximas')), default='D')
    intercambiador = models.ForeignKey(Intercambiador, on_delete=models.DO_NOTHING)
    fluido_servicio = models.ForeignKey(Fluido, on_delete=models.DO_NOTHING, related_name="fluido_servicio_diseno", verbose_name="Fluido Lado Servicio")
    fluido_interno = models.ForeignKey(Fluido, on_delete=models.DO_NOTHING, related_name="fluido_interno_diseno", verbose_name="Fluido Lado Interno")

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
        db_table = "condiciones_simulacion_tubos"

class ParametrosDiseno(models.Model):
    id = models.AutoField(primary_key=True)
    intercambiador = models.ForeignKey(Intercambiador, on_delete=models.DO_NOTHING)
    fluido_servicio = models.ForeignKey(Fluido, on_delete=models.DO_NOTHING, related_name="fluido_servicio_parametros", verbose_name="Fluido Lado Servicio")
    fluido_interno = models.ForeignKey(Fluido, on_delete=models.DO_NOTHING, related_name="fluido_interno_parametros", verbose_name="Fluido Lado Interno")

    usucio_diseno = models.DecimalField(max_digits=6, decimal_places=2,verbose_name="Usucio  [kcal/h.C.m2] (condiciones de diseño)", null = True)
    efectividad_diseno = models.DecimalField(max_digits=6, decimal_places=5,verbose_name="Efectividad [ԑ] (condiciones de diseño)", null = True)
    ntu_diseno = models.DecimalField(max_digits=6, decimal_places=5,verbose_name="NTU (condiciones máximas)", null = True)
    eficiencia_diseno = models.DecimalField(max_digits=5, decimal_places=2,verbose_name="Eficiencia [Ѱ] (condiciones máximas) [%]", null = True)
    usucio_maximas = models.DecimalField(max_digits=6, decimal_places=2,verbose_name="Usucio  [kcal/h.C.m2] (condiciones de diseño)", null = True)
    efectividad_maximas = models.DecimalField(max_digits=6, decimal_places=5,verbose_name="Efectividad [ԑ] (condiciones de diseño)", null = True)
    ntu_maximas = models.DecimalField(max_digits=6, decimal_places=5,verbose_name="NTU (condiciones máximas)", null = True)
    eficiencia_maximas = models.DecimalField(max_digits=5, decimal_places=2,verbose_name="Eficiencia [Ѱ] (condiciones máximas) [%]", null = True)

    class Meta:
        db_table = "parametros_diseno"

class SimulacionIntercambiador(models.Model):
    id = models.AutoField(primary_key=True)
    intercambiador = models.ForeignKey(Intercambiador, on_delete=models.DO_NOTHING)
    condiciones = models.ForeignKey(CondicionesSimulacionTubos, on_delete=models.DO_NOTHING, null=True)

    # Entrada

    fecha = models.DateTimeField(verbose_name="Fecha de la Simulación", null=True)

    temp_in_serv = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Temperatura de Entrada °C (Servicio)")
    temp_out_serv = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Temperatura de Salida °C (Servicio)")

    temp_in_proceso = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Temperatura de Entrada °C (Proceso)")
    temp_out_proceso = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Temperatura de Salida °C (Proceso)")

    flujo_interno = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Flujo Másico Total Kg/h (Proceso)")
    flujo_externo = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Flujo Másico Total Kg/h (Externo)")

    # Resultados

    lmtd = models.DecimalField(max_digits=9, decimal_places=4, verbose_name="LMTD")
    a_transferencia = models.DecimalField(max_digits=9, decimal_places=4, verbose_name="Área de Transferencia")
    u = models.DecimalField(max_digits=9, decimal_places=4, verbose_name="U [Kcal/h.°C.m2]")
    ua = models.DecimalField(max_digits=9, decimal_places=4, verbose_name="UA [Kcal/h.C]")
    ntu = models.DecimalField(max_digits=9, decimal_places=4, verbose_name="NTU")
    efectividad = models.DecimalField(max_digits=9, decimal_places=4, verbose_name="Efectividad")
    eficiencia = models.DecimalField(max_digits=9, decimal_places=4, verbose_name="Eficiencia")
    ensuciamiento = models.DecimalField(max_digits=9, decimal_places=4, verbose_name="Ensuciamiento")

    class Meta:
        db_table = "simulacion_intercambiador"
