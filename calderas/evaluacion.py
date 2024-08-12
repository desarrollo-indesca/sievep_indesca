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
    '74-82-8', '74-84-0', '74-98-6', '106-97-8',
    '75-28-5', '109-66-0', '110-54-3',
    '78-78-4', '1333-74-0', '110-54-3',
    '7783-06-4'
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
    [2, 7/2, 5, 13/2, 13/2, 8, 8, 19/2,  3/2, 1/2,],
	[1,   2, 3,    4,    4, 5, 5,    6,    0, 0,  ],
	[2,   3, 4,    5,    5, 6, 6,    7,    1, 1,  ],
	[0,   0, 0,    0,    0, 0, 0,    0,    1, 0,  ]
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

PESOS_MOLECULARES = {
    '74-82-8': 16.043,
    '74-84-0': 30.07,
    '74-98-6': 44.097,
    '75-28-5': 58.123,
    '106-97-8': 58.123,
    '78-78-4': 72.15,
    '109-66-0': 72.15,
    '110-54-3': 86.177,
    '1333-74-0': 2.016,
    '7783-06-4': 34.082,
    '7732-18-5': 18.015,
    '7782-44-7': 31.999,
    '124-38-9': 44.01,
    '7446-09-5': 64.065, 
    '7727-37-9': 28.014,
    '7704-34-9': 32.065,
    '7440-44-0': 12.000
}

MOLES_CARBONO_INDIRECTO = {
    '74-82-8': {
        "moles": 1,
        "carbono": True
    },
    '74-84-0': {
        "moles": 2,
        "carbono": True
    },
    '74-98-6': {
        "moles": 3,
        "carbono": False
    },
    '75-28-5': {
        "moles": 4,
        "carbono": True
    },
    '106-97-8': {
        "moles": 4,
        "carbono": True
    },
    '78-78-4': {
        "moles": 5,
        "carbono": True
    },
    '109-66-0': {
        "moles": 5,
        "carbono": True
    },
    '110-54-3': {
        "moles": 6,
        "carbono": True
    },
    '124-38-9': {
        "moles": 1,
        "carbono": True
    }
}

MOLES_HIDROGENO_INDIRECTO = {
    '74-82-8': 4,
    '74-84-0': 6,
    '74-98-6': 8,
    '75-28-5': 10,
    '106-97-8': 10,
    '78-78-4': 12,
    '109-66-0': 12,
    '110-54-3': 14,
    '7783-06-4': 2,
    '124-38-9': 2,
    '7732-18-5': 2
}

PORCENTAJES_CARBONO = {
    '74-82-8': 0.75, 
    '74-84-0': 0.8, 
    '74-98-6': 0.9429756719960654, 
    '75-28-5': 0.8275862068965517, 
    '106-97-8': 0.8275862068965517, 
    '78-78-4': 0.8333333333333334, 
    '109-66-0': 0.8333333333333334, 
    '110-54-3': 0.8372093023255814, 
    '124-38-9': 0.8571428571428571
}

PORCENTAJES_HIDROGENO = {
    '74-82-8': 0.25, 
    '74-84-0': 0.2, 
    '74-98-6': 0.18181818181818182, 
    '75-28-5': 0.1724137931034483, 
    '106-97-8': 0.1724137931034483, 
    '78-78-4': 0.16666666666666666, 
    '109-66-0': 0.16666666666666666, 
    '110-54-3': 0.16279069767441862, 
    '7783-06-4': 0.05871128724497285, 
    '124-38-9': 0.14285714285714285, 
    '7732-18-5': 0.11111419761660048
}

ENTALPIA_FORMACION = {
    '74-82-8': -17.895,
    '74-84-0': -20.236,
    '74-98-6': -24.820,
    '75-28-5': -31.452,
    '106-97-8': -29.812,
    '78-78-4': -35,
    '109-66-0': -35,
    '110-54-3': -40,
    '7783-06-4': -4.8159,
    '7732-18-5': -57.7915,
    '7782-44-7': 0,
    '124-38-9': -93.9293,
    '7446-09-5': -70.7695
}

R = 8.3145e-5

