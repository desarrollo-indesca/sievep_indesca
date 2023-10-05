from thermo.heat_capacity import HeatCapacityGas
import numpy

def calcular_cp(fluido, t1, t2, unidad = 'K'):
    if(unidad == 'C'):
        t1 = float(t1)
        t1 += 273.15

        t2 = float(t2)
        t2 += 273.15

    t = numpy.mean([t1, t2])
    quimico = HeatCapacityGas(fluido)

    cp = quimico.calculate(t, 'POLING_POLY')

    return round(cp, 4)