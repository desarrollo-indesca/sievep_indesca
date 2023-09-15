from django.db import models

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

# Modelos para Filtrado
class Complejo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = "complejo"

class Planta(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    complejo = models.ForeignKey(Complejo, on_delete=models.DO_NOTHING)

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
    codigo = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = "tema"

# Modelo de Fluido para Equipos
class Fluido(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40)
    formula = models.CharField(max_length=25,null=True)

    peso_molecular = models.DecimalField(max_digits=6, decimal_places=3)
    estado = models.CharField(max_length=1, choices=estados_fluidos)
    unidad = models.ForeignKey(Unidades, on_delete=models.DO_NOTHING)

    # Constantes Termodinámicas
    a = models.DecimalField(max_digits=6, decimal_places=3)
    b = models.DecimalField(max_digits=8, decimal_places=7)
    c = models.DecimalField(max_digits=12, decimal_places=11)
    d = models.DecimalField(max_digits=12, decimal_places=11)

    minimo = models.IntegerField()
    maximo = models.IntegerField()

    def cp(self, t):
        a = self.a
        b = self.b
        c = self.c
        d = self.d

        return a + b*t + c*t**2 + d*t**3

    class Meta:
        db_table = "fluido"

# Específicos de Intercambiadores
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

    class Meta:
        db_table = "intercambiador"

class TiposDeTubo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25)

    class Meta:
        db_table = "tipos_de_tubo"

class PropiedadesTuboCarcasa(models.Model):
    id = models.AutoField(primary_key=True)
    intercambiador = models.OneToOneField(Intercambiador, related_name="datos_tubo_carcasa", on_delete=models.DO_NOTHING)

    # Datos del área
    area = models.DecimalField(max_digits=12, decimal_places=5)
    numero_tubos = models.IntegerField(null=True)
    longitud_tubos = models.IntegerField(null=True)
    od_tubos = models.IntegerField(null=True)

    # Datos Carcasa
    id_carcasa = models.IntegerField(null=True)
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
    fabricante_tubo = models.TextField(null=True, max_length=100)

    # Generales
    criticidad = models.CharField(choices=criticidades, max_length=1)
    arreglo_serie = models.IntegerField()
    arreglo_paralelo = models.IntegerField()
    numero_pasos = models.IntegerField()

    # Datos calculados
    q = models.DecimalField(max_digits=10, decimal_places=3)
    u = models.DecimalField(max_digits=10, decimal_places=3)
    ensuciamiento = models.DecimalField(max_digits=10, decimal_places=3)

    class Meta:
        db_table = "intercambiador_tubo_carcasa"

class CondicionesTuboCarcasa(models.Model):
    intercambiador = models.ForeignKey(PropiedadesTuboCarcasa, on_delete=models.DO_NOTHING)
    lado = models.TextField(max_length=1, choices=(('T', 'Tubo'), ('C', 'Carcasa')))
    
    temp_entrada = models.DecimalField(max_digits=7, decimal_places=2) # Celsius
    temp_salida = models.DecimalField(max_digits=7, decimal_places=2) # Celsius
    flujo_masico = models.DecimalField(max_digits=12, decimal_places=5) # Kg/h
    
    flujo_vapor_entrada = models.DecimalField(max_digits=12, decimal_places=5, default=0) # Kg/h
    flujo_vapor_salida = models.DecimalField(max_digits=12, decimal_places=5, default=0) # Kg/h

    flujo_liquido_salida = models.DecimalField(max_digits=12, decimal_places=5, default=0) # Kg/h
    flujo_liquido_salida = models.DecimalField(max_digits=12, decimal_places=5, default=0) # Kg/h
    
    cambio_de_fase  = models.CharField(max_length=1, choices=cambios_de_fase)

    presion_entrada = models.DecimalField(max_digits=10, decimal_places=4) # barg
    caida_presion_max = models.DecimalField(max_digits=7, decimal_places=5)
    caida_presion_min = models.DecimalField(max_digits=7, decimal_places=5)
    fouling = models.DecimalField(max_digits=10, decimal_places=9) #m^2*C/W

    class Meta:
        db_table = "condiciones_tubo_carcasa"

class EvaluacionesIntercambiador(models.Model):
    fecha = models.DateTimeField(auto_now=True)
    intercambiador = models.ForeignKey(Intercambiador, on_delete=models.CASCADE)
    condiciones = models.ForeignKey(CondicionesTuboCarcasa, on_delete=models.DO_NOTHING)
    metodo = models.CharField(max_length=1, choices=(('E', 'Método Efectividad-NTU'), ('L', 'Método LMTD')))

    # Datos de Entrada
    temp_ex_entrada = models.DecimalField(max_digits=7, decimal_places=2) # Celsius
    temp_ex_salida = models.DecimalField(max_digits=7, decimal_places=2) # Celsius
    temp_in_entrada = models.DecimalField(max_digits=7, decimal_places=2) # Celsius
    temp_in_salida = models.DecimalField(max_digits=7, decimal_places=2) # Celsius
    flujo_masico_ex = models.DecimalField(max_digits=12, decimal_places=5) # Kg/h
    flujo_masico_in = models.DecimalField(max_digits=12, decimal_places=5) # Kg/h
    presion_inicial = models.DecimalField(max_digits=10, decimal_places=3)
    presion_final = models.DecimalField(max_digits=10, decimal_places=3)

    # Datos de Salida
    lmtd = models.DecimalField(max_digits=12, decimal_places=5)
    area_transferencia = models.DecimalField(max_digits=12, decimal_places=5)
    u = models.DecimalField(max_digits=12, decimal_places=5) # Kcal/h.C.m^2
    ua = models.DecimalField(max_digits=12, decimal_places=5) # Kcal/h.C
    ntu = models.DecimalField(max_digits=12, decimal_places=5)
    efectividad = models.DecimalField(max_digits=12, decimal_places=5)
    eficiencia = models.DecimalField(max_digits=12, decimal_places=5)
    ensuciamiento = models.DecimalField(max_digits=12, decimal_places=5)
    q = models.DecimalField(max_digits=12, decimal_places=5)

    class Meta:
        db_table = "evaluaciones_intercambiadores"