from thermo.chemical import Chemical
from thermo.mixture import Mixture
import CoolProp.CoolProp as CP
from .unidades import transformar_unidades_cp
import numpy

def calcular_cp(fluido: str, t1: float, t2: float, unidad_salida: int = 29, presion: float = 101325):
    """
    Resumen:
        Función para el cálculo de la capacidad calorífica del fluido mediante el CAS del fluido,
        temperatura de entrada y temperatura de salida.

    Parámetros:
        fluido: str -> CAS del fluido
        t1: float -> Temperatura inicial (K)
        t2: float -> Temperatura final (K)
        unidad_salida: int -> ID de la unidad de salida
        presion: float -> Presión
    
    Devuelve:
        float: Cp del fluido en esas condiciones 
    """
    
    t = numpy.mean([t1, t2])
    
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
                cp = CP.PropsSI('C','T',t,'P',presion,name)
                break
            except:
                continue
        
        if(cp == None):
            raise Exception     
    except: # Cálculo de Cp con Thermo (En caso de falla)
        cp = quimico.Cp 
        print("THERMO")

    return round(transformar_unidades_cp([cp], 29, unidad_salida)[0], 4)

def calcular_entalpia_entre_puntos(fluido: str, t1: float, t2: float, presion: float):
    quimico = Chemical(fluido,T=t1, P=presion)
    tsat = quimico.Tsat(P=presion)

    if(t1 <= tsat): # Caso Líquido > Gas
        return entalpia_l_a_g(quimico, t1, t2, presion, tsat)
    else: # Caso Gas > Líquido
        return entalpia_g_a_l(quimico, t1, t2, presion, tsat)

def entalpia_l_a_g(quimico: Chemical, t1: float, t2: float, presion: float, tsat: float):
    try:
        h_liquido_subenfriado = numpy.ceil(quimico.HeatCapacityLiquid.T_dependent_property_integral(t1,tsat)/quimico.MW  
                                - quimico.calc_H_excess(T=tsat, P=presion)/1000)
    except:
        h_liquido_subenfriado = numpy.ceil(quimico.HeatCapacityLiquid.T_dependent_property_integral(t1,tsat)/quimico.MW)

    quimico.calculate(tsat, P=presion)

    try:
        h_liquido_saturado = numpy.ceil(quimico.Hvap/1000 - quimico.calc_H_excess(T=tsat, P=presion)/1000)
    except:
        h_liquido_saturado = numpy.ceil(quimico.Hvap/1000)

    quimico.calculate(t2)

    try:
        h_vapor_sobrecalentado = numpy.ceil(quimico.HeatCapacityGas.T_dependent_property_integral(tsat,t2)/quimico.MW
                                    - quimico.calc_H_excess(T=t2, P=presion)/1000)
    except:
        h_vapor_sobrecalentado = numpy.ceil(quimico.HeatCapacityGas.T_dependent_property_integral(tsat,t2)/quimico.MW)

    return numpy.ceil(h_liquido_subenfriado+h_vapor_sobrecalentado+h_liquido_saturado)

def entalpia_g_a_l(quimico: Chemical, t1: float, t2: float, presion: float, tsat: float):
    try:
        h_vapor_sobrecalentado = numpy.ceil(quimico.HeatCapacityGas.T_dependent_property_integral(t1,tsat)/quimico.MW
                                - quimico.calc_H_excess(T=tsat, P=presion)/1000) 
    except:
        h_vapor_sobrecalentado = numpy.ceil(quimico.HeatCapacityGas.T_dependent_property_integral(t1,tsat)/quimico.MW) 
    
    quimico.calculate(tsat, P=presion)

    try:
        h_liquido_saturado = numpy.ceil(quimico.Hvap/1000 - quimico.calc_H_excess(T=tsat, P=presion)/1000) 
    except:
        h_liquido_saturado = numpy.ceil(quimico.Hvap/1000) 
    
    quimico.calculate(t2)
    
    try:
        h_liquido_subenfriado = numpy.ceil(quimico.HeatCapacityLiquid.T_dependent_property_integral(tsat,t1)/quimico.MW  
                                - quimico.calc_H_excess(T=tsat, P=presion)/1000)
    except:
        h_liquido_subenfriado = numpy.ceil(quimico.HeatCapacityLiquid.T_dependent_property_integral(tsat,t1)/quimico.MW)

    return numpy.ceil(h_liquido_subenfriado+h_vapor_sobrecalentado+h_liquido_saturado)