from thermo.heat_capacity import HeatCapacityGas, HeatCapacityLiquid
from thermo.chemical import Chemical
import numpy

def calcular_cp(fluido, t1, t2):

    t = numpy.mean([t1, t2])
    quimico = Chemical(fluido)
    mw = quimico.MW # PESO MOLECULAR
    
    if(t >= quimico.Tb):
        quimico = HeatCapacityGas(fluido)
        try:
            cp = quimico.calculate(t,'JOBACK') / mw
        except:
            try:
                cp = quimico.calculate(t,'TRCIG') / mw
            except:
                cp = 0
    else:
        quimico = HeatCapacityLiquid(fluido)
        try:
            cp = quimico.calculate(t,'HEOS_FIT') / mw
        except:
            try:
                cp = quimico.calculate(t,'ZABRANSKY_SPLINE') / mw
            except:
                cp = 0

    return round(cp*1000, 4)