from thermo.chemical import Chemical
from thermo.mixture import Mixture
from .unidades import transformar_unidades_cp
import numpy

def calcular_cp(fluido: str, t1: float, t2: float, unidad_salida: int = 29, presion: float = 101325, fase: str = 'a') -> float:
    """
    Resumen:
        Función para el cálculo de la capacidad calorífica del fluido mediante
        el CAS del fluido, temperatura de entrada y temperatura de salida.

    Parámetros:
        fluido: str -> CAS del fluido
        t1: float -> Temperatura inicial (K)
        t2: float -> Temperatura final (K)
        unidad_salida: int -> ID de la unidad de salida
        presion: float -> Presión para el cálculo (Pa). El default es 101325Pa.
        fase: string -> 'a' es automático. 'g' es gas. 'l' líquido.
    
    Devuelve:
        float: Cp del fluido en esas condiciones
    """
    
    t = numpy.mean([t1, t2]) # Promedio de temperaturas
    
    if(fluido == '132259-10-0'): # Caso especial del Aire
        quimico = Mixture('air',T=t,P=presion)
    else: # Demás casos
        quimico = Chemical(fluido,T=t,P=presion)
 
    if(fase == 'l'): # Líquido
        cp = quimico.Cpl
    elif(fase == 'g'): # Gase
        cp = quimico.Cpg
    else: # Automático
        cp = quimico.Cp

    return round(transformar_unidades_cp([cp], 29, unidad_salida)[0], 4)

def calcular_entalpia_entre_puntos(fluido: str, t1: float, t2: float, presion: float) -> float:
    """
    Resumen:
        Calcula la entalpía entre dos temperaturas y una presión dada en caso de que haya cambio de fase.
    
    Parámetros:
        fluido: str -> CAS del fluido 
        t1: float -> Temperatura inicial (K)
        t2: float -> Temperatura final (K)
        presion: float -> Presión de entrada (Pa)

    Devuelve:
        float -> Entalpía calculada
    """
    quimico = Chemical(fluido,T=t1,P=presion)
    tsat = quimico.Tsat(P=presion)

    if(t1 <= tsat): # Caso Líquido > Gas
        print(1)
        return entalpia_l_a_g(quimico, t1, t2, presion, tsat)
    else: # Caso Gas > Líquido
        print(2)
        return entalpia_g_a_l(quimico, t1, t2, presion, tsat)

def entalpia_l_a_g(quimico: Chemical, t1: float, t2: float, presion: float, tsat: float) -> float:
    """
    Resumen:
        Calcula la entalpía de líquido a gas del fluido en la temperatura y presion dadas.
        Utiliza las integrales del Cp y el exceso dado por la librería thermo.
    """
    try:
        h_liquido = numpy.ceil(quimico.HeatCapacityLiquid.T_dependent_property_integral(t1,tsat)/quimico.MW  
                                - quimico.calc_H_excess(T=tsat, P=presion)/1000)
    except:
        h_liquido = numpy.ceil(quimico.HeatCapacityLiquid.T_dependent_property_integral(t1,tsat)/quimico.MW)

    quimico.calculate(tsat, P=presion)

    try:
        h_liquido_saturado = numpy.ceil(quimico.Hvap/1000 - quimico.calc_H_excess(T=tsat, P=presion)/1000)
    except:
        h_liquido_saturado = numpy.ceil(quimico.Hvap/1000)

    quimico.calculate(t2, P=presion)

    try:
        h_vapor = numpy.ceil(quimico.HeatCapacityGas.T_dependent_property_integral(tsat,t2)/quimico.MW
                                    - quimico.calc_H_excess(T=t2, P=presion)/1000)
    except:
        h_vapor = numpy.ceil(quimico.HeatCapacityGas.T_dependent_property_integral(tsat,t2)/quimico.MW)

    return numpy.ceil(h_liquido+h_vapor+h_liquido_saturado)*1000 # J/Kg

def entalpia_g_a_l(quimico: Chemical, t1: float, t2: float, presion: float, tsat: float) -> float:
    """
    Resumen:
        Calcula la entalpía de gas a líquido del fluido en la temperatura y presion dadas.
        Utiliza las integrales del Cp y el exceso dado por la librería thermo.
    """

    try:
        h_vapor = numpy.ceil(quimico.HeatCapacityGas.T_dependent_property_integral(t1,tsat)/quimico.MW
                                - quimico.calc_H_excess(T=tsat, P=presion)/1000) 
    except:
        h_vapor = numpy.ceil(quimico.HeatCapacityGas.T_dependent_property_integral(t1,tsat)/quimico.MW) 
    
    quimico.calculate(tsat, P=presion)

    try:
        h_liquido_saturado = numpy.ceil(quimico.Hvap/1000 - quimico.calc_H_excess(T=tsat, P=presion)/1000) 
    except:
        h_liquido_saturado = numpy.ceil(quimico.Hvap/1000) 
   
    quimico.calculate(t2, P=presion)
    
    try:
        h_liquido = numpy.ceil(quimico.HeatCapacityLiquid.T_dependent_property_integral(tsat,t2)/quimico.MW  
                                - quimico.calc_H_excess(T=tsat, P=presion)/1000)
    except:
        h_liquido = numpy.ceil(quimico.HeatCapacityLiquid.T_dependent_property_integral(tsat,t2)/quimico.MW)

    return abs(numpy.ceil(h_liquido+h_vapor-h_liquido_saturado)*1000) # J/Kg

def calcular_tsat_hvap(cas: str, presion: float):
    quimico = Chemical(cas)
    return (quimico.Tsat(presion),quimico.Hvap)

def calcular_fase(cas: str, t1: float, t2: float, presion) -> str:
    """
    Resumen:
        Esta función calculará la fase del fluido de los datos dados.
    """

    return Chemical(cas,T=numpy.mean([t1,t2]), P=presion).phase