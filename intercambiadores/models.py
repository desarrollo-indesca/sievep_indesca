from django.db import models
from django.contrib.auth import get_user_model
from calculos.evaluaciones import evaluacion_tubo_carcasa

# Tipos Estáticos

criticidades = [
    ('C', 'Crítico'),
    ('S', 'Semi Crítico'),
    ('N', 'No Crítico')
]

tipos_condiciones = [
    ('D', 'Diseño'),
    ('M', 'Máximas'),
    ('m', 'Mínimas'),
    ('P', 'Proceso'),
    ('p', 'Planta'),
    ('O', 'Otro')
]

cambios_de_fase = [
    ('S', 'Sin Cambio de Fase'),
    ('P','Cambio de Fase Parcial'),
    ('T', 'Cambio de Fase Total')
]

estados_fluidos = [
    ("L", "Líquido"),
    ("G", "Gaseoso")
]

tipos_unidades = [
    ("T", "Temperatura"),
    ("t", "Tiempo"),
    ("m", "Masa"),
    ("P", "Presión"),
    ("L", "Longitud")
]

arreglos_flujo = [
    ('C', 'Cocorriente'),
    ('c', 'Contracorriente'),
    ('M', 'Cruzado (Mezclado)'),
    ('m', 'Sin Mezclar')
]

# Modelos para Filtrado
class Complejo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.nombre

    class Meta:
        db_table = "complejo"

