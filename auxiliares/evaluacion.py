import math
from calculos.unidades import transformar_unidades_longitud, transformar_unidades_viscosidad, transformar_unidades_densidad, transformar_unidades_presion
from calculos.termodinamicos import calcular_densidad, calcular_presion_vapor, calcular_viscosidad

GRAVEDAD = 9.81

def calcular_area(diametro):
    return math.pi/4*diametro

def calcular_velocidad(flujo, area):
    return flujo/area

def calcular_numero_reynolds(velocidad, diametro, densidad, viscosidad):
    return velocidad*diametro*densidad/viscosidad

def calcular_numeros_reynolds(velocidad, tramos, densidad, viscosidad):
    res = []
    for tramo in tramos:
        diametro = transformar_unidades_longitud([tramo.diametro_tuberia], tramo.diametro_tuberia_unidad.pk)[0]
        res.append(calcular_numero_reynolds(velocidad, diametro, densidad, viscosidad))
    
    return res

def calcular_factor_friccion(flujo, numero_reynolds, diametro, rugosidad):
    if(flujo == 'L'):
        return 64/numero_reynolds
    else:
        return 0.25/(math.log10(1/(3.7*diametro/rugosidad)+5.74/numero_reynolds**0.9))**2

def calcular_flujo_bomba(tramos, numeros_reynolds, diametro, rugosidad):
    res = []
    for i,tramo in enumerate(tramos):
        numero_reynolds = numeros_reynolds[i]
        diametro = transformar_unidades_longitud([tramo.diametro_tuberia], tramo.diametro_tuberia_unidad.pk)[0]
        tipo_flujo = 'L' if numero_reynolds < 2000 else 'T' if numero_reynolds > 4000 else 'R'
        factor_friccion = calcular_factor_friccion(tipo_flujo, numero_reynolds, diametro, tramo.material_tuberia.rugosidad)
        factor_turbulento = 0.25/(math.log10(1/(3.7*diametro/tramo.material_tuberia.rugosidad)))**2

        res.append({
            'tipo_flujo': tipo_flujo,
            'factor_friccion': factor_friccion,
            'factor_turbulento': factor_turbulento,
        })

    return res

def calculo_contracciones_expansiones(tramos):
    diametro = 0
    c,e = 0,0

    for tramo in tramos:
        actual = transformar_unidades_longitud([tramo.diametro_tuberia], tramo.diametro_tuberia_unidad.pk)[0]
        if(diametro == 0):
            diametro = actual
        elif(actual > diametro):
            e += 1
        elif(actual < diametro):
            c += 1
    
    return [c, e]

def calcular_cabezal(densidad, presion_descarga, presion_succion, altura_descarga, altura_succion, flujo, area_descarga, area_succion, htotal):
    return 1/(densidad*GRAVEDAD)*(presion_descarga - presion_succion) + (altura_descarga - altura_succion) + flujo**2/(2*GRAVEDAD)*(1/area_descarga**2 - 1/area_succion**2) + htotal

def calculo_perdida_tramos(tramos, velocidad, area, area_comp, flujos):
    ec = velocidad**2/(2*GRAVEDAD)
    c,e = calculo_contracciones_expansiones(tramos)
    k,h,ft = 0,0,0

    for i,tramo in enumerate(tramos):
        h += flujos[i]['factor_friccion']*(tramo.longitud_tuberia/tramo.diametro_tuberia)*(velocidad**2/2*GRAVEDAD)
        k += 340*tramo.numero_valvula_globo if tramo.numero_valvula_globo else 0
        k += 150*tramo.numero_valvula if tramo.numero_valvula else 0
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
        k += 0.5*c
        k += (1(area/area_comp)**2)*e*0
        k += 1 if i == 0 else 0 # Entrada / Salida
        ft += flujos[i]['factor_turbulento']
    
    h_accesorios = ft*ec*k

    return [h, h_accesorios]

def determinar_cavitacion(npsha, npshr):
    return 'D' if npsha == None or npshr == None else 'N' if npsha > npshr else 'C'