def obtener_moles_reaccion(composicion: list):
    """
    Resumen:
        Calcula los moles de los compuestos resultantes de la reaccion quimica en la caldera.

    Parametros:
        composicion : list
            Lista de diccionarios, donde cada diccionario tiene la estructura {'compuesto':objeto_compuesto, 'x_vol': valor_moles}

    Devuelve:
        list
            Lista con dos elementos. El primero es un diccionario donde las llaves son los CAS de los compuestos resultantes de la reaccion y los valores son los moles de cada compuesto. El segundo elemento es el calor especifico del gas resultante de la reaccion.
    """
    n = {}
    especifico = 0
    calor_calculado = False

    for i in range(4):
        moles = 0
        for j,compuesto in enumerate(composicion):
            cas = compuesto['compuesto'].CAS
            moles += compuesto['x_vol'] * MATRIZ_ESTEQUIOMETRICA[i][j] 

            if(not calor_calculado):
                especifico += compuesto['x_vol'] * CALORES_COMBUSTION[cas]

        n[COMPUESTOS_RESULTANTES_COMBUSTION[i]] = moles
        calor_calculado = True

    return [n, especifico]

def normalizar_composicion(composicion: list):
    """
    Resumen:
        Normaliza la composicion de los compuestos del combustible la caldera.

    Parametros:
        composicion : list
            Lista de diccionarios, donde cada diccionario tiene la estructura {'fluido':objeto_fluido, 'porc_vol': porcentaje_volumen, 'porc_aire': porcentaje_aire}

    Devuelve:
        list
            Lista de diccionarios normalizados, donde cada diccionario tiene la estructura {'compuesto':objeto_compuesto, 'x_vol': valor_moles_normalizado, 'x_aire': valor_moles_aire_normalizado}
    """
    composicion_normalizada = {}
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
    """
    Resumen:
        Calcula las entalpias de los compuestos del gas de combustion.

    Parametros:
        presion : float
            Presion del gas de combustion [Pa]
        temperatura : float
            Temperatura del gas de combustion [K]
        composicion : list
            Lista de diccionarios, donde cada diccionario tiene la estructura {'compuesto':objeto_compuesto, 'x_vol': valor_moles}

    Devuelve:
        dict
            Diccionario donde las llaves son los CAS de los compuestos y los valores son las entalpias de cada compuesto [J/mol]
    """
    entalpias = {}
    for comp in composicion:
        cas = comp['compuesto'].CAS
        entalpias[cas] = CP.PropsSI('H', 'P', presion, 'T', temperatura, COMPUESTOS_COOLPROP[cas]) 

    return entalpias

def calcular_calores_gas(composicion, h):
    """
    Resumen:
        Calcula el calor especifico y el promedio de masa molecular del gas de combustion.

    Parametros:
        composicion : list
            Lista de diccionarios, donde cada diccionario tiene la estructura {'compuesto':objeto_compuesto, 'x_vol': valor_moles}
        h : dict
            Diccionario donde las llaves son los CAS de los compuestos y los valores son las entalpias de cada compuesto [J/mol]

    Devuelve:
        tuple
            Tupla con dos elementos. El primer elemento es el calor especifico del gas de combustion [J/kgK]. El segundo elemento es el promedio de masa molecular del gas de combustion [kg/mol]
    """
    calor_especifico = 0.0
    pm_gas_promedio = 0.0

    for comp in composicion:
        compuesto = comp['compuesto']
        calor_especifico += comp['x_vol'] * h[compuesto.CAS] * PESOS_MOLECULARES[compuesto.CAS]
        pm_gas_promedio += comp['x_vol'] * PESOS_MOLECULARES[compuesto.CAS]

    return (calor_especifico, pm_gas_promedio)

