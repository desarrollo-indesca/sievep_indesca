import math
from calculos.unidades import transformar_unidades_longitud, transformar_unidades_viscosidad, transformar_unidades_densidad, transformar_unidades_presion, transformar_unidades_flujo_volumetrico
from calculos.termodinamicos import DENSIDAD_DEL_AGUA_LIQUIDA_A_5C,calcular_densidad, calcular_densidad_aire, calcular_presion_vapor, calcular_viscosidad

GRAVEDAD = 9.81

def calcular_eficiencia(potencia_real: float, potencia_calculada: float):
    '''
    Resumen:
        Función para el cálculo de la eficiencia.

    Parámetros:
        potencia_real: float (W) -> Potencia real del equipo
        potencia_calculada: float (W) ->Potencia real del equipo

    Devuelve:
        float (%) -> Porcentaje de eficiencia del equipo 
    '''
    return potencia_calculada/potencia_real*100

def calcular_areas(tramos, id):
    '''
    Resumen:
        Función para el cálculo de las áreas de cada tramo.

    Parámetros:
        tramos: QuerySet -> Tramos de tuberías del lado ordenados por PK
        id: float (m) -> Diámetro interno de la succión o la descarga en caso de que no hayan tramos

    Devuelve:
        list[float (m2)] -> Áreas de cada tramo 
    '''

    areas = []
    if(tramos.count()):
        for tramo in tramos:
            diametro = transformar_unidades_longitud([tramo.diametro_tuberia], tramo.diametro_tuberia_unidad.pk)[0]
            areas.append(math.pi/4*diametro**2)
    else:
        areas.append(math.pi/4*id**2)

    return areas

def calcular_velocidades(flujo, areas):
    '''
    Resumen:
        Función para el cálculo de velocidades por tramo y área.

    Parámetros:
        flujo: float (m3/s) -> Flujo circulante por la bomba
        areas: list[float (m2)] -> Área de cada tramo

    Devuelve:
        float (RPM) -> Velocidad específica de la bomba 
    '''
    return [flujo/area for area in areas]

def calcular_numero_reynolds(velocidad, diametro, densidad, viscosidad):
    '''
    Resumen:
        Cálculo del número de Reynolds de UN SOLO tramo

    Parámetros:
        velocidad: float (m/s) -> Velocidad del tramo
        diametro: float (m) -> Diámetro de la tubería del tramo
        densidad: float (Kg/m3) -> Densidad del fluido
        viscosidad: float (Kg/m3) -> Viscosidad del fluido

    Devuelve:
        float -> Número de Reynolds del tramo 
    '''
    return velocidad*diametro*densidad/viscosidad

def calcular_numeros_reynolds(velocidades, tramos, densidad, viscosidad):
    '''
    Resumen:
        Función para el cálculo de los números de Reynolds correspondientes a cada tramo

    Parámetros:
        velocidades: list[float (m/s)] -> Velocidades de cada tramo
        tramos: QuerySet -> Tramos de tuberías
        densidad: float (Kg/m3) -> Densidad del fluido circulante
        viscosidad: flaot (Pa.s) -> Viscosidad del fluido circulante

    Devuelve:
        list[float] -> Número de Reynolds de cada tramo de tubería 
    '''

    res = []
    for i,tramo in enumerate(tramos):
        diametro = transformar_unidades_longitud([tramo.diametro_tuberia], tramo.diametro_tuberia_unidad.pk)[0]
        res.append(calcular_numero_reynolds(velocidades[i], diametro, densidad, viscosidad))
    
    return res

def calcular_factor_friccion(flujo, numero_reynolds, diametro, rugosidad):
    '''
    Resumen:
        Función para el cálculo del factor de fricción de un tramo de tubería.

    Parámetros:
        flujo: str -> Tipo de flujo del tramo
        numero_reynolds: float -> Número de Reynolds del flujo del tramo
        diametro: float (m) -> Diámetro de la tubería que corresponde al tramo
        rugosidad: float -> Factor de rugosidad del material de la tubería del tramo

    Devuelve:
        float -> Factor de fricción calculado 
    '''
    if(flujo == 'L'): # Flujo Laminar
        return 64/numero_reynolds
    else: # Flujo Transitorio o Turbulento
        return 0.25/(math.log10(1/(3.7*diametro/rugosidad)+5.74/numero_reynolds**0.9))**2

