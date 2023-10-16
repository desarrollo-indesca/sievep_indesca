from thermo.heat_capacity import HeatCapacityGas, HeatCapacityLiquid # CLASES
import CoolProp.CoolProp as CP
from thermo.heat_capacity import heat_capacity_gas_methods, heat_capacity_liquid_methods
from thermo.chemical import Chemical
import numpy

def calcular_cp(fluido: str, t1: float, t2: float):
    """
    Resumen:
        Función para el cálculo de la capacidad calorífica del fluido mediante el CAS del fluido,
        temperatura de entrada y temperatura de salida.

    Parámetros:
        fluido: str -> CAS del fluido
        t1: float -> Temperatura inicial (K)
        t2: float -> Temperatura final (K)
    
    Devuelve:
        float: Cp del fluido en esas condiciones (J/KgK)
    """
    t = numpy.mean([t1, t2])
    quimico = Chemical(fluido)

    mw = quimico.MW # PESO MOLECULAR

    # Caso Especial del Aire
    if(quimico.Tb == None):
        return round(CP.PropsSI('C','P',101325,'T',t,'Air.mix'), 4)

    if(t >= quimico.Tb): # Caso Gas
        quimico = HeatCapacityGas(fluido)

        for metodo in heat_capacity_gas_methods: # Búsqueda del método permitido
            try:
                return round(quimico.calculate(t, metodo)/mw*1000,4)
            except:
                 continue
        cp = 0
    else: # Caso Líquido
        quimico = HeatCapacityLiquid(fluido)
        for metodo in heat_capacity_liquid_methods: # Búsqueda del método permitido
            try:
                return round(quimico.calculate(t, metodo)/mw*1000,4)
            except:
                 continue
        cp = 0

    return round(cp*1000, 4)