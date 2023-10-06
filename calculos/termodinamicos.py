from thermo.heat_capacity import HeatCapacityGas
from thermo.chemical import Chemical
import numpy

def calcular_cp(fluido, t1, t2):

    t = numpy.mean([t1, t2])
    quimico = HeatCapacityGas(fluido)

    mw = Chemical(fluido).MW # PESO MOLECULAR
    
    try:
        cp = quimico.calculate(t,'JOBACK') / mw
    except:
        try:
            cp = quimico.calculate(t,'TRCIG') / mw
        except:
            cp = 0

    return round(cp*1000, 4)