def calcular_flujo_bomba(tramos, numeros_reynolds, velocidades):
    '''
    Resumen:
        Función para el cálculo de los datos de cada flujo por tramo de tubería.

    Parámetros:
        tramos: QuerySet -> Tramos del lado del cual se están calculando las pérdidas ordenados por PK.
        numeros_reynolds: list[float] -> Números de reynolds de cada tramo
        velocidades: list[float (RPM)] -> Velocidades de cada tramo

    Devuelve:
        list[dict] -> Lista con los datos de flujo de cada tramo de tubería del lado correspondiente 
    '''

    res = []
    for i,tramo in enumerate(tramos):
        numero_reynolds = numeros_reynolds[i]
        diametro = transformar_unidades_longitud([tramo.diametro_tuberia], tramo.diametro_tuberia_unidad.pk)[0]
        
        tipo_flujo = 'L' if numero_reynolds < 2000 else 'T' if numero_reynolds > 4000 else 'R'
        
        factor_friccion = calcular_factor_friccion(tipo_flujo, numero_reynolds, diametro, tramo.material_tuberia.rugosidad)
        factor_turbulento = 0.25/(math.log10(1/(3.7*diametro/tramo.material_tuberia.rugosidad)))**2

        res.append({
            'diametro': tramo.diametro_tuberia,
            'diametro_unidad': tramo.diametro_tuberia_unidad.simbolo,
            'longitud': tramo.longitud_tuberia,
            'longitud_unidad': tramo.longitud_tuberia_unidad.simbolo,            
            'tipo_flujo': tipo_flujo,
            'factor_friccion': factor_friccion,
            'factor_turbulento': factor_turbulento,
            'velocidad': velocidades[i]
        })

    return res

def calcular_cabezal(densidad, presion_descarga, presion_succion, altura_descarga, altura_succion, flujo, area_descarga, area_succion, htotal):
    '''
    Resumen:
        Función para el cálculo del cabezal de la bomba.

    Parámetros:
        densidad: float (Kg/m3) -> Densidad volumétrica del fluido circulante
        presion_descarga: float (Pa) -> Presión del lado de la descarga
        presion_succion: float (Pa) -> Presión del lado de la succión
        altura_descarga: float (m) -> Altura del lado de la descarga
        altura_succion: float (m) -> Altura del lado de la succión
        flujo: float (m3/s) -> Flujo circulante por la bomba
        area_descarga: float (m2) -> Área total del lado de la descarga
        area_succion: float (m2) -> Área total del lado de la succión
        htotal: float (m) -> Pérdidas totales

    Devuelve:
        float (m) -> Cabezal calculado 
    '''
    return (1/(densidad*GRAVEDAD)*(presion_descarga - presion_succion) + (altura_descarga - altura_succion) + flujo**2/(2*GRAVEDAD)*(1/area_descarga**2 - 1/area_succion**2) + htotal)

