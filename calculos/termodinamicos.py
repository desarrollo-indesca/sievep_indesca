from thermo.chemical import Chemical
from thermo.mixture import Mixture

import CoolProp.CoolProp as CP
from .unidades import transformar_unidades_cp
import numpy

DENSIDAD_DEL_AGUA_LIQUIDA_A_5C = 1000.1953

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
 
    if(fluido == '132259-10-0'): # Caso especial del Aire
        try: # Cálculo de Cp con CoolProp (Preferido)
            cp = CP.PropsSI('C','T',t,'P',presion,'air')
        except: # Cálculo de Cp con Thermo (En caso de falla)
            quimico = Mixture('air',T=t,P=presion)
            cp = quimico.Cp

    quimico = Chemical(fluido,T=t,P=presion)
    try: # Cálculo de Cp con CoolProp (Preferido)
        cp = None

        # Conseguir nombre válido en CoolProp
        for i in range(5):
            try:
                name = quimico.synonyms[i].title().replace(' ','').replace('O-','o-').replace('N-','n-').replace('P-','p-')
                print(presion)
                if(fase == 'g'):
                    cp = CP.PropsSI('C','T',t,'P|gas',presion,name)
                elif(fase == 'l'):
                    cp = CP.PropsSI('C','T',t,'P|liquid',presion,name)
                else:
                    cp = CP.PropsSI('C','T',t,'P',presion,name)
                break
            except:
                continue

        if(cp == None):
            raise Exception
        else:
            print("COOLPROP")  
    except: # Cálculo de Cp con Thermo (En caso de falla)
        print('thermo')
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
        float -> Entalpía calculada (J/Kg)
    """
    quimico = Chemical(fluido,T=t1,P=presion)
    tsat = quimico.Tsat(P=presion)

    if(t1 <= tsat): # Caso Líquido > Gas
        return entalpia_l_a_g(quimico, t1, t2, presion, tsat)
    else: # Caso Gas > Líquido
        return entalpia_g_a_l(quimico, t1, t2, presion, tsat)

def entalpia_l_a_g(quimico: Chemical, t1: float, t2: float, presion: float, tsat: float) -> float:
    """
    Resumen:
        Función interna.
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
        Función interna.
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

def calcular_tsat_hvap(cas: str, presion: float, tsat: float = None) -> tuple:
    '''
    Resumen:
        Calcula la temperatura de saturación y el calor latente de vaporización de un fluido a una presión dada mediante su CAS.

    Parámetros:
        cas: str -> CAS del fluido
        presion: float -> Presión de entrada (Pa)

    Devuelve:
        tuple -> (Temperatura de saturación (K), Calor latente de vaporización (J/Kg))
    '''
    quimico = Chemical(cas,P=presion)

    if(not tsat):
        tsat = quimico.Tsat(presion)
    
    quimico.calculate(tsat)

    return (tsat,quimico.Hvap if quimico.Hvap else quimico.Hvap_Tb)

def calcular_fase(cas: str, t1: float, t2: float, presion) -> str:
    """
    Resumen:
        Esta función calculará la fase del fluido de los datos dados.

    Parámetros:
        cas: str -> CAS del fluido
        t1: float -> Temperatura inicial (K)
        t2: float -> Temperatura final (K)
        presion: float -> Presión de entrada (Pa)

    Devuelve:
        str -> Fase del fluido
    """

    return Chemical(cas,T=numpy.mean([t1,t2]), P=presion).phase

def obtener_viscosidad_liquido_saturado(quimico, t):
    psat = quimico.Psat
    quimico.calculate(t, psat + 10)
    return quimico.mul

def calcular_viscosidad(cas: str, t: float, p: float = 101325) -> (float, bool):
    """
    Resumen:
        Esta función calculará la viscosidad dinámica de un fluido según su temperatura y presión. En fase Líquido.

    Parámetros:
        cas: str -> CAS del fluido
        t: float -> Temperatura (K)
        p: float -> Presión (Pa)

    Devuelve:
        (float, bool) -> viscosidad dinámica del fluido en las condiciones presentadas en fase líquido. / boolean indicando si se asumió saturado
    """
    quimico = Chemical(cas, t, p)
    mu = quimico.mul
    flag = False

    if(not mu):
        mu = obtener_viscosidad_liquido_saturado(quimico, t)
        flag = True

    return (mu, flag)

def calcular_presion_vapor(cas: str, t: float, p: float = 101325) -> float:
    """
    Resumen:
        Esta función calculará la presión de vapor de un fluido según su temperatura y presión.

    Parámetros:
        cas: str -> CAS del fluido
        t: float -> Temperatura (K)
        p: float -> Presión (Pa)

    Devuelve:
        float -> Presión de vapor del fluido en las condiciones presentadas.
    """
    quimico = Chemical(cas, t, p)
    return quimico.Psat

def calcular_densidad(cas: str, t: float, p: float = 101325) -> float:
    """
    Resumen:
        Esta función calculará la densidad de un fluido según su temperatura y presión. En fase líquido.

    Parámetros:
        cas: str -> CAS del fluido
        t: float -> Temperatura inicial (K)
        p: float -> Presión (Pa)

    Devuelve:
        (float, bool) -> Densidad del fluido en las condiciones presentadas. En fase líquido. / boolean indicando si se asumió saturado
    """

    quimico = Chemical(cas, t, p)
    rho = quimico.rhol
    flag = False

    if(not rho):
        rho = obtener_densidad_liquido_saturado(quimico, t)
        flag = True

    return (rho, flag)

def obtener_densidad_liquido_saturado(quimico, t):
    psat = quimico.Psat
    quimico.calculate(t, psat + 10)
    return quimico.rhol

def calcular_densidad_relativa(cas: str, t: float, p: float = 101325) -> float:
    """
    Resumen:
        Esta función calculará la densidad de un fluido según su temperatura y presión.

    Parámetros:
        cas: str -> CAS del fluido
        t: float -> Temperatura inicial (K)
        p: float -> Presión (Pa)

    Devuelve:
        float -> Densidad del fluido en las condiciones presentadas.
    """

    quimico = Chemical(cas, t, p)
    rho = quimico.rhol

    if(not rho):
        rho = obtener_densidad_liquido_saturado(quimico, t)

    return rho/DENSIDAD_DEL_AGUA_LIQUIDA_A_5C