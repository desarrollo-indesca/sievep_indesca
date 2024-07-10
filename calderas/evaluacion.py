from thermo.chemical import Chemical
from CoolProp import CoolProp as CP

import math

COMPUESTOS_COMBUSTION = [
    Chemical('74-82-8'), Chemical('74-84-0'), Chemical('74-98-6'), 
    Chemical('75-28-5'), Chemical('106-97-8'), Chemical('78-78-4'), 
    Chemical('109-66-0'), Chemical('110-54-3'), Chemical('1333-74-0'), 
    Chemical('C10H22'), Chemical('7783-06-4')
]

COMPUESTOS_RESULTANTES_COMBUSTION = [
    Chemical('7782-44-7'), Chemical('124-38-9'), 
    Chemical('7732-18-5'), Chemical('7446-09-5')
]

MATRIZ_ESTEQUIOMETRICA = [
    [0, 2, 7/2, 5, 13/2, 13/2, 8, 8, 19/2, 1/2, 3/2 ],
	[0, 1,   2, 3,    4,    4, 5, 5,    6,   0, 0   ],
	[0, 2,   3, 4,    5,    5, 6, 6,    7,   1, 1   ],
	[0, 0,   0, 0,    0,    0, 0, 0,    0,   0, 1   ]
]

CALORES_COMBUSTION = {
    '74-82-8': -802.6,
    '74-84-0': -1428.6,
    '74-98-6': -2043.1,
    '75-28-5': -2649,
    '106-97-8': -2657.3,
    '78-78-4': -3239.5,
    '109-66-0': -3244.9,
    '110-54-3': -3855.1,
    '1333-74-0': -241.8,
    '7783-06-4': -518,
}

R=8.3145e-5

def obtener_moles_reaccion(composicion: list):
    moles = 0
    n = []
    especifico = 0
    for i in range(4):
        for j,compuesto in enumerate(composicion):
            moles[compuesto['cas']] = compuesto['x'] * MATRIZ_ESTEQUIOMETRICA[i][j] 
            especifico = compuesto['x'] * CALORES_COMBUSTION[compuesto['cas']]

        n[COMPUESTOS_RESULTANTES_COMBUSTION[i]] = moles
        moles = 0

    return [moles, n, especifico]

def normalizar_composicion(composicion: list):
    composicion_normalizada = []
    total = sum(composicion)
    for comp in composicion:
        composicion_normalizada.append({
            'compuesto': comp['fluido'],
            'x': round(comp['porc_vol']/total, 6)
        })
    
    return composicion_normalizada

def calcular_entalpia_combustion(composicion: list):
    entalpia = 0
    for comp in composicion:
        entalpia += comp['x'] * CALORES_COMBUSTION[comp['cas']]

    return entalpia

def calcular_h(presion: float, temperatura: float, composicion: list):
    entalpias = []
    for comp in composicion:
        entalpias = {
            'cas': comp['cas'],
            'h': CP.PropsSI('H', 'P', presion, 'T', temperatura, comp['compuesto']) 
        }

    return entalpias

def calcular_calores_gas(composicion, h):
    calor_especifico = 0.0
    pm_gas_promedio = 0.0

    for comp in composicion:
        calor_especifico += comp['x'] * h['h'] * comp['x'].Mw
        pm_gas_promedio += comp['x'] * comp['x'].Mw

    return calor_especifico, pm_gas_promedio

def calcular_calores_aire(composicion, h, temperatura_aire, presion_aire, humedad_relativa_aire):
    C1 = 73.649
    C2 = -7258.2
    C3 = -7.6037
    C4 = 4.1635e-6
    C5 = 2
    
    p_h2o = (math.e**(C1 + C2/(temperatura_aire+273.15) + C3*math.log(temperatura_aire+273.15)+C4*math.pow(temperatura_aire+273.15,C5)))
    x_h2o = humedad_relativa_aire/100*(p_h2o/presion_aire)

    aire_seco = [0.21, 0.79]
    aire_humedo = [0.21-x_h2o, 0.79*(1-x_h2o), x_h2o]

    calor_especifico = 0.0
    pm_aire_promedio = 0.0

    for i in range(3):
        calor_especifico += aire_humedo[i] * h[i]['h'] * h[i]['compuesto'].MW
        pm_aire_promedio += aire_humedo[i] * h[i]['compuesto'].MW

    return calor_especifico, pm_aire_promedio