def calculo_perdida_tramos(tramos, velocidades, areas, area_comp, flujos):
    '''
    Resumen:
        Función para el cálculo de las pérdidas por tramo.

    Parámetros:
        tramos: QuerySet -> Tramos del lado del cual se están calculando las pérdidas ordenados por PK.
        velocidades: list[float (m/s)] -> Lista de las velocidades de los tramos
        areas: list[float (m2)] -> Lista de las áreas de los tramos
        area_comp: list[float (m2)] -> Áreas de comparación (descarga)
        flujos: list[str] -> Tipos de flujo por tramo

    Devuelve:
        [float (m), float (m)] -> Pérdida por Tubería y Pérdida por Accesorios
    '''

    ec = 0
    k,h,ft = 0,0,0
    diametro_previo = 0
    h_accesorios = 0

    area_comp = sum(area_comp) # Suma del área de comparación

    for i,tramo in enumerate(tramos): # Cálculo de las pérdidas por tramo
        k = 0
        ec = velocidades[i]**2/(2*GRAVEDAD) # Energía cinética
        longitud = transformar_unidades_longitud([tramo.longitud_tuberia], tramo.longitud_tuberia_unidad.pk)[0]
        diametro = transformar_unidades_longitud([tramo.diametro_tuberia], tramo.diametro_tuberia_unidad.pk)[0]
        
        if(diametro_previo == 0):
            diametro_previo = diametro
        
        h += flujos[i]['factor_friccion']*(longitud/diametro)*ec
        k += 340*tramo.numero_valvula_globo if tramo.numero_valvula_globo else 0
        k += 150*tramo.numero_valvula_angulo if tramo.numero_valvula_angulo else 0
        k += 8*tramo.numero_valvulas_compuerta if tramo.numero_valvulas_compuerta else 0
        k += 35*tramo.numero_valvulas_compuerta_abierta_3_4 if tramo.numero_valvulas_compuerta_abierta_3_4 else 0
        k += 160*tramo.numero_valvulas_compuerta_abierta_1_2 if tramo.numero_valvulas_compuerta_abierta_1_2 else 0
        k += 900*tramo.numero_valvulas_compuerta_abierta_1_4 if tramo.numero_valvulas_compuerta_abierta_1_4 else 0
        k += 100*tramo.numero_valvula_giratoria if tramo.numero_valvula_giratoria else 0
        k += 150*tramo.numero_valvula_bola if tramo.numero_valvula_bola else 0
        k += 45*tramo.numero_valvulas_mariposa_2_8 if tramo.numero_valvulas_mariposa_2_8 else 0
        k += 35*tramo.numero_valvulas_mariposa_10_14 if tramo.numero_valvulas_mariposa_10_14 else 0
        k += 25*tramo.numero_valvulas_mariposa_16_24 if tramo.numero_valvulas_mariposa_16_24 else 0
        k += 420*tramo.numero_valvula_vastago if tramo.numero_valvula_vastago else 0
        k += 75*tramo.numero_valvula_bisagra if tramo.numero_valvula_bisagra else 0
        k += 30*tramo.numero_codos_90 if tramo.numero_codos_90 else 0
        k += 20*tramo.numero_codos_90_rl if tramo.numero_codos_90_rl else 0
        k += 50*tramo.numero_codos_90_ros if tramo.numero_codos_90_ros else 0
        k += 16*tramo.numero_codos_45 if tramo.numero_codos_45 else 0
        k += 26*tramo.numero_codos_45_ros if tramo.numero_codos_45_ros else 0
        k += 50*tramo.numero_codos_180 if tramo.numero_codos_180 else 0
        k += 20*tramo.conexiones_t_directo if tramo.conexiones_t_directo else 0
        k += 60*tramo.conexiones_t_ramal if tramo.conexiones_t_ramal else 0
        k += 1 if i == 0 else 0 # Entrada / Salida (una vez por lado)
        ft = flujos[i]['factor_turbulento']

        if(diametro_previo < diametro):
            k += (1-(areas[i]/area_comp)**2)*diametro
        elif(diametro_previo > diametro):
            k += 0.5

        diametro_previo = diametro
   
        h_accesorios += ft*ec*k

    return [h, h_accesorios]

def determinar_cavitacion(npsha, npshr):
    '''
    Resumen:
        Función para determinar si la bomba está cavitando o no.

    Parámetros:
        npsha: float (m) -> NPSHa de la bomba
        npshr: float (m) -> NPSHr de la bomba

    Devuelve:
        str -> 'D' si no sabe, 'C' si está cavitando, 'N' si no. 
    '''
    return 'D' if npsha == None or npshr == None else 'N' if npsha > npshr else 'C'