def calcular_calores_aire(h, temperatura_aire, presion_aire, humedad_relativa_aire):
    """
    Calcula el calor especifico y el promedio de masa molecular del aire de combustion.

    Parametros:
        h : dict
            Diccionario donde las llaves son los CAS de los compuestos y los valores son las entalpias de cada compuesto [J/mol]
        temperatura_aire : float
            Temperatura del aire de combustion [K]
        presion_aire : float
            Presion del aire de combustion [Pa]
        humedad_relativa_aire : float
            Humedad relativa del aire de combustion [%]

    Devuelve:
        tuple
            Tupla con tres elementos. El primer elemento es el calor especifico del aire de combustion [J/kgK]. El segundo elemento es el promedio de masa molecular del aire de combustion [kg/mol]. El tercero es la composición del aire húmedo.
    """
    C1 = 73.649
    C2 = -7258.2
    C3 = -7.6037
    C4 = 4.1635e-6
    C5 = 2
    
    p_h2o = (math.e**(C1 + C2/(temperatura_aire) + C3*math.log(temperatura_aire)+C4*math.pow(temperatura_aire,C5)))/100000
    x_h2o = humedad_relativa_aire/100*(p_h2o/(presion_aire))

    aire_humedo = [
        0.21*(1-x_h2o),
        0.79*(1-x_h2o),
        x_h2o
    ]

    calor_especifico = 0.0
    pm_aire_promedio = 0.0

    for i in range(3):
        cas = COMPUESTOS_AIRE[i]
        mw = PESOS_MOLECULARES[cas]
        calor_especifico += aire_humedo[i] * h[cas] * mw
        pm_aire_promedio += aire_humedo[i] * mw

    return calor_especifico, pm_aire_promedio, aire_humedo

