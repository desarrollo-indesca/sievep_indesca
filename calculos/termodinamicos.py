from thermo.heat_capacity import HeatCapacityGas, HeatCapacityLiquid
from thermo.chemical import Chemical
from calculos.unidades import normalizar_unidades_temperatura
import numpy

def calcular_cp(fluido, t1, t2):

    t = numpy.mean([t1, t2])
    quimico = Chemical(fluido) # PESO MOLECULAR
    mw = quimico.MW

    if(t >= quimico.Tb):
        print("GAS")
        quimico = HeatCapacityGas(fluido)
        try:
            cp = quimico.calculate(t,'JOBACK') / mw
        except:
            try:
                cp = quimico.calculate(t,'TRCIG') / mw
            except:
                cp = 0
    else:
        print("LIQUIDO")
        quimico = HeatCapacityLiquid(fluido)
        try:
            cp = quimico.calculate(t,'HEOS_FIT') / mw
        except:
            try:
                cp = quimico.calculate(t,'ZABRANSKY_SPLINE') / mw
            except:
                cp = 0

    return round(cp*1000, 4)