def calcular_propiedades_termodinamicas_bomba(temp_operacion, presion_succion, condiciones_fluido):
    '''
    Resumen:
        Función para el cálculo de las propiedades termodinámicas a través de Thermo cuando se utiliza el tipo "A" de cálculos.
        Además realiza la transformación de fluidos no registrados.

    Parámetros:
        temp_operacion: float (Kelvin) -> Temperatura de operación para el cálculo.
        presion_succion: float (Pa) -> Presión del lado de la succión
        condiciones_fluido: CondicionesFluidoBomba -> Modelo del cual se extraerán las unidades de las propiedades de los fluidos a efectos de transformación.

    Devuelve:
        (float, float, float) -> Propiedades en orden (viscosidad, densidad, presion_vapor) 
    '''

    fluido = condiciones_fluido.fluido

    if(fluido): # Cálculo si el fluido existe
        viscosidad = calcular_viscosidad(fluido.cas, temp_operacion, presion_succion)[0]
        densidad = calcular_densidad(fluido.cas, temp_operacion, presion_succion)[0]
        presion_vapor = calcular_presion_vapor(fluido.cas, temp_operacion, presion_succion)
        return (viscosidad, densidad, presion_vapor)
    
    # Transformación a SI si el fluidop no existe
    viscosidad = transformar_unidades_viscosidad([condiciones_fluido.viscosidad], condiciones_fluido.viscosidad_unidad.pk)
    presion_vapor = transformar_unidades_presion([condiciones_fluido.presion_vapor], condiciones_fluido.presion_vapor_unidad.pk)
    densidad = transformar_unidades_presion([condiciones_fluido.densidad], condiciones_fluido.densidad_unidad.pk)

    return (viscosidad, densidad, presion_vapor)        

def obtener_propiedades(temp_operacion, presion_succion, bomba, propiedades, unidades_propiedades, tipo_propiedades):
    '''
    Resumen:
        Función para el cálculo de la velocidad específica de la bomba al momento de la evaluación.

    Parámetros:
        temp_operacion: float (Kelvin) -> Temperatura de operación
        presion_succion: float (Pa) -> Presión de la succión
        bomba: Bombas -> Bomba de la cual se obtendrán las propiedades
        propiedades: list -> Lista de propiedades en el orden indicado en la función principal
        unidades_propiedades: list ->  Unidades de las propiedades en orden
        tipo_propiedades: str -> Tipo de cálculo de propiedades

    Devuelve:
        (float, float, float) -> (densidad, presion_vapor, viscosidad) 
    '''

    if(tipo_propiedades == 'A'): # Cálculo Automático
        viscosidad, densidad, presion_vapor = calcular_propiedades_termodinamicas_bomba(temp_operacion, presion_succion, bomba.condiciones_diseno.condiciones_fluido)
    elif(tipo_propiedades == 'F'): # Obtención de datos por ficha
        fluido = bomba.condiciones_diseno.condiciones_fluido
        viscosidad = transformar_unidades_viscosidad([fluido.viscosidad], fluido.viscosidad_unidad.pk)[0]
        
        if(not fluido.densidad_unidad): # Densidad Relativa
            densidad = fluido.densidad * DENSIDAD_DEL_AGUA_LIQUIDA_A_5C
        else:
            densidad = transformar_unidades_densidad([fluido.densidad], fluido.densidad_unidad.pk)[0]
        
        presion_vapor = transformar_unidades_presion([fluido.presion_vapor], fluido.presion_vapor_unidad.pk)[0]
    elif(tipo_propiedades == 'M'): # Obtención de datos manual (ingresados por el usuario)
        viscosidad = transformar_unidades_viscosidad([float(propiedades[0])], int(unidades_propiedades[0]))[0]

        if(unidades_propiedades[1] == '' or not unidades_propiedades[1]):
            densidad = float(propiedades[1])*DENSIDAD_DEL_AGUA_LIQUIDA_A_5C # Densidad Relativa
        else:
            densidad = transformar_unidades_densidad([float(propiedades[1])], int(unidades_propiedades[1]))[0]
        
        presion_vapor = transformar_unidades_presion([float(propiedades[2])], int(unidades_propiedades[2]))[0]

    return (densidad, presion_vapor, viscosidad)

