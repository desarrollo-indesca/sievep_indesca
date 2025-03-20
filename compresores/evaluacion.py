from CoolProp.CoolProp import PropsSI
from .models import COMPUESTOS
import math

def normalizacion(X: dict):
    """
    Normaliza un conjunto de datos X de tal manera que la suma de los elementos 
    normalizados sea igual a 1. 

    Args:
        X (list[float]): Lista de valores a normalizar.

    Returns:
        list[float]: Lista de valores normalizados.
    """
    total = sum([val for key,val in X.items()])
    for key, val in X.items():
        X[key] = val / total
    return X

def PMpromedio(x, PM):
    """
    Calcula el promedio ponderado de los elementos de x usando los pesos PM.

    Args:
        x (list[float]): Lista de valores a promediar.
        PM (list[float]): Lista de pesos correspondientes a cada valor en x.

    Returns:
        float: Promedio ponderado.
    """
    print(len(x), len(PM))
    PMprom = sum(xi * PM[i] for i, xi in enumerate(x))
    return PMprom

def FraccionMasica(x, PM):
    """
    Calcula la fracción másica de x utilizando los pesos PM.

    Args:
        x (list[float]): Lista de valores a calcular la fracción másica.
        PM (list[float]): Lista de pesos correspondientes a cada valor en x.

    Returns:
        list[float]: Lista de fracciones másicas.
    """
    total = sum(xi * PM[i] for i, xi in enumerate(x))
    y = [xi * PM[i] / total for i, xi in enumerate(x)]
    return y

def suma(z):
    """
    Suma todos los elementos de la lista z.

    Args:
        z (list[float]): Lista de valores a sumar.

    Returns:
        float: Suma total de los elementos en z.
    """
    return sum(z)

def PropiedadTermodinamica(PT, P, T, C):
    """
    Obtiene propiedades termodinámicas utilizando el módulo de propiedades.

    Args:
        PT (str): Tipo de propiedad.
        P (list[float]): Lista de presiones.
        T (list[float]): Lista de temperaturas.
        C (list[str]): Lista de componentes.

    Returns:
        list[list[float]]: Matriz de propiedades calculadas.
    """
    Propiedad = []
    for i in range(len(P)):
        a = [PropsSI(PT, 'P', P[i], 'T', T[i], C[j]) for j in range(len(C))]
        Propiedad.append(a)
    return Propiedad

def TotalPropiedad(x, H,):
    """
    Calcula la propiedad total sumando elementos de x y H.

    Args:
        x (list[list[float]]): Matriz de coeficientes.
        H (list[list[float]]): Matriz de propiedades.

    Returns:
        list[float]: Lista de propiedades totales.
    """
    total = []
    for i in range(len(x)):
        a = sum(x[i][j] * H[i][j] for j in range(11))
        total.append(a)
    return total

def EntalpiaIsoentropica(P, S, C):
    """
    Calcula la entalpía isotrópica usando presiones, entropías y componentes.

    Args:
        P (list[float]): Lista de presiones.
        S (list[list[float]]): Lista de entropías.
        C (list[str]): Lista de componentes.

    Returns:
        list[list[float]]: Matriz de entalpías calculadas.
    """
    Propiedad = []
    for i in range(len(P)):
        a = [PropsSI('H', 'P', P[i], 'S', S[i][j], C[j]) for j in range(len(C))]
        Propiedad.append(a)
    return Propiedad

def CpPromedio(z1, z2):
    """
    Calcula el promedio de dos listas de valores.

    Args:
        z1 (list[float]): Primera lista de valores.
        z2 (list[float]): Segunda lista de valores.

    Returns:
        list[float]: Lista de promedios de z1 y z2.
    """
    promedio = [(z1[i] + z2[i]) / 2 for i in range(len(z1))]
    return promedio