class Planta(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    complejo = models.ForeignKey(Complejo, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.nombre.upper()

    class Meta:
        db_table = "planta"

# Modelo de Unidades
class Unidades(models.Model):
    id = models.AutoField(primary_key=True)
    simbolo = models.CharField(max_length=10)
    tipo = models.CharField(max_length=1)

    def __str__(self):
        return self.simbolo

    class Meta:
        db_table = "unidades"

# Modelo de Fluido para Equipos
class Fluido(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40)
    cas = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.nombre.upper()

    class Meta:
        ordering = ('nombre',)
        db_table = "fluido"

class TipoIntercambiador(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = "tipo_intercambiador"

# Modelo de Tema de Equipo
class Tema(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(null=True)
    tipo_intercambiador = models.ForeignKey(TipoIntercambiador, on_delete=models.DO_NOTHING, default=1)

    def __str__(self) -> str:
        return self.codigo.upper()

    class Meta:
        db_table = "tema"

# Específicos de Intercambiadores Tubo y Carcasa
class Intercambiador(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=50, unique=True)
    tipo = models.ForeignKey(TipoIntercambiador, on_delete=models.DO_NOTHING)
    fabricante = models.CharField(max_length=45)
    planta = models.ForeignKey(Planta, on_delete=models.DO_NOTHING)
    tema = models.ForeignKey(Tema, on_delete=models.DO_NOTHING)
    servicio = models.CharField(max_length=100)
    arreglo_flujo = models.CharField(max_length=1, choices=arreglos_flujo)
    criticidad = models.CharField(max_length=1, choices=criticidades)

    def intercambiador(self):
        return PropiedadesTuboCarcasa.objects.get(intercambiador = self)
    
    def tema_final(self):
        return self.tema.codigo[2] if self.tema.codigo[2] != 'N' else 'N_2'
    
    def flujo_largo(self):
        for flujo in arreglos_flujo:
            if(flujo[0] == self.arreglo_flujo):
                return flujo[1]

    class Meta:
        db_table = "intercambiador"

class TiposDeTubo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.nombre.upper()

    class Meta:
        db_table = "tipos_de_tubo"

class PropiedadesTuboCarcasa(models.Model):
    id = models.AutoField(primary_key=True)
    intercambiador = models.OneToOneField(Intercambiador, related_name="datos_tubo_carcasa", on_delete=models.DO_NOTHING)

    # Datos del área
    area = models.DecimalField(max_digits=12, decimal_places=2)
    area_unidad = models.ForeignKey(Unidades, on_delete=models.DO_NOTHING, related_name="area_unidad_tubocarcasa")

    numero_tubos = models.IntegerField(null=True)

    longitud_tubos = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    longitud_tubos_unidad = models.ForeignKey(Unidades, on_delete=models.DO_NOTHING, related_name="longitud_tubos_tubocarcasa")

    diametro_externo_tubos = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    diametro_interno_tubos = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    diametro_tubos_unidad = models.ForeignKey(Unidades, on_delete=models.DO_NOTHING, related_name="diametros_unidad_tubocarcasa")

    # Datos Carcasa
    fluido_carcasa = models.ForeignKey(Fluido, related_name="fluido_carcasa", on_delete=models.DO_NOTHING, null=True)
    material_carcasa = models.CharField(null=True, max_length=50)
    conexiones_entrada_carcasa = models.CharField(null=True, max_length=50)
    conexiones_salida_carcasa = models.CharField(null=True, max_length=50)

    # Datos Tubos
    material_tubo = models.CharField(null=True, max_length=50)
    fluido_tubo = models.ForeignKey(Fluido, related_name="fluido_tubo", on_delete=models.DO_NOTHING, null=True)
    tipo_tubo = models.ForeignKey(TiposDeTubo, on_delete=models.DO_NOTHING)
    conexiones_entrada_tubos = models.CharField(null=True, max_length=50)
    conexiones_salida_tubos = models.CharField(null=True, max_length=50)

    pitch_tubos = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    unidades_pitch = models.ForeignKey(Unidades, on_delete=models.DO_NOTHING, related_name="pitch_unidad_tubocarcasa")

    # Generales
    arreglo_serie = models.IntegerField()
    arreglo_paralelo = models.IntegerField()
    numero_pasos_tubo = models.IntegerField(default=1)
    numero_pasos_carcasa = models.IntegerField(default=1)

    # Datos calculados
    q = models.DecimalField(max_digits=15, decimal_places=3)
    u = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    ensuciamiento = models.DecimalField(max_digits=12, decimal_places=9, null=True)

    q_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="unidad_q", default=28)
    u_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="unidad_u", default=27)
    ensuciamiento_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="unidad_ensuciamiento",default=31)

    def calcular_diseno(self):
        cond_tubo= self.condicion_tubo()
        cond_carcasa = self.condicion_carcasa()
        ti = float(cond_tubo.temp_entrada)
        ts = float(cond_tubo.temp_salida)
        Ti = float(cond_carcasa.temp_entrada)
        Ts = float(cond_carcasa.temp_salida)
        ft = float(cond_tubo.flujo_masico)
        fc = float(cond_carcasa.flujo_masico)

        fluido_cp_gas_tubo = float(cond_tubo.fluido_cp_gas) if cond_tubo.fluido_cp_gas else None
        fluido_cp_liquido_tubo = float(cond_tubo.fluido_cp_liquido) if cond_tubo.fluido_cp_liquido else None
        fluido_cp_gas_carcasa = float(cond_carcasa.fluido_cp_gas) if cond_carcasa.fluido_cp_gas else None
        fluido_cp_liquido_carcasa = float(cond_carcasa.fluido_cp_liquido) if cond_carcasa.fluido_cp_liquido else None

        return evaluacion_tubo_carcasa(self, ti, ts, Ti, Ts, ft, fc, 
            self.numero_tubos,  fluido_cp_gas_tubo, fluido_cp_liquido_tubo,
            fluido_cp_gas_carcasa, fluido_cp_liquido_carcasa,
            unidad_temp=cond_carcasa.temperaturas_unidad.pk, unidad_flujo=cond_carcasa.flujos_unidad.pk)

    def condicion_tubo(self):
        return self.intercambiador.condiciones.get(lado='T')
    
    def condicion_carcasa(self):
        return self.intercambiador.condiciones.get(lado='C')
    
    def criticidad_larga(self):
        for x in criticidades:
            if(x[0] == self.intercambiador.criticidad):
                return x[1]

    class Meta:
        db_table = "intercambiador_tubo_carcasa"
        ordering = ('intercambiador__tag',)

class CondicionesTuboCarcasa(models.Model):
    intercambiador = models.ForeignKey(Intercambiador, on_delete=models.CASCADE, related_name="condiciones")
    lado = models.TextField(max_length=1, choices=(('T', 'Tubo'), ('C', 'Carcasa')))
    
    temp_entrada = models.DecimalField(max_digits=7, decimal_places=2)
    temp_salida = models.DecimalField(max_digits=7, decimal_places=2)
    temperaturas_unidad = models.ForeignKey(Unidades, on_delete=models.DO_NOTHING, related_name="temperaturas_condiciones_unidades_tubocarcasa", null=True)

    flujo_masico = models.DecimalField(max_digits=10, decimal_places=2)
    flujo_vapor_entrada = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    flujo_vapor_salida = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    flujo_liquido_entrada = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    flujo_liquido_salida = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    flujos_unidad = models.ForeignKey(Unidades, on_delete=models.DO_NOTHING, related_name="flujos_unidad_tubocarcasa", null=True)
    fluido_etiqueta = models.CharField(null=True, max_length=50)
    tipo_cp = models.CharField(null=False, choices=[['M','Manual'],['A','Automático']], max_length=1)
    fluido_cp_liquido = models.DecimalField(null=True, max_digits=9, decimal_places=4)
    fluido_cp_gas = models.DecimalField(null=True, max_digits=9, decimal_places=4)
    hvap = models.DecimalField(max_digits=15, decimal_places=4, null=True)
    tsat = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    unidad_cp = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="unidad_cp", default=29)
    
    cambio_de_fase  = models.CharField(max_length=1, choices=cambios_de_fase)

    presion_entrada = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    caida_presion_max = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    caida_presion_min = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    unidad_presion = models.ForeignKey(Unidades, on_delete=models.DO_NOTHING, related_name="presion_unidad_tubocarcasa")

    fouling = models.DecimalField(max_digits=12, decimal_places=9, null=True) #m^2*C/W

    def cambio_fase_largo(self):
        for x in cambios_de_fase:
            if(x[0] == self.cambio_de_fase):
                return x[1]

    class Meta:
        db_table = "condiciones_tubo_carcasa"