def construir_resultados_bomba(densidad, viscosidad, presion_vapor, cabezal, potencia_calculada,
                                eficiencia, ns, npsha, cavita, velocidades_succion, velocidades_descarga,
                                flujos_succion, flujos_descarga, h_succion_tuberia, h_succion_acc,
                                h_total_succion, h_descarga_tuberia, h_descarga_acc, h_total_descarga) -> dict:
    '''
    Resumen:
        Función que construye los resultados de la evaluación de una bomba en forma de diccionario para su interpretación del lado de la vista.

    Parámetros:
        densidad: float (m3/Kg) -> Densidad volumétrica del fluido circulante.
        viscosidad: float (Pa.s) -> Viscosidad dinámica calculada del fluido circulante
        presion_vapor: float (Pa) -> Presión de vapor del fluido circulante
        cabezal: float (m) -> Cabezal calculado
        potencia_calculada: float (W) -> Potencia calculada de la bomba
        eficiencia: float (%) -> Eficiencia calculada
        ns: float (RPM) -> Velocidad específica calculada
        npsha: float (m) -> NPSHa calculado
        cavita: str -> La bomba cavita: Sí ('S'), No ('N') o No se sabe ('D').
        velocidades_succion: list[float] -> Velocidades en cada tramo de las tuberías de la succión.
        velocidades_descarga: list[float] -> Velocidades en cada tramo de las tuberías de la descarga.
        flujos_succion: list[float] -> Tipo de flujo en cada tramo de la succión.
        flujos_descarga: list[float] -> Tipo de flujo en cada tramo de la descarga.
        h_succion_tuberia: list[float] -> Pérdidas por tubería en cada tramo de la succión.
        h_succion_acc: list[float] -> Pérdidas por accesorios en cada tramo de la succión.
        h_total_succion: list[float] -> Pérdidas totales (tubería+accesorios) en cada tramo de la succión.
        h_descarga_tuberia: list[float] -> Pérdidas por tubería en cada tramo de la descarga.
        h_descarga_acc: list[float] -> Pérdidas por accesorios en cada tramo de la descarga.
        h_total_descarga: list[float] -> Pérdidas totales (tubería+accesorios) en cada tramo de la descarga.

    Devuelve:
        dict -> Resultados de la evaluación en SI
    '''

    return {
        'propiedades': {
            'densidad': densidad,
            'viscosidad': viscosidad,
            'presion_vapor': presion_vapor
        },
        'cabezal_total': cabezal,
        'potencia_calculada': potencia_calculada,
        'eficiencia': eficiencia,
        'velocidad_especifica': ns,
        'npsha': npsha,
        'cavita': cavita,
        'velocidad': {
            's': velocidades_succion,
            'd': velocidades_descarga
        },
        'flujo': {
            's': flujos_succion,
            'd': flujos_descarga,
            't': '-'
        },
        'perdidas': {
            's': {
                'tuberia': h_succion_tuberia,
                'accesorio': h_succion_acc,
                'total': h_total_succion
            },
            'd': {
                'tuberia': h_descarga_tuberia,
                'accesorio': h_descarga_acc,
                'total': h_total_descarga
            },
            't': {
               'tuberia': h_succion_tuberia + h_descarga_tuberia,
               'accesorio': h_descarga_acc + h_succion_acc,
               'total': h_total_succion + h_total_descarga
            }
        }
    }

def calcular_ns(velocidad: float, flujo: float, cabezal: float):
    '''
    Resumen:
        Función para el cálculo de la velocidad específica de la bomba al momento de la evaluación.

    Parámetros:
        velocidad: float (RPM) -> Velocidad de la bomba en RPM
        flujo: float (m3/s) -> Flujo circulante por la bomba
        cabezal: float (m) -> Cabezal calculado de la bomba

    Devuelve:
        float (RPM) -> Velocidad específica de la bomba 
    '''

    flujo_gpm = transformar_unidades_flujo_volumetrico([flujo], 42, 48)[0]
    cabezal_ft = transformar_unidades_longitud([cabezal], 4, 14)[0]

    # RPM * sqrt(GPM) / ft**0.75
    ns = velocidad*math.sqrt(flujo_gpm)/(cabezal_ft)**0.75

    return ns