def calcular_n_total_salida(n: list, composicion: list,
                            n_gas_entrada: float, calores_horno: list,
                            n_aire_entrada: float, aire_humedo: list):
    """
    Calcula el valor total de las fracciones molares de los gases salientes de la caldera.

    Parametros:
        n : dict
            Diccionario con las fracciones molares de los compuestos de los gases de combustión. Las llaves son los CAS de los compuestos y los valores son las fracciones molares de cada compuesto.
        composicion : dict
            Diccionario con la composición de los compuestos de los gases de combustión. Las llaves son los CAS de los compuestos y los valores son los diccionarios de composición.
        n_gas_entrada : float
            Cantidad de gases de combustión entrantes [m3/s].
        calores_horno : dict
            Diccionario con los calores especificos de cada compuesto de los gases de combustión. Las llaves son los CAS de los compuestos y los valores son los calores especificos.
        n_aire_entrada : float
            Cantidad de aire de combustion entrantes [m3/s].
        aire_humedo : list
            Lista con las fracciones molares del aire húmedo. El primer elemento representa la fraccion molar de nitrogeno, el segundo elemento representa la fraccion molar de oxigeno y el tercer elemento representa la fraccion molar de agua.

    Devuelve:
        tuple
            Tupla con tres elementos. El primer elemento es la suma de las entalpias de los gases salientes [kJ/s]. El segundo elemento es la suma de las fracciones molares molares de los gases salientes. El tercero es el porcentaje de exceso de oxigeno.
    """
    entalpias = []

    x_co2 = (n['124-38-9']+composicion['124-38-9']['x_vol'])*n_gas_entrada
    entalpias.append(x_co2*PESOS_MOLECULARES['124-38-9']*calores_horno['124-38-9']/1000)

    x_so2 = (n['7446-09-5']+composicion['7446-09-5']['x_vol'])*n_gas_entrada
    entalpias.append(x_so2*PESOS_MOLECULARES['7446-09-5']*calores_horno['7446-09-5']/1000)

    x_n2 = n_aire_entrada*aire_humedo[1]+composicion['7727-37-9']['x_vol']*n_gas_entrada
    entalpias.append(x_n2*PESOS_MOLECULARES['7727-37-9']*calores_horno['7727-37-9']/1000)

    x_o2_entrada = n_aire_entrada*aire_humedo[0]
    x_o2_reaccion = n_gas_entrada*n['7782-44-7']
    x_o2 = x_o2_entrada-x_o2_reaccion
    entalpias.append(x_o2*PESOS_MOLECULARES['7782-44-7']*calores_horno['7782-44-7']/1000)
    o2_exceso = x_o2/x_o2_reaccion*100

    x_h2o_aire = n_aire_entrada*aire_humedo[2]
    x_h2o_gas = n_gas_entrada*composicion['7732-18-5']['x_vol']
    x_h2o_reaccion = n['7732-18-5']*n_gas_entrada
    x_h2o = x_h2o_aire+x_h2o_gas+x_h2o_reaccion
    entalpias.append(x_h2o*PESOS_MOLECULARES['7732-18-5']*calores_horno['7732-18-5']/1000)
    
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
    """
    Evalúa la caldera utilizando los parámetros de entrada.

    Args:
        flujo_gas (float): Flujo de gas en m³/h.
        temperatura_gas (float): Temperatura de gas en K.
        presion_gas (float): Presión de gas en bar.
        flujo_aire (float): Flujo de aire en m³/h.
        temperatura_aire (float): Temperatura de aire en K.
        presion_aire (float): Presión de aire en bar.
        humedad_relativa_aire (float): Humedad relativa del aire en %.
        temperatura_horno (float): Temperatura del horno en K.
        presion_horno (float): Presión del horno en bar.
        flujo_agua (float): Flujo de agua en m³/h.
        temperatura_agua (float): Temperatura del agua en K.
        presion_agua (float): Presión del agua en bar.
        flujo_vapor (float): Flujo de vapor en m³/h.
        temperatura_vapor (float): Temperatura del vapor en K.
        presion_vapor (float): Presión del vapor en bar.
        composiciones_combustible (list): Lista de composiciones de combustible.

    Returns:
        dict: Devuelve un diccionario con los valores de la evaluación de la caldera.
    """

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

    calor_gas_especifico, pm_promedio = calcular_calores_gas(composicion_normalizada.values(), h_gas)    
    
    ngas_entrada = flujo_gas*3600*((presion_gas)/100000/(R*temperatura_gas))/1000 # Kg/h
    mgas_entrada = ngas_entrada*pm_promedio #kmol/h
    energia_gas_entrada = ngas_entrada*calor_gas_especifico/1000

    calor_aire_especifico, pm_aire_promedio, aire_humedo = calcular_calores_aire(h_aire, temperatura_aire, 
                                                                        presion_aire, humedad_relativa_aire)
   
    naire_entrada = flujo_aire*3600*((presion_aire/100000)/(R*temperatura_aire))/1000 # kg/h
    maire_entrada = naire_entrada*pm_aire_promedio
    energia_aire_entrada = naire_entrada*calor_aire_especifico/1000

    energia_total_entrada = energia_gas_entrada + energia_aire_entrada
    energia_total_reaccion = calor_especifico_combustion*ngas_entrada*1e3

    entalpias_totales, n_total, ns_totales, o2_exceso = calcular_n_total_salida(
        n, composicion_normalizada, ngas_entrada, h_horno, naire_entrada, 
        aire_humedo
    )

    flujo_combustion = n_total/(((presion_horno/100000)/(R*temperatura_horno))/1000)
    flujo_combustion_masico = sum([ns_totales[compuesto['compuesto'].CAS]*PESOS_MOLECULARES[compuesto['compuesto'].CAS] for compuesto in compuestos_horno])

    energia_horno = energia_total_reaccion + entalpias_totales + energia_total_entrada
    
    flujo_purga = (flujo_agua - flujo_vapor)*3600/1000 # T/h

    energia_vapor = (flujo_vapor*h_vapor - flujo_agua*h_agua + flujo_vapor*2.44346*1e6)*3600/1000 # kJ/h

    eficiencia = abs(energia_vapor/energia_horno) * 100

    return {
       'flujo_combustion': flujo_combustion,
       'oxigeno_exceso': o2_exceso,

       'fraccion_h2o_gas': round(ns_totales['7732-18-5'], 4),
       'fraccion_n2_gas': round(ns_totales['7727-37-9'], 4),
       'fraccion_o2_gas': round(ns_totales['7782-44-7'], 4),
       'fraccion_so2_gas': round(ns_totales['7446-09-5'], 4),
       'fraccion_co2_gas': round(ns_totales['124-38-9'], 4),

       'balance_gas': {
           'masico': mgas_entrada,
           'molar': ngas_entrada
       },

       'balance_aire': {
           'masico': maire_entrada,
           'molar': naire_entrada           
       },

       'flujo_combustion_masico': flujo_combustion_masico,

       'energia_gas_entrada': energia_gas_entrada,
       'energia_aire_entrada': energia_aire_entrada,
       'energia_total_entrada': energia_total_entrada,
       'energia_total_reaccion': energia_total_reaccion,
       'energia_horno': energia_horno,
       'energia_total_salida': entalpias_totales,

       'flujo_purga': flujo_purga,
       'energia_vapor': energia_vapor,

       'eficiencia': eficiencia
    }

