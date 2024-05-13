'''
Funciones contenedoras de la lógica de evaluación de turbinas.
'''

from calculos.termodinamicos import calcular_entalpia_coolprop, calcular_fase_coolprop, definicion_fases_coolprop
from auxiliares.evaluacion import calcular_eficiencia

def determinar_flujos_corrientes(corrientes, corrientes_diseno, flujo_entrada) -> list:
    flujo_entrada_diseno = next(filter(lambda x : x['entrada'], corrientes_diseno))['flujo']

    for i,_ in enumerate(corrientes):
        corrientes[i]['flujo'] = corrientes_diseno[i]['flujo']/flujo_entrada_diseno*flujo_entrada

    return corrientes

def determinar_propiedades_corrientes(corrientes):
    for i,_ in enumerate(corrientes):
        presion,temperatura = corrientes[i]['presion'],corrientes[i]['temperatura'] 
        corrientes[i]['entalpia'] = calcular_entalpia_coolprop(temperatura, presion, 'water')
        corrientes[i]['fase'] = definicion_fases_coolprop(calcular_fase_coolprop(temperatura, presion, 'water'))

        if(not corrientes[i]['entalpia'] or not corrientes[i]['fase']):
            raise Exception("No se pudo calcular la entalpía y/o fase de una corriente.")

    return corrientes

def calcular_balance_energia_entrada(corrientes_actualizadas):
    corriente_entrada = next(filter(lambda x : x['entrada'], corrientes_actualizadas))
    return corriente_entrada['entalpia']*corriente_entrada['flujo']

def calcular_balance_energia_salida(corrientes_actualizadas):
    return sum([x['entalpia']*x['flujo'] for x in corrientes_actualizadas if not x['entrada']])

def evaluar_turbina(flujo_entrada: float, potencia: float, corrientes: list, corrientes_diseno: list):
    # Determninar los flujos circulantes
    corrientes_actualizadas = determinar_flujos_corrientes(corrientes, corrientes_diseno, flujo_entrada)
    
    # Determinar la entalpía y fase de cada corriente e integrarlas
    corrientes_actualizadas = determinar_propiedades_corrientes(corrientes_actualizadas)

    # Balances de energía
    h_entrada = calcular_balance_energia_entrada(corrientes_actualizadas)
    h_salida = calcular_balance_energia_salida(corrientes_actualizadas)

    # Cálculo de potencia
    potencia_calculada = h_entrada - h_salida
    eficiencia = calcular_eficiencia(potencia_calculada, potencia)

    return {
        "eficiencia": eficiencia,
        "potencia_calculada": potencia_calculada,
        "corrientes": corrientes_actualizadas
    }