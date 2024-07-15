from thermo.chemical import Chemical
from CoolProp import CoolProp as CP

import math

COMPUESTOS = {
    '74-82-8': Chemical('74-82-8'), '74-84-0': Chemical('74-84-0'), '74-98-6': Chemical('74-98-6'), 
    '124-38-9': Chemical('124-38-9'), '106-97-8': Chemical('106-97-8'), '75-28-5': Chemical('75-28-5'), 
    '7727-37-9': Chemical('7727-37-9'), '78-78-4': Chemical('78-78-4'), '109-66-0': Chemical('109-66-0'), 
    '110-54-3': Chemical('110-54-3'), '7782-44-7': Chemical('7782-44-7'), 
    '7783-06-4': Chemical('7783-06-4'), '7732-18-5': Chemical('7732-18-5'),  
    '1333-74-0': Chemical('1333-74-0'), '7446-09-5': Chemical('7446-09-5'),
}

COMPUESTOS_COOLPROP = {
    '74-82-8': 'Methane', '74-84-0': 'Ethane', '74-98-6': 'Propane', 
    '124-38-9': 'CarbonDioxide', '106-97-8': 'Butane', '75-28-5': 'IsoButane', 
    '7727-37-9': 'Nitrogen', '78-78-4': "Isopentane", '109-66-0': "n-Pentane", 
    '110-54-3': 'n-Hexane', '7782-44-7': "Oxygen", 
    '7783-06-4': "HydrogenSulfide", '7732-18-5': "Water",  
    '1333-74-0': "Hydrogen", '7446-09-5': "SulfurDioxide"
}

COMPUESTOS_COMBUSTION = [
    '74-82-8', '74-84-0', '74-98-6', '75-28-5',
    '106-97-8', '109-66-0', '110-54-3',
    '78-78-4 ', '1333-74-0', '110-54-3'
    '7446-09-5'
]

COMPUESTOS_AIRE = [
    '7782-44-7', '7727-37-9',
    '7732-18-5'
]

COMPUESTOS_HORNO = [
    '7782-44-7', '124-38-9',
    '7732-18-5', '7446-09-5',
    '7727-37-9'
]

COMPUESTOS_RESULTANTES_COMBUSTION = [
    '7782-44-7', '124-38-9', 
    '7732-18-5', '7446-09-5'
]

