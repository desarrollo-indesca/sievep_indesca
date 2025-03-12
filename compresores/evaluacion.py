from CoolProp.CoolProp import PropsSI
import math

def normalizacion(X):
    """
    Normaliza un conjunto de datos X de tal manera que la suma de los elementos 
    normalizados sea igual a 1. 

    Args:
        X (list[float]): Lista de valores a normalizar.

    Returns:
        list[float]: Lista de valores normalizados.
    """
    total = sum(X)
    x = [xi / total for xi in X]
    return x

def PMpromedio(x, PM):
    """
    Calcula el promedio ponderado de los elementos de x usando los pesos PM.

    Args:
        x (list[float]): Lista de valores a promediar.
        PM (list[float]): Lista de pesos correspondientes a cada valor en x.

    Returns:
        float: Promedio ponderado.
    """
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

def TotalPropiedad(x, H):
    """
    Calcula la propiedad total sumando elementos de x y H.

    Args:
        x (list[list[float]]): Matriz de coeficientes.
        H (list[list[float]]): Matriz de propiedades.

    Returns:
        list[float]: Lista de propiedades totales.
    """
    total = []
    for i in range(5):
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

def evaluar():
    """
    Evaluar y calcular los parámetros de un compresor de 5 etapas.
    
    Lee los valores de entrada desde un sistema de interfaz HTML, normaliza los flujos,
    calcula el peso molecular promedio y las fracciones másicas, y luego calcula las
    propiedades termodinámicas y otros parámetros del compresor.

    Este método genera gráficos como parte del análisis final.
    """
    # Etiquetas para los elementos HTML
    Etiquetas = [
        ['PM1', 'Flujo1', 'PresionE1', 'PresionS1', 'TemperaturaE1', 'TemperaturaS1', 'Ki1', 'Ks1', 'Zi1', 'Zs1', 'FlujoVolumetrico1', 'PotenciaTeorica1', 'RPM1', 'FlujoSurge1', 'Hpoly1', 'EficPoly1'],
        ['PM2', 'Flujo2', 'PresionE2', 'PresionS2', 'TemperaturaE2', 'TemperaturaS2', 'Ki2', 'Ks2', 'Zi2', 'Zs2', 'FlujoVolumetrico2', 'PotenciaTeorica2', 'RPM2', 'FlujoSurge2', 'Hpoly2', 'EficPoly2'],
        ['PM3', 'Flujo3', 'PresionE3', 'PresionS3', 'TemperaturaE3', 'TemperaturaS3', 'Ki3', 'Ks3', 'Zi3', 'Zs3', 'FlujoVolumetrico3', 'PotenciaTeorica3', 'RPM3', 'FlujoSurge3', 'Hpoly3', 'EficPoly3'],
        ['PM4', 'Flujo4', 'PresionE4', 'PresionS4', 'TemperaturaE4', 'TemperaturaS4', 'Ki4', 'Ks4', 'Zi4', 'Zs4', 'FlujoVolumetrico4', 'PotenciaTeorica4', 'RPM4', 'FlujoSurge4', 'Hpoly4', 'EficPoly4'],
        ['PM5', 'Flujo5', 'PresionE5', 'PresionS5', 'TemperaturaE5', 'TemperaturaS5', 'Ki5', 'Ks5', 'Zi5', 'Zs5', 'FlujoVolumetrico5', 'PotenciaTeorica5', 'RPM5', 'FlujoSurge5', 'Hpoly5', 'EficPoly5']
    ]

    PresionE = []
    TemperaturaE = []
    PresionS = []
    TemperaturaS = []
    Flujo = []
    PotenciaTeorica = []
    FlujoVolumetrico = []
    Hpoly = []

    for i in range(5):
        PresionE.append(float(input(f"Valor de {Etiquetas[i][2]}: ")) * 1e5)
        TemperaturaE.append(float(input(f"Valor de {Etiquetas[i][4]}: ")) + 273.15)
        PresionS.append(float(input(f"Valor de {Etiquetas[i][3]}: ")) * 1e5)
        TemperaturaS.append(float(input(f"Valor de {Etiquetas[i][5]}: ")) + 273.15)
        Flujo.append(float(input(f"Valor de {Etiquetas[i][1]}: ")))
        FlujoVolumetrico.append(float(input(f"Valor de {Etiquetas[i][10]}: ")))
        PotenciaTeorica.append(float(input(f"Valor de {Etiquetas[i][11]}: ")))
        Hpoly.append(float(input(f"Valor de {Etiquetas[i][14]}: ")))

    EtiquetasX = [['X1H2', 'X2H2', 'X3H2', 'X4H2', 'X5H2'],
                   ['X1CH4', 'X2CH4', 'X3CH4', 'X4CH4', 'X5CH4'],
                   ['X1C2H4', 'X2C2H4', 'X3C2H4', 'X4C2H4', 'X5C2H4'],
                   ['X1C2H6', 'X2C2H6', 'X3C2H6', 'X4C2H6', 'X5C2H6'],
                   ['X1C3H6', 'X2C3H6', 'X3C3H6', 'X4C3H6', 'X5C3H6'],
                   ['X1C3H8', 'X2C3H8', 'X3C3H8', 'X4C3H8', 'X5C3H8'],
                   ['X1C4H8', 'X2C4H8', 'X3C4H8', 'X4C4H8', 'X5C4H8'],
                   ['X1C4H10', 'X2C4H10', 'X3C4H10', 'X4C4H10', 'X5C4H10'],
                   ['X1C5H12', 'X2C5H12', 'X3C5H12', 'X4C5H12', 'X5C5H12'],
                   ['X1C6H6', 'X2C6H6', 'X3C6H6', 'X4C6H6', 'X5C6H6'],
                   ['X1H2O', 'X2H2O', 'X3H2O', 'X4H2O', 'X5H2O']]

    X1, X2, X3, X4, X5 = [], [], [], [], []
    
    for i in range(11):
        X1.append(float(input(f"Valor de {EtiquetasX[i][0]}: ")))
        X2.append(float(input(f"Valor de {EtiquetasX[i][1]}: ")))
        X3.append(float(input(f"Valor de {EtiquetasX[i][2]}: ")))
        X4.append(float(input(f"Valor de {EtiquetasX[i][3]}: ")))
        X5.append(float(input(f"Valor de {EtiquetasX[i][4]}: ")))

    x1 = normalizacion(X1)
    x2 = normalizacion(X2)
    x3 = normalizacion(X3)
    x4 = normalizacion(X4)
    x5 = normalizacion(X5)

    x = [x1, x2, x3, x4, x5]

    # Cálculo del Peso Molecular Promedio
    PM = [2.016, 16.043, 28.054, 30.070, 42.081, 44.097, 56.107, 58.123, 72.150, 78.115, 18.020]

    PMprom = [PMpromedio(xi, PM) for xi in x]

    y = [FraccionMasica(xi, PM) for xi in x]

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

    ZE = TotalPropiedad(x, ZEi)
    ZS = TotalPropiedad(x, ZSi)

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

    # Eficiencia Isoentropica ecuación de relación Presion y Temperatura
    Eficienciar = [(TemperaturaE[i] / (TemperaturaS[i] - TemperaturaE[i])) * (pow(RelacionCompresion[i], (K[i] - 1) / K[i]) - 1) * 100 for i in range(len(RelacionCompresion))]

    # Cálculo de eficiencia Politropica
    EficienciaPolitropica = [((K[i] - 1) / K[i]) / ((n[i] - 1) / n[i]) * 100 for i in range(len(K))]

    # Cálculo de la eficiencia real
    EficienciaTeorica = [PotenciaTeorica[i] / Potencia[i] * 100 for i in range(len(K))]

    # Cálculo Temperatura Isoentropica
    TemperaturaIsoentropica = [TemperaturaE[i] * pow(RelacionCompresion[i], (K[i] - 1) / K[i]) for i in range(len(K))]

    # Diferencial de presión y temperatura entre etapas
    PresionD = []
    TemperaturaD = []
    DH = []
    for i in range(4):
        PresionD.append(PresionS[i] - PresionE[i + 1])
        TemperaturaD.append(TemperaturaS[i] - TemperaturaE[i + 1])
        DH.append(HS[i] - HE[i + 1])

    # Cálculo Flujo Volumetrico por etapa
    FlujoVolumetricoCe = []
    FlujoVolumetricoCs = []
    for i in range(5):
        FlujoVolumetricoCe.append(Flujo[i] / PMprom[i] * TemperaturaE[i] / PresionE[i] * 8.314466e3)
        FlujoVolumetricoCs.append(Flujo[i] / PMprom[i] * TemperaturaS[i] / PresionS[i] * 8.314466e3)

    # Relación Volumetrica
    RelacionVolumetrica = [FlujoVolumetricoCs[i] / FlujoVolumetricoCe[i] for i in range(len(FlujoVolumetricoCe))]

    # Cálculo delta de Entalpia
    DeltaH = [HS[i] - HE[i] for i in range(5)]
    DeltaHs = [HSs[i] - HE[i] for i in range(5)]

    # Cálculo de energía con el CP
    DeltaHcp = [CpEtapaPromedio[i] * (TemperaturaS[i] - TemperaturaE[i]) for i in range(5)]
    DeltaHcpIso = [CpEtapaPromedio[i] * (TemperaturaIsoentropica[i] - TemperaturaE[i]) for i in range(5)]
