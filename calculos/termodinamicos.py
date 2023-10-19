from thermo.chemical import Chemical
from thermo.mixture import Mixture
from .unidades import transformar_unidades_cp
import numpy

def calcular_cp(fluido: str, t1: float, t2: float, unidad_salida = 29):
    """
    Resumen:
        Función para el cálculo de la capacidad calorífica del fluido mediante el CAS del fluido,
        temperatura de entrada y temperatura de salida.

    Parámetros:
        fluido: str -> CAS del fluido
        t1: float -> Temperatura inicial (K)
        t2: float -> Temperatura final (K)
        unidad_salida: int -> ID de la unidad de salida
    
    Devuelve:
        float: Cp del fluido en esas condiciones 
    """
    
    t = numpy.mean([t1, t2])
    cp = Chemical(fluido,T=t).Cp if fluido != '132259-10-0' else Mixture('air',T=t).Cp

    return round(transformar_unidades_cp([cp], 29, unidad_salida)[0], 4)