# FUNCIONES DE MÉTODO INDIRECTO

def calcular_pm_promedio(composiciones_combustible):
    return sum([PESOS_MOLECULARES[cas]*compuesto['x_vol'] for cas,compuesto in composiciones_combustible.items()])

def calcular_moles_carbon(composiciones_combustible,  flujo_molar_gas):
    for cas,comp in composiciones_combustible.items():
        moles = comp['x_vol'] * flujo_molar_gas
        composiciones_combustible[cas]['moles'] = moles

        if(PORCENTAJES_CARBONO.get(cas)):
            composiciones_combustible[cas]['moles_carbon'] = moles * PORCENTAJES_CARBONO[cas]

    moles_totales_carbon = sum([comp.get('moles_carbon', 0) for comp in composiciones_combustible.values()])
    porcentaje_carbon = moles_totales_carbon/flujo_molar_gas * 100

    return composiciones_combustible, porcentaje_carbon

def calcular_moles_azufre(composiciones_combustible, flujo_molar_gas, porc_s_h2s):
    composiciones_combustible['7783-06-4']['moles_azufre'] = composiciones_combustible['7783-06-4']['moles'] * porc_s_h2s
    porcentaje_azufre = composiciones_combustible['7783-06-4']['moles_azufre']/flujo_molar_gas * 100

    return composiciones_combustible, porcentaje_azufre

def calcular_moles_oxigeno(composiciones_combustible, flujo_molar_gas, porc_o2_co2, porc_o2_h2o):
    composiciones_combustible['7732-18-5']['moles_oxigeno'] =  porc_o2_h2o * composiciones_combustible['7732-18-5']['moles']
    composiciones_combustible['124-38-9']['moles_oxigeno'] =  porc_o2_co2 * composiciones_combustible['124-38-9']['moles']
    
    moles_totales_oxigeno = sum([comp.get('moles_oxigeno', 0) for comp in composiciones_combustible.values()])
    porcentaje_oxigeno = moles_totales_oxigeno/flujo_molar_gas * 100

    return composiciones_combustible, porcentaje_oxigeno

def calcular_moles_hidrogeno(composiciones_combustible, flujo_molar_gas):
    for cas,comp in composiciones_combustible.items():
        if(PORCENTAJES_HIDROGENO.get(cas)):
            composiciones_combustible[cas]['moles_azufre'] = comp['x_vol'] * PORCENTAJES_HIDROGENO[cas]
    
    moles_totales_hidrogeno = sum([comp.get('moles_azufre', 0) for comp in composiciones_combustible.values()])
    porcentaje_hidrogeno = moles_totales_hidrogeno/flujo_molar_gas * 100

    return composiciones_combustible, porcentaje_hidrogeno

def calcular_flujos_composiciones_masicas(composiciones_combustible, flujo_masico_gas):
    for cas,comp in composiciones_combustible.items():
        composiciones_combustible[cas]['flujo_masico'] = comp['moles'] * PESOS_MOLECULARES[cas]
        composiciones_combustible[cas]['y'] = composiciones_combustible[cas]['flujo_masico'] / flujo_masico_gas

    return composiciones_combustible