def evaluar_compresor(etapas):
    """
    Evaluar y calcular los parámetros de un compresor de 5 etapas.
    
    Lee los valores de entrada desde un sistema de interfaz HTML, normaliza los flujos,
    calcula el peso molecular promedio y las fracciones másicas, y luego calcula las
    propiedades termodinámicas y otros parámetros del compresor.

    Este método genera gráficos como parte del análisis final.
    """

    PresionE = [etapa['entradas']['presion_in'] for etapa in etapas]
    TemperaturaE = [etapa['entradas']['temperatura_in'] for etapa in etapas]
    PresionS = [etapa['entradas']['presion_out'] for etapa in etapas]
    TemperaturaS = [etapa['entradas']['temperatura_out'] for etapa in etapas]
    Flujo = [etapa['entradas']['flujo_gas'] for etapa in etapas]
    PotenciaTeorica = [etapa['entradas']['potencia_generada'] for etapa in etapas]

    for i,etapa in enumerate(etapas):
        etapas[i]['composiciones'] = normalizacion(etapa['composiciones'])

    # Cálculo del Peso Molecular Promedio
    PM = [2.016, 16.043, 28.054, 30.070, 42.081, 44.097, 56.107, 58.123, 72.150, 78.115, 18.020,0,0,0,0,0,0,0]

    PMprom = [PMpromedio(list(etapa['composiciones'].values()), PM) for etapa in etapas]

    y = [FraccionMasica(list(etapa['composiciones'].values()), PM) for etapa in etapas]

    # Cálculo de Propiedades Termodinámicas
    Compuestos = ['Hydrogen', 'Methane', 'Ethylene', 'Ethane', 'Propylene', 
                  'n-Propane', '1-Butene', 'n-Butane', 'n-Pentane', 'Benzene', 'Water']

    HEi = PropiedadTermodinamica('H', PresionE, TemperaturaE, Compuestos)
    HSi = PropiedadTermodinamica('H', PresionS, TemperaturaS, Compuestos)

    SEi = PropiedadTermodinamica('S', PresionE, TemperaturaE, Compuestos)
    SSi = PropiedadTermodinamica('S', PresionS, TemperaturaS, Compuestos)

    HSsi = EntalpiaIsoentropica(PresionS, SEi, Compuestos)

    CpEi = PropiedadTermodinamica('Cpmass', PresionE, TemperaturaE, Compuestos)
    CpSi = PropiedadTermodinamica('Cpmass', PresionS, TemperaturaS, Compuestos)

    CvEi = PropiedadTermodinamica('Cvmass', PresionE, TemperaturaE, Compuestos)
    CvSi = PropiedadTermodinamica('Cvmass', PresionS, TemperaturaS, Compuestos)

    ZEi = PropiedadTermodinamica('Z', PresionE, TemperaturaE, Compuestos)
    ZSi = PropiedadTermodinamica('Z', PresionS, TemperaturaS, Compuestos)

    # Cálculo de Propiedades por Etapa
    HE = TotalPropiedad(y, HEi)
    HS = TotalPropiedad(y, HSi)

    SE = TotalPropiedad(y, SEi)
    SS = TotalPropiedad(y, SSi)

    HSs = TotalPropiedad(y, HSsi)

    CpE = TotalPropiedad(y, CpEi)
    CpS = TotalPropiedad(y, CpSi)

    CvE = TotalPropiedad(y, CvEi)
    CvS = TotalPropiedad(y, CvSi)

    ZE = TotalPropiedad(y, ZEi)
    ZS = TotalPropiedad(y, ZSi)

    # Cálculo Capacidad Calorífica promedio
    CpEtapaPromedio = CpPromedio(CpE, CpS)
    CvEtapaPromedio = CpPromedio(CvE, CvS)

    # Cálculo del Coeficiente Isoentropico
    K = [CpEtapaPromedio[i] / CvEtapaPromedio[i] for i in range(len(CpEtapaPromedio))]
    Ke = [CpE[i] / CvE[i] for i in range(len(CpE))]
    Ks = [CpS[i] / CvS[i] for i in range(len(CpS))]

    # Cálculo de Eficiencia Isoentropica
    Eficiencia = [(HSs[i] - HE[i]) / (HS[i] - HE[i]) * 100 for i in range(len(HE))]

    # Cálculo de Potencia
    Potencia = [Flujo[i] / 3600 * (HS[i] - HE[i]) / 1000 for i in range(len(HE))]
    Cabezal = [(HS[i] - HE[i]) / 9.81 for i in range(len(HE))]

    PotenciaIso = [Flujo[i] / 3600 * (HSs[i] - HE[i]) / 1000 for i in range(len(HE))]
    CabezalIso = [(HSs[i] - HE[i]) / 9.81 for i in range(len(HE))]

    # Relación de Compresión
    RelacionCompresion = [PresionS[i] / PresionE[i] for i in range(len(PresionE))]
    RelacionTemperatura = [TemperaturaS[i] / TemperaturaE[i] for i in range(len(TemperaturaE))]

    # Coeficiente politropico
    n = [pow(1 - math.log(TemperaturaS[i] / TemperaturaE[i]) / math.log(PresionS[i] / PresionE[i]), -1) for i in range(len(PresionE))]

    # Cálculo de la eficiencia real
    EficienciaTeorica = [PotenciaTeorica[i] / Potencia[i] * 100 for i in range(len(K))]

    # Diferencial de presión y temperatura entre etapas
    PresionD = []
    TemperaturaD = []
    DH = []
    for i in range(len(etapas) - 1):
        PresionD.append(PresionS[i] - PresionE[i + 1])
        TemperaturaD.append(TemperaturaS[i] - TemperaturaE[i + 1])
        DH.append(HS[i] - HE[i + 1])

    # Cálculo Flujo Volumetrico por etapa
    FlujoVolumetricoCe = []
    FlujoVolumetricoCs = []
    for i in range(len(etapas)):
        FlujoVolumetricoCe.append(Flujo[i] / PMprom[i] * TemperaturaE[i] / PresionE[i] * 8.314466e3)
        FlujoVolumetricoCs.append(Flujo[i] / PMprom[i] * TemperaturaS[i] / PresionS[i] * 8.314466e3)

    # Relación Volumetrica
    RelacionVolumetrica = [FlujoVolumetricoCs[i] / FlujoVolumetricoCe[i] for i in range(len(FlujoVolumetricoCe))]

    return {
        "k_prom": K,
        "k_in": Ke,
        "k_out": Ks,
        "eficiencia": Eficiencia,
        "potencia": Potencia,
        "cabezal": Cabezal,
        "potencia_iso": PotenciaIso,
        "cabezal_iso": CabezalIso,
        "relacion_compresion": RelacionCompresion,
        "relacion_temperatura": RelacionTemperatura,
        "n": n,
        "eficiencia_teorica": EficienciaTeorica,
        "caida_presion": PresionD,
        "caida_temperatura": TemperaturaD,
        "energia_ret": DH,
        "flujo_entrada": FlujoVolumetricoCe,
        "flujo_salida": FlujoVolumetricoCs,
        "relacion_volumetrica": RelacionVolumetrica,
        "z_in": ZE,
        "z_out": ZS,
        "pm_calculado": PMprom
    }