MATRIZ_ESTEQUIOMETRICA = [
    [2, 7/2, 5, 13/2, 13/2, 8, 8, 19/2, 1/2, 3/2 ],
	[1,   2, 3,    4,    4, 5, 5,    6,   0, 0   ],
	[2,   3, 4,    5,    5, 6, 6,    7,   1, 1   ],
	[0,   0, 0,    0,    0, 0, 0,    0,   0, 1   ]
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
    n = {}
    especifico = 0
    for i in range(4):
        moles = 0
        for j,compuesto in enumerate(composicion):
            cas = compuesto['compuesto'].CAS
            moles += compuesto['x_vol'] * MATRIZ_ESTEQUIOMETRICA[i][j] 
            especifico += compuesto['x_vol'] * CALORES_COMBUSTION[cas]

        n[COMPUESTOS_RESULTANTES_COMBUSTION[i]] = moles

    return [n, especifico]

def normalizar_composicion(composicion: list):
    composicion_normalizada = {}
    print(composicion)
    total_vol = sum([float(comp['porc_vol']) for comp in composicion])
    total_aire = sum([float(comp['porc_aire']) for comp in composicion if comp['porc_aire']])

    for comp in composicion:
        cas = comp['fluido']['cas'].strip()
        composicion_normalizada[cas] = {
            'compuesto': COMPUESTOS[cas],
            'x_vol': round(float(comp['porc_vol'])/total_vol, 6),
            'x_aire': round(float(comp['porc_aire'])/total_aire, 6) if comp['porc_aire'] else 0
        }
    
    return composicion_normalizada

def calcular_h(presion: float, temperatura: float, composicion: list):
    entalpias = {}
    for comp in composicion:
        cas = comp['compuesto'].CAS
        entalpias[cas] = CP.PropsSI('H', 'P', presion, 'T', temperatura, COMPUESTOS_COOLPROP[cas]) 

    return entalpias

def calcular_calores_gas(composicion, h):
    calor_especifico = 0.0
    pm_gas_promedio = 0.0

    for comp in composicion:
        compuesto = comp['compuesto']
        calor_especifico += comp['x_vol'] * h[compuesto.CAS] * compuesto.MW
        pm_gas_promedio += comp['x_vol'] * compuesto.MW

    return calor_especifico, pm_gas_promedio

def calcular_calores_aire(composiciones, h, temperatura_aire, presion_aire, humedad_relativa_aire):
    C1 = 73.649
    C2 = -7258.2
    C3 = -7.6037
    C4 = 4.1635e-6
    C5 = 2
    
    p_h2o = (math.e**(C1 + C2/(temperatura_aire+273.15) + C3*math.log(temperatura_aire+273.15)+C4*math.pow(temperatura_aire+273.15,C5)))
    x_h2o = humedad_relativa_aire/100*(p_h2o/presion_aire)

    aire_humedo = [
        0.21-x_h2o,
        0.79*(1-x_h2o),
        x_h2o
    ]

    calor_especifico = 0.0
    pm_aire_promedio = 0.0

    for i in range(3):
        cas = COMPUESTOS_AIRE[i]
        mw = composiciones[cas]['compuesto'].MW
        calor_especifico += aire_humedo[i] * h[cas] * mw
        pm_aire_promedio += aire_humedo[i] * mw

    return calor_especifico, pm_aire_promedio, aire_humedo

def calcular_n_total_salida(n: list, composicion: list,
                            n_gas_entrada: float, calores_horno: list,
                            n_aire_entrada: float, aire_humedo: list):
    entalpias = []

    x_co2 = (n['124-38-9']+composicion['124-38-9']['x_vol'])*n_gas_entrada
    entalpias.append(x_co2*composicion['124-38-9']['compuesto'].MW*calores_horno['124-38-9'])

    x_so2 = (n['7446-09-5']+composicion['7446-09-5']['x_vol'])*n_gas_entrada
    entalpias.append(x_so2*composicion['7446-09-5']['compuesto'].MW*calores_horno['7446-09-5'])

    x_n2 = n_aire_entrada*aire_humedo[1]+composicion['7727-37-9']['x_vol']*n_gas_entrada
    entalpias.append(x_n2*composicion['7727-37-9']['compuesto'].MW*calores_horno['7727-37-9'])

    x_o2_entrada = n_aire_entrada*aire_humedo[0]
    x_o2_reaccion = n_gas_entrada*n['7782-44-7']
    x_o2 = x_o2_entrada-x_o2_reaccion
    entalpias.append(x_o2*composicion['7782-44-7']['compuesto'].MW*calores_horno['7782-44-7'])
    o2_exceso = x_o2/x_o2_reaccion*100

    x_h2o_aire = n_aire_entrada*aire_humedo[2]
    x_h2o_gas = n_gas_entrada*composicion['7732-18-5']['x_vol']
    x_h2o_reaccion = n['7732-18-5']*n_gas_entrada
    x_h2o = x_h2o_aire+x_h2o_gas+x_h2o_reaccion
    entalpias.append(x_h2o*composicion['7732-18-5']['compuesto'].MW*calores_horno['7732-18-5'])
    
    n_total = sum([x_h2o, x_n2, x_o2, x_so2, x_co2])

    ns_totales = {
        '124-38-9': x_co2/n_total,
        '7446-09-5': x_so2/n_total,
        '7727-37-9': x_n2/n_total,
        '7732-18-5': x_h2o/n_total,
        '7782-44-7': x_o2/n_total
    }

    return sum(entalpias), n_total, ns_totales, o2_exceso

def evaluar_caldera(flujo_gas: float, temperatura_gas: float, presion_gas: float,
                    flujo_aire: float, temperatura_aire: float, presion_aire: float,
                    humedad_relativa_aire: float, temperatura_horno: float,
                    presion_horno: float, flujo_agua: float, temperatura_agua: float,
                    presion_agua: float, flujo_vapor: float, temperatura_vapor: float,
                    presion_vapor: float, composiciones_combustible: list):
    
    composicion_normalizada = normalizar_composicion(composiciones_combustible)
    
    compuestos_combustion = [compuesto for compuesto in composicion_normalizada.values() if compuesto['compuesto'].CAS in COMPUESTOS_COMBUSTION]
    compuestos_horno = [compuesto for compuesto in composicion_normalizada.values() if compuesto['compuesto'].CAS in COMPUESTOS_HORNO]
    compuestos_aire = [compuesto for compuesto in composicion_normalizada.values() if compuesto['compuesto'].CAS in COMPUESTOS_AIRE]

    n, calor_especifico_combustion = obtener_moles_reaccion(compuestos_combustion)

    h_gas = calcular_h(presion_gas, temperatura_gas, composicion_normalizada.values())
    h_aire = calcular_h(presion_aire, temperatura_aire, compuestos_aire)
    h_horno = calcular_h(presion_horno, temperatura_horno, compuestos_horno)
    
    h_agua = CP.PropsSI('H', 'P', presion_agua, 'T', temperatura_agua, 'water')
    h_vapor = CP.PropsSI('H', 'P', presion_vapor, 'T', temperatura_vapor, 'water')

    calor_gas_especifico, calor_gas_promedio = calcular_calores_gas(composicion_normalizada.values(), h_gas)    
    ngas_entrada = flujo_gas*(presion_gas/(R*temperatura_gas)) 
    mgas_entrada = ngas_entrada*calor_gas_promedio
    energia_gas_entrada = ngas_entrada*calor_gas_especifico

    calor_aire_especifico, calor_aire_promedio, aire_humedo = calcular_calores_aire(composicion_normalizada,
                                                                        h_aire, temperatura_aire, 
                                                                        presion_aire, humedad_relativa_aire)
    naire_entrada = flujo_aire*(presion_aire/(R*temperatura_aire))
    maire_entrada = naire_entrada*calor_aire_promedio

    energia_aire_entrada = maire_entrada*calor_aire_especifico

    energia_total = energia_gas_entrada + energia_aire_entrada
    energia_total_reaccion = calor_especifico_combustion*ngas_entrada

    entalpias_totales, n_total, ns_totales, o2_exceso = calcular_n_total_salida(
        n, composicion_normalizada, ngas_entrada, h_horno, naire_entrada, 
        aire_humedo
    )

    pm_salida_promedio = [compuesto['x_vol']*compuesto['compuesto'].MW for compuesto in compuestos_horno]
    flujo_combustion = n_total/(presion_horno/(R*temperatura_horno))
    flujo_combustion_masico = sum([ns_totales[compuesto['compuesto'].CAS]*compuesto['compuesto'].MW for compuesto in compuestos_horno])

    energia_horno = energia_total_reaccion + entalpias_totales + energia_aire_entrada
    flujo_purga = flujo_agua - flujo_vapor

    energia_vapor = flujo_vapor*h_vapor - flujo_agua*h_agua + flujo_vapor

    eficiencia = abs(energia_vapor/energia_horno) * 100

    return {
       'flujo_combustion': flujo_combustion,
       'oxigeno_exceso': o2_exceso,

       'fraccion_h2o_gas': ns_totales['7732-18-5'],
       'fraccion_n2_gas': ns_totales['7727-37-9'],
       'fraccion_o2_gas': ns_totales['7782-44-7'],
       'fraccion_so2_gas': ns_totales['7446-09-5'],
       'fraccion_co2_gas': ns_totales['124-38-9'],

       'balance_gas': {
           'masico': mgas_entrada,
           'molar': ngas_entrada
       },

       'balance_aire': {
           'masico': maire_entrada,
           'molar': naire_entrada           
       },

       'pm_salida_promedio': pm_salida_promedio,
       'flujo_combustion_masico': flujo_combustion_masico,

       'energia_gas_entrada': energia_gas_entrada,
       'energia_aire_entrada': energia_aire_entrada,
       'energia_total': energia_total,
       'energia_total_entrada': energia_total,
       'energia_total_reaccion': energia_total_reaccion,
       'energia_horno': energia_horno,
       'energia_total_salida': abs(energia_vapor),

       'flujo_purga': flujo_purga,
       'energia_vapor': energia_vapor,

       'eficiencia': eficiencia
    }