def evaluacion_bomba(bomba, velocidad, temp_operacion, presion_succion, presion_descarga, 
                     altura_succion, altura_descarga, diametro_interno_succion,
                     diametro_interno_descarga, flujo, potencia, npshr, tipo_propiedades,
                     propiedades = None, unidades_propiedades = None) -> dict:
    '''
    Resumen:
        Función para la evaluación de una bomba. A gran escala, toma los parámetros necesarios de la bomba y la evaluación,
        obtiene las propiedades termodinámicas del fluido según instrucciones del usuario, y hace los cálculos correspondientes
        a la evaluación de una bomba centrífuga.

        Todos los parámetros deben encontrarse en sistema internacional SI para devolver resultados concisos.

    Parámetros:
        bomba: Bombas -> Bomba a la cual se le realizará la evaluación.
        velocidad: float (RPM) -> Velocidad de la bomba (parámetro fijo).
        temp_operacion: float (Kelvin) -> Temperatura de operación de la bomba. Esencial para las propiedades termodinámicas.
        presion_succion: float (Pa) -> Presión del lado de la succión
        presion_descarga: float (Pa) -> Presión del lado de la descarga 
        altura_succion: float (m) -> Altura de la succión. Si no se tiene, asumir en 0.
        altura_descarga: float (m) -> Altura de la descarga. Si no se tiene, asumir en 0.
        diametro_interno_succion: float (m) -> Diámetro interno de la succión. Se utiliza si no hay tramos de tuberías registrados de este lado.
        diametro_interno_descarga: float (m) -> Diámetro interno de la descarga. Se utiliza si no hay tramos de tuberías registrados de este lado.
        flujo: float (m3/s) -> Flujo o Capacidad de la bomba
        potencia: float (W) -> Potencia al momento de la evaluación
        npshr: float (m) -> NPSHr de la bomba al momento de la evaluación. No es requerido, llenar con None.
        tipo_propiedades: str -> Tipo de cálculo de propiedades termodinámicas. Por ficha (F), automático (A) o manual (M).
        propiedades: list[float,float,float] = None -> Propiedades en orden [viscosidad, densidad, presion_vapor] del fluido en caso de haber sido ingresados manualmente.
        unidades_propiedades: list[str,str,str] = None -> Unidades de las propiedades en orden [unidad_viscosidad, unidad_densidad, unidad_presion_vapor] en caso de haber sido ingresados manualmente.

    Devuelve:
        dict -> Resultados de la evaluación en SI
    '''
    
    densidad, presion_vapor, viscosidad = obtener_propiedades(temp_operacion, presion_succion, bomba, propiedades, unidades_propiedades, tipo_propiedades)
    tramos_succion = bomba.instalacion_succion.tuberias.all().order_by('pk')
    tramos_descarga = bomba.instalacion_descarga.tuberias.all().order_by('pk')

    areas_succion, areas_descarga = calcular_areas(tramos_succion, diametro_interno_succion), calcular_areas(tramos_descarga, diametro_interno_descarga)
    velocidades_succion, velocidades_descarga = calcular_velocidades(flujo, areas_succion), calcular_velocidades(flujo, areas_descarga)

    nr_succion = calcular_numeros_reynolds(velocidades_succion, tramos_succion, densidad, viscosidad)
    nr_descarga = calcular_numeros_reynolds(velocidades_descarga, tramos_descarga, densidad, viscosidad)

    flujos_succion = calcular_flujo_bomba(tramos_succion, nr_succion, velocidades_succion)
    flujos_descarga = calcular_flujo_bomba(tramos_descarga, nr_descarga, velocidades_descarga)

    h_succion_tuberia, h_succion_acc = calculo_perdida_tramos(tramos_succion, velocidades_succion, areas_succion, areas_descarga, flujos_succion)
    h_descarga_tuberia, h_descarga_acc = calculo_perdida_tramos(tramos_descarga, velocidades_descarga, areas_descarga, areas_descarga, flujos_descarga)

    h_total_succion = h_succion_tuberia + h_succion_acc
    h_total_descarga = h_descarga_tuberia + h_descarga_acc
    htotal = h_total_succion + h_total_descarga

    cabezal = calcular_cabezal(densidad, presion_descarga, presion_succion, altura_succion, altura_descarga, flujo, sum(areas_descarga), sum(areas_succion), htotal)   
    potencia_calculada = cabezal*densidad*GRAVEDAD*flujo
    eficiencia = calcular_eficiencia(potencia, potencia_calculada)
    ns = calcular_ns(velocidad, flujo, cabezal)
    
    npsha = presion_succion/(densidad*GRAVEDAD) + altura_succion - presion_vapor/(densidad*GRAVEDAD) - h_total_succion
    cavita = determinar_cavitacion(npsha, npshr)
   
    res = construir_resultados_bomba(densidad, viscosidad, presion_vapor, cabezal, potencia_calculada,
                                eficiencia, ns, npsha, cavita, velocidades_succion, velocidades_descarga,
                                flujos_succion, flujos_descarga, h_succion_tuberia, h_succion_acc,
                                h_total_succion, h_descarga_tuberia, h_descarga_acc, h_total_descarga)

    return res

