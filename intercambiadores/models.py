from django.db import models
from django.contrib.auth import get_user_model

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
    ('S', 'Sin cambio de fase'),
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
    simbolo = models.CharField(max_length=5)
    valor = models.DecimalField(max_digits=10, decimal_places=5)
    tipo = models.CharField(max_length=1)

    class Meta:
        db_table = "unidades"

# Modelo de Tema de Equipo
class Tema(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(null=True)

    def __str__(self) -> str:
        return self.codigo.upper()

    class Meta:
        db_table = "tema"

# Modelo de Fluido para Equipos
class Fluido(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40)
    formula = models.CharField(max_length=25,null=True)

    peso_molecular = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    estado = models.CharField(max_length=1, choices=estados_fluidos)
    unidad_temperatura = models.ForeignKey(Unidades, on_delete=models.DO_NOTHING, null=True)

    # Constantes Termodinámicas
    a = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    b = models.DecimalField(max_digits=8, decimal_places=7, null=True)
    c = models.DecimalField(max_digits=12, decimal_places=11, null=True)
    d = models.DecimalField(max_digits=12, decimal_places=11, null=True)

    minimo = models.IntegerField(null=True)
    maximo = models.IntegerField(null=True)

    def cp(self, t):
        a = self.a
        b = self.b
        c = self.c
        d = self.d

        return a + b*t + c*t**2 + d*t**3

    def __str__(self) -> str:
        return self.nombre.upper()

    class Meta:
        db_table = "fluido"

# Específicos de Intercambiadores Tubo y Carcasa
class TipoIntercambiador(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = "tipo_intercambiador"

class Intercambiador(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=50, unique=True)
    tipo = models.ForeignKey(TipoIntercambiador, on_delete=models.DO_NOTHING)
    fabricante = models.CharField(max_length=45)
    planta = models.ForeignKey(Planta, on_delete=models.DO_NOTHING)
    tema = models.ForeignKey(Tema, on_delete=models.DO_NOTHING)
    servicio = models.CharField(max_length=100)
    arreglo_flujo = models.CharField(max_length=1, choices=arreglos_flujo)

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
    area = models.DecimalField(max_digits=12, decimal_places=5)
    area_unidad = models.ForeignKey(Unidades, on_delete=models.DO_NOTHING, related_name="area_unidad_tubocarcasa")

    numero_tubos = models.IntegerField(null=True)

    longitud_tubos = models.IntegerField(null=True)
    longitud_tubos_unidad = models.ForeignKey(Unidades, on_delete=models.DO_NOTHING, related_name="longitud_tubos_tubocarcasa")

    diametro_externo_tubos = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    diametro_interno_tubos = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    diametro_tubos_unidad = models.ForeignKey(Unidades, on_delete=models.DO_NOTHING, related_name="diametros_unidad_tubocarcasa")

    # Datos Carcasa
    fluido_carcasa = models.ForeignKey(Fluido, related_name="fluido_carcasa", on_delete=models.DO_NOTHING)
    material_carcasa = models.CharField(null=True, max_length=12)
    conexiones_entrada_carcasa = models.CharField(null=True, max_length=12)
    conexiones_salida_carcasa = models.CharField(null=True, max_length=12)

    # Datos Tubos
    material_tubo = models.CharField(null=True, max_length=12)
    fluido_tubo = models.ForeignKey(Fluido, related_name="fluido_tubo", on_delete=models.DO_NOTHING)
    tipo_tubo = models.ForeignKey(TiposDeTubo, on_delete=models.DO_NOTHING)
    conexiones_entrada_tubos = models.CharField(null=True, max_length=12)
    conexiones_salida_tubos = models.CharField(null=True, max_length=12)

    pitch_tubos = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    unidades_pitch = models.ForeignKey(Unidades, on_delete=models.DO_NOTHING, related_name="pitch_unidad_tubocarcasa")

    # Generales
    criticidad = models.CharField(choices=criticidades, max_length=1)
    arreglo_serie = models.IntegerField()
    arreglo_paralelo = models.IntegerField()
    numero_pasos_tubo = models.IntegerField(default=1)
    numero_pasos_carcasa = models.IntegerField(default=1)

    # Datos calculados
    q = models.DecimalField(max_digits=10, decimal_places=3)
    u = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    ensuciamiento = models.DecimalField(max_digits=10, decimal_places=3, null=True)

    def condicion_tubo(self):
        return self.condiciones.get(lado='T')
    
    def condicion_carcasa(self):
        return self.condiciones.get(lado='C')
    
    def criticidad_larga(self):
        for x in criticidades:
            if(x[0] == self.criticidad):
                return x[1]

    class Meta:
        db_table = "intercambiador_tubo_carcasa"
        ordering = ('intercambiador__tag',)

class CondicionesTuboCarcasa(models.Model):
    intercambiador = models.ForeignKey(PropiedadesTuboCarcasa, on_delete=models.DO_NOTHING, related_name="condiciones")
    lado = models.TextField(max_length=1, choices=(('T', 'Tubo'), ('C', 'Carcasa')))
    
    temp_entrada = models.DecimalField(max_digits=7, decimal_places=2)
    temp_salida = models.DecimalField(max_digits=7, decimal_places=2)
    temperaturas_unidad = models.ForeignKey(Unidades, on_delete=models.DO_NOTHING, related_name="temperaturas_condiciones_unidades_tubocarcasa", null=True)

    flujo_masico = models.DecimalField(max_digits=12, decimal_places=5)
    flujo_vapor_entrada = models.DecimalField(max_digits=12, decimal_places=5, null=True)
    flujo_vapor_salida = models.DecimalField(max_digits=12, decimal_places=5, null=True)
    flujo_liquido_entrada = models.DecimalField(max_digits=12, decimal_places=5, null=True)
    flujo_liquido_salida = models.DecimalField(max_digits=12, decimal_places=5, null=True)
    flujos_unidad = models.ForeignKey(Unidades, on_delete=models.DO_NOTHING, related_name="flujos_unidad_tubocarcasa", null=True)
    
    cambio_de_fase  = models.CharField(max_length=1, choices=cambios_de_fase)

    presion_entrada = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    caida_presion_max = models.DecimalField(max_digits=9, decimal_places=5, null=True)
    caida_presion_min = models.DecimalField(max_digits=9, decimal_places=5, null=True)
    unidad_presion = models.ForeignKey(Unidades, on_delete=models.DO_NOTHING, related_name="presion_unidad_tubocarcasa")

    fouling = models.DecimalField(max_digits=10, decimal_places=9, null=True) #m^2*C/W

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
    condiciones = models.ForeignKey(CondicionesTuboCarcasa, on_delete=models.DO_NOTHING)
    metodo = models.CharField(max_length=1, choices=(('E', 'Método Efectividad-NTU'), ('L', 'Método LMTD')))

    # Datos de Entrada
    temp_ex_entrada = models.DecimalField(max_digits=7, decimal_places=2)
    temp_ex_salida = models.DecimalField(max_digits=7, decimal_places=2)
    temp_in_entrada = models.DecimalField(max_digits=7, decimal_places=2)
    temp_in_salida = models.DecimalField(max_digits=7, decimal_places=2)
    temperaturas_unidad = models.ForeignKey(Unidades, on_delete=models.DO_NOTHING, related_name="temperatura_unidad_evaluacionintercambiador")

    flujo_masico_ex = models.DecimalField(max_digits=12, decimal_places=5) 
    flujo_masico_in = models.DecimalField(max_digits=12, decimal_places=5)
    unidad_flujo = models.ForeignKey(Unidades, on_delete=models.DO_NOTHING, related_name="flujo_unidad_evaluacionintercambiador")

    presion_inicial = models.DecimalField(max_digits=10, decimal_places=3)
    presion_final = models.DecimalField(max_digits=10, decimal_places=3)
    unidad_presion = models.ForeignKey(Unidades, on_delete=models.DO_NOTHING, related_name="presion_unidad_evaluacionintercambiador")

    # Datos de Salida
    lmtd = models.DecimalField(max_digits=12, decimal_places=5)
    area_transferencia = models.DecimalField(max_digits=12, decimal_places=5)
    u = models.DecimalField(max_digits=12, decimal_places=5)
    ua = models.DecimalField(max_digits=12, decimal_places=5) 
    ntu = models.DecimalField(max_digits=12, decimal_places=5)
    efectividad = models.DecimalField(max_digits=12, decimal_places=5)
    eficiencia = models.DecimalField(max_digits=12, decimal_places=5)
    ensuciamiento = models.DecimalField(max_digits=12, decimal_places=5)
    q = models.DecimalField(max_digits=12, decimal_places=5)
    numero_tubos = models.IntegerField()

    class Meta:
        db_table = "evaluaciones_intercambiadores"