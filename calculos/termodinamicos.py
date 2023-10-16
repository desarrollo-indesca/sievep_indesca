from thermo.heat_capacity import HeatCapacityGas, HeatCapacityLiquid # CLASES
import CoolProp.CoolProp as CP
from thermo.heat_capacity import heat_capacity_gas_methods, heat_capacity_liquid_methods
from thermo.chemical import Chemical
import numpy

def calcular_cp(fluido, t1, t2):
    t = numpy.mean([t1, t2])
    quimico = Chemical(fluido)

    mw = quimico.MW # PESO MOLECULAR

    if(quimico.Tb == None):
        return round(CP.PropsSI('C','P',101325,'T',t,'Air.mix'), 4)

    if(t >= quimico.Tb):
        quimico = HeatCapacityGas(fluido)

        for metodo in heat_capacity_gas_methods:
            try:
                return round(quimico.calculate(t, metodo)/mw*1000,4)
            except:
                 continue
        cp = 0
    else:
        quimico = HeatCapacityLiquid(fluido)
        for metodo in heat_capacity_liquid_methods:
            try:
                return round(quimico.calculate(t, metodo)/mw*1000,4)
            except:
                 continue
        cp = 0

    return round(cp*1000, 4)