## EVALUACIONES DE VENTILADORES
def calcular_relacion_densidad(densidad_ficha: float, densidad_calculada: float):
    '''
    Resumen:
        Función para el cálculo de la relación de densidad para la evaluación del ventilador.

    Parámetros:
        densidad_ficha: float (Kg/m3) -> Densidad del aire por ficha. De no tenerse se asume el coeficiente en 1.
        densidad_calculada: float (Kg/m3) -> Densidad del aire calculada

    Devuelve:
        float -> Coeficiente de relación entre las densidades
    '''
    return densidad_ficha/densidad_calculada if densidad_ficha else 1.0

def calcular_potencia_ventilador(presion_entrada: float, presion_salida: float, relacion_densidad: float, flujo: float):
    '''
    Resumen:
        Función para el cálculo de la potencia del ventilador.

    Parámetros:
        presion_entrada: float (Pa) -> Presión de entrada
        presion_salida: float (Pa) -> Presión de salida
        relacion_densidad: float -> Relación de densidad
        flujo: float (m3/s) -> Flujo VOLUMÉTRICO que circula a través del ventilador

    Devuelve:
        float (W) -> Potencia calculada 
    '''
    
    return flujo * (presion_salida - presion_entrada) * relacion_densidad

def evaluar_ventilador(presion_entrada: float, presion_salida: float, flujo: float, tipo_flujo: str,
                        temperatura_operacion: float, potencia_real: float, densidad_ficha: float = None) -> float:
    '''
    Resumen:
        Función para evaluar un ventilador de acuerdo a los datos dados.

    Parámetros:
        presion_entrada: float (Pa) -> Presión de entrada (evaluación)
        presion_salida: float (Pa) -> Presión de salida (evaluación)
        flujo: float (m3/s) -> Flujo volumétrico que circula a través del ventilador (evaluación)
        temperatura_operacion: float (K) -> Temperatura de Operación (evaluación)
        potencia_real: float (W) -> Potencia real del ventilador (evaluación)
        densidad_ficha: float (Kg/m3) -> Densidad volumétrica especificada en ficha. No es obligatorio.

    Devuelve:
        float -> Coeficiente de relación entre las densidades
    '''
  
    densidad_calculada = calcular_densidad_aire(temperatura_operacion, presion_entrada + 101325)
    relacion_densidad = calcular_relacion_densidad(densidad_ficha, densidad_calculada)

    if(tipo_flujo == 'M'):
        flujo = flujo * densidad_calculada

    potencia_calculada = calcular_potencia_ventilador(presion_entrada, presion_salida, relacion_densidad, flujo)
    eficiencia = calcular_eficiencia(potencia_real, potencia_calculada)

    return {
        'relacion_densidad': round(relacion_densidad, 6),
        'potencia_calculada': round(potencia_calculada, 4),
        'eficiencia': round(eficiencia, 2),
        'densidad_calculada': round(densidad_calculada, 6),
        'tipo_flujo': tipo_flujo
    }

# TODO: FUNCIONES EVALUACIÓN PRECALENTADOR DE AGUA
# TODO: COMENTAR CALDERAS INDIRECTO