def evaluar_metodo_indirecto(composiciones_combustible, temperatura_aire, flujo_aire, velocidad_aire,
                                presion_aire, temperatura_gas, presion_gas, flujo_gas,  
                                area_superficie, temperatura_superficie, temperatura_horno):
    
    composicion_normalizada = normalizar_composicion(composiciones_combustible)
    flujo_molar_gas = (presion_gas*flujo_gas)/temperatura_gas
    pm_promedio = calcular_pm_promedio(composicion_normalizada)
    flujo_masico_gas = pm_promedio*flujo_molar_gas

    peso_molecular_oxigeno = PESOS_MOLECULARES['7782-44-7']
    peso_molecular_carbono = PESOS_MOLECULARES['7440-44-0']
    peso_molecular_azufre = PESOS_MOLECULARES['7704-34-9']

    porc_o2_co2 = (2 * peso_molecular_oxigeno) / (2 * peso_molecular_oxigeno + peso_molecular_carbono)
    porc_o2_h2o = (1 * peso_molecular_oxigeno) / (2 * 1 + 1 * peso_molecular_oxigeno)
    porc_s_h2s =  (1 * peso_molecular_azufre) / (2 + 1 * peso_molecular_carbono + 1 * peso_molecular_azufre)

    composiciones_combustible, porcentaje_carbon = calcular_moles_carbon(
        composicion_normalizada, flujo_molar_gas
    )

    composiciones_combustible, porcentaje_hidrogeno = calcular_moles_hidrogeno(
        composicion_normalizada, flujo_molar_gas
    )

    composiciones_combustible, porcentaje_oxigeno = calcular_moles_oxigeno(
        composicion_normalizada, flujo_molar_gas, porc_o2_co2, porc_o2_h2o
    )

    composiciones_combustible, porcentaje_azufre = calcular_moles_azufre(
        composicion_normalizada, flujo_molar_gas, porc_s_h2s
    )

    composicion_normalizada = calcular_flujos_composiciones_masicas(
        composicion_normalizada, flujo_masico_gas
    )

    flujo_molar_aire = (flujo_aire*presion_aire)/(8.314*(temperatura_aire))*0.001
    pm_aire_promedio = (composicion_normalizada['7782-44-7']['x_aire']*peso_molecular_oxigeno+composicion_normalizada['7727-37-9']['x_aire']*PESOS_MOLECULARES['7727-37-9']+composicion_normalizada['7732-18-5']['x_aire']*PESOS_MOLECULARES['7732-18-5'])
    flujo_masico_aire = (flujo_molar_aire*pm_aire_promedio)
    masa_agua_aire = composicion_normalizada['7732-18-5']['x_aire'] * flujo_masico_aire
    masa_aire_seco = flujo_masico_aire - masa_agua_aire
    factor_humedad = masa_agua_aire / masa_aire_seco

    poder_calorifico = sum([
        comp['y']*CALORES_COMBUSTION[cas] for cas,comp in composicion_normalizada.items()
    ])

    aire_teorico_req = ((11.6 * porcentaje_carbon + (34.8 * (porcentaje_hidrogeno - (porcentaje_oxigeno / 8)) + 4.35 * porcentaje_azufre))) / 100
    porc_aire_exceso = (composicion_normalizada['7732-18-5']['x_vol'] / (21 - composicion_normalizada['7732-18-5']['x_vol'])) * 100
    masa_aire_suministrado = (1 + porc_aire_exceso / 100) * aire_teorico_req
    masa_gas_seco_combustion = (composicion_normalizada['124-38-9']['x_vol'] * 44) / (12) + composicion_normalizada['7727-37-9']['x_vol'] + (masa_aire_suministrado * 77) / (100) + (masa_aire_suministrado - aire_teorico_req) * 23 / 100

    l1 = ((masa_gas_seco_combustion * 0.23 * (temperatura_horno - temperatura_aire)) / poder_calorifico) * 100
    l2 = ((9 * composicion_normalizada['1333-74-0']['x_vol'] * (584 + 0.45 * (temperatura_horno - temperatura_aire))) / poder_calorifico) * 100
    l3 = ((composicion_normalizada['7732-18-5']['x_vol'] * (584 + 0.45 * (temperatura_horno - temperatura_aire))) / poder_calorifico) * 100
    l4 = ((masa_aire_suministrado * factor_humedad * 0.45 * (temperatura_horno - temperatura_aire)) / poder_calorifico) * 100

    if (temperatura_superficie != 0 and velocidad_aire != 0 and area_superficie != 0):
        perdidas_radiacion_y_conveccion_area = (0.548 * ((pow((temperatura_superficie + 273, 15) / 55.55, 4)) - pow((temperatura_aire + 273, 15) / 55.55, 4)) + 1.957 * (temp_superficie - temperatura_aire) * ((196.85 * velocidad_aire + 68.9) / 68.9)**0.5) * 0.86
        perdida_hora = perdidas_radiacion_y_conveccion_area * area_superficie
        l6 = ((perdida_hora * 100) / (flujo_molar_gas * poder_calorifico)) * 100
    else:
        l6 = 3

    eficiencia = 100 - l1 - l2 - l3 - l4 - l6

    return {
        'perdidas': {
            'l1': l1,
            'l2': l2,
            'l3': l3,
            'l4': l4,
            'l6': l6
        },
        'eficiencia': eficiencia
    }