# Modelo de Evaluaciones
class EvaluacionesIntercambiador(models.Model):
    creado_por = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
    fecha = models.DateTimeField(auto_now=True)
    intercambiador = models.ForeignKey(Intercambiador, on_delete=models.CASCADE)
    metodo = models.CharField(max_length=1, choices=(('E', 'Método Efectividad-NTU'), ('L', 'Método LMTD')))
    nombre = models.CharField(max_length=50)

    # Datos de Entrada
    temp_ex_entrada = models.DecimalField(max_digits=12, decimal_places=2)
    temp_ex_salida = models.DecimalField(max_digits=12, decimal_places=2)
    temp_in_entrada = models.DecimalField(max_digits=12, decimal_places=2)
    temp_in_salida = models.DecimalField(max_digits=12, decimal_places=2)
    temperaturas_unidad = models.ForeignKey(Unidades, on_delete=models.DO_NOTHING, related_name="temperatura_unidad_evaluacionintercambiador")

    flujo_masico_ex = models.DecimalField(max_digits=12, decimal_places=2) 
    flujo_masico_in = models.DecimalField(max_digits=12, decimal_places=2)
    unidad_flujo = models.ForeignKey(Unidades, on_delete=models.DO_NOTHING, related_name="flujo_unidad_evaluacionintercambiador")

    caida_presion_in = models.DecimalField(max_digits=10, decimal_places=2)
    caida_presion_ex = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_presion = models.ForeignKey(Unidades, on_delete=models.DO_NOTHING, related_name="presion_unidad_evaluacionintercambiador")

    cp_tubo_gas = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    cp_tubo_liquido = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    cp_carcasa_gas = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    cp_carcasa_liquido = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    tipo_cp_carcasa = models.CharField(max_length=1, choices=[['A', 'Automático'], ['M','Manual']])
    tipo_cp_tubo = models.CharField(max_length=1, choices=[['A', 'Automático'], ['M','Manual']])
    cp_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name="cp_unidad_evaluacionintercambiador", default=29)

    # Datos de Salida
    lmtd = models.DecimalField(max_digits=12, decimal_places=2)
    area_transferencia = models.DecimalField(max_digits=12, decimal_places=2)
    u = models.DecimalField(max_digits=15, decimal_places=4)    
    ua = models.DecimalField(max_digits=15, decimal_places=4) 
    ntu = models.DecimalField(max_digits=12, decimal_places=4)
    efectividad = models.DecimalField(max_digits=12, decimal_places=2)
    eficiencia = models.DecimalField(max_digits=12, decimal_places=2)
    ensuciamiento = models.DecimalField(max_digits=10, decimal_places=8)
    q = models.DecimalField(max_digits=12, decimal_places=3)
    numero_tubos = models.IntegerField()

    visible = models.BooleanField(default=True)

    def promedio_carcasa(self):
        return (self.temp_ex_entrada + self.temp_ex_salida)/2

    def promedio_tubo(self):
        return (self.temp_in_entrada + self.temp_in_salida)/2

    class Meta:
        db_table = "evaluaciones_intercambiadores"
        ordering = ('-fecha',)