def calcular_propiedades_termodinamicas_bomba(temp_operacion, presion_succion, condiciones_fluido):
    fluido = condiciones_fluido.fluido 
    if(fluido):
        viscosidad = calcular_viscosidad(fluido.cas, temp_operacion, presion_succion)
        densidad = calcular_densidad(fluido.cas, temp_operacion, presion_succion)
        presion_vapor = calcular_presion_vapor(fluido.cas, temp_operacion, presion_succion)
        return (viscosidad, densidad, presion_vapor)

    viscosidad = transformar_unidades_viscosidad([condiciones_fluido.viscosidad], condiciones_fluido.viscosidad_unidad.pk)
    presion_vapor = transformar_unidades_presion([condiciones_fluido.presion_vapor], condiciones_fluido.presion_vapor_unidad.pk)
    densidad = transformar_unidades_presion([condiciones_fluido.densidad], condiciones_fluido.densidad_unidad.pk)

    return (viscosidad, presion_vapor, densidad)        

def evaluacion_bomba(bomba, velocidad, temp_operacion, presion_succion, presion_descarga, 
                     altura_succion, altura_descarga, diametro_interno_succion,
                     diametro_interno_descarga, flujo, potencia, npshr):
    
    # SE ASUMEN TODAS LAS UNIDADES EN SISTEMA INTERNACIONAL
    
    densidad, viscosidad, presion_vapor = calcular_propiedades_termodinamicas_bomba(temp_operacion, presion_succion, bomba.condiciones_diseno.condiciones_fluido)

    area_succion, area_descarga = calcular_area(diametro_interno_succion), calcular_area(diametro_interno_descarga)
    velocidad_succion, velocidad_descarga = calcular_velocidad(flujo, area_succion), calcular_velocidad(flujo, area_descarga)

    nr_succion = calcular_numeros_reynolds(velocidad_succion, bomba.instalacion_succion.tuberias, densidad, viscosidad)
    nr_descarga = calcular_numeros_reynolds(velocidad_descarga, bomba.instalacion_descarga.tuberias, densidad, viscosidad)

    flujos_succion = calcular_flujo_bomba(nr_succion, diametro_interno_succion)
    flujos_descarga = calcular_flujo_bomba(nr_descarga, diametro_interno_descarga)

    h_succion_tuberia, h_succion_acc = calculo_perdida_tramos(bomba.instalacion_succion.tuberias, velocidad_succion, area_succion, area_descarga, flujos_succion)
    h_descarga_tuberia, h_descarga_acc = calculo_perdida_tramos(bomba.instalacion_descarga.tuberias, velocidad_descarga, area_descarga, area_descarga, flujos_descarga)

    h_total_succion = h_succion_tuberia + h_succion_acc
    h_total_descarga = h_descarga_tuberia + h_descarga_acc
    htotal = h_total_succion + h_total_descarga

    cabezal = calcular_cabezal(densidad, presion_descarga, presion_succion, altura_succion, altura_descarga, flujo, area_descarga, area_succion, htotal)   
    
    potencia_calculada = cabezal*densidad*GRAVEDAD*flujo
    eficiencia = potencia_calculada/potencia*100
    ns = velocidad*math.sqrt(flujo*15850.35)/(cabezal*3.28)**0.75
    npsha = presion_succion/(densidad*GRAVEDAD) + altura_succion - presion_vapor/(densidad*GRAVEDAD) - h_total_succion
    cavita = determinar_cavitacion(npshr, npsha)
    
    res = {
        'cabezal_total': cabezal,
        'potencia_calculada': potencia_calculada,
        'eficiencia': eficiencia,
        'velocidad_especifica': ns,
        'npsha': npsha,
        'cavita': cavita,
        'reynolds': {
            's': nr_succion,
            'd': nr_descarga
        },
        'friccion': {
            's': sum([flujo['factor_friccion'] for flujo in flujos_succion]),
            'd': sum([flujo['factor_friccion'] for flujo in flujos_descarga])
        },
        'turbulento': {
            's': sum([flujo['factor_turbulento'] for flujo in flujos_succion]),
            'd': sum([flujo['factor_turbulento'] for flujo in flujos_descarga])
        },
        'flujo': {
            's': sum([flujo['tipo_flujo'] for flujo in flujos_succion]),
            'd': sum([flujo['tipo_flujo'] for flujo in flujos_descarga])
        }
    }

    return res