def calcular_n_total_salida(n: list, composicion: list,
                            n_gas_entrada: float, calores_horno: list,
                            n_aire_entrada: float, aire_humedo: list):
    entalpias = []
    ns = []
    for i,compuesto in enumerate(n):
        x = (compuesto['moles']+composicion[compuesto['cas']['x']]*n_gas_entrada)
        ns.append(x)
        entalpias.append(x*compuesto['compuesto'].MW*calores_horno[i])

    x_n2 = n_aire_entrada*aire_humedo[1]+composicion[13][x]*n_gas_entrada
    entalpias.append(x_n2*composicion[12]['compuesto'].MW*calores_horno[5])

    x_o2_entrada = n_aire_entrada*aire_humedo[2]
    x_o2_reaccion = n_gas_entrada*n[5]
    x_o2 = x_o2_entrada-x_o2_reaccion
    entalpias.append(x_o2*composicion[11]['compuesto'].MW*calores_horno[4])
    o2_exceso = x_o2/x_o2_reaccion

    n_h2o_aire = n_aire_entrada*aire_humedo[2]
    n_h2o_gas = n_gas_entrada*composicion[11]['x']
    n_h2o_reaccion = n[6]*n_gas_entrada
    n_h2o = n_h2o_aire+n_h2o_gas+n_h2o_reaccion
    entalpias.append(n_h2o*composicion[24]['compuesto'].PM*calores_horno[6])
    
    n_total = sum([n_h2o, x_n2, x_o2, *ns])

    return sum(entalpias), n_total, [x/n_total for x in [n_h2o, x_n2, x_o2, *ns]], o2_exceso

def evaluar_caldera(flujo_gas: float, temperatura_gas: float, presion_gas: float,
                    flujo_aire: float, temperatura_aire: float, presion_aire: float,
                    humedad_relativa_aire: float, temperatura_horno: float,
                    presion_horno: float, flujo_agua: float, temperatura_agua: float,
                    presion_agua: float, flujo_vapor: float, temperatura_vapor: float,
                    presion_vapor: float, composiciones_combustible: list):
    
    composicion_normalizada = normalizar_composicion(composiciones_combustible)
    
    compuestos_combustion = composicion_normalizada[:10]
    moles_reaccion, n, calor_especifico_reaccion = obtener_moles_reaccion(compuestos_combustion)
    entalpia_combustion = calcular_entalpia_combustion(compuestos_combustion)

    h_gas = calcular_h(presion_gas, temperatura_gas, composicion_normalizada[:-2])
    h_aire = calcular_h(presion_aire, temperatura_aire, [composicion_normalizada])
    
    h_horno = calcular_h(presion_horno, temperatura_horno, composicion_normalizada)
    
    h_agua = CP.PropsSI('H', 'P', presion_agua, 'T', temperatura_agua, 'water')
    h_vapor = CP.PropsSI('H', 'P', presion_vapor, 'T', temperatura_vapor, 'water')

    calor_gas_especifico, calor_gas_promedio = calcular_calores_gas(composicion_normalizada, h_gas)    
    ngas_entrada = flujo_gas*(presion_gas/(R*temperatura_gas)) 
    mgas_entrada = ngas_entrada*calor_gas_promedio
    energia_gas_entrada = mgas_entrada*calor_gas_especifico

    calor_aire_especifico, calor_aire_promedio = calcular_calores_aire([composicion_normalizada], h_aire, temperatura_aire, presion_aire, humedad_relativa_aire)
    naire_entrada = flujo_aire*(presion_aire/(R*temperatura_aire))
    maire_entrada = naire_entrada*calor_aire_promedio

    energia_aire_entrada = maire_entrada*calor_aire_especifico

    energia_total = energia_gas_entrada + energia_aire_entrada
    energia_total_reaccion = calor_especifico_reaccion*ngas_entrada

    entalpias_totales, n_total, ns_totales, o2_exceso = calcular_n_total_salida()

    pm_salida_promedio = '' #TODO
    flujo_combustion = n_total/(presion_horno/(R*temperatura_horno))
    flujo_combustion_masico = '' # TODO

    energia_horno = energia_total_reaccion + entalpias_totales + energia_aire_entrada
    flujo_purga = flujo_agua - flujo_vapor

    energia_vapor = flujo_vapor*h_vapor - flujo_agua*h_agua + flujo_vapor*2.44346*1e6

    eficiencia = abs(energia_vapor/energia_horno) * 100

    return {
       'flujo_combustion': flujo_combustion,
       'oxigeno_exceso': o2_exceso,

       'fraccion_h2o_gas': ns_totales[0],
       'fraccion_n2_gas': ns_totales[1],
       'fraccion_o2_gas': ns_totales[2],
       'fraccion_co2_gas': ns_totales[3],

       'balance_gas': {
           
       },

       'balance_aire': {
           
       },

       'energia_gas_entrada': energia_gas_entrada,
       'energia_aire_entrada': energia_aire_entrada,

       'flujo_purga': flujo_purga,
       'energia_vapor': energia_vapor,

       'eficiencia': eficiencia
    }
