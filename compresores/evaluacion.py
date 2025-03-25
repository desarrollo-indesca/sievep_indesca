from CoolProp.CoolProp import PropsSI
from bokeh.embed import components
from bokeh.plotting import figure

from .models import COMPUESTOS, EntradaEtapaEvaluacion
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
        "pm_calculado": PMprom,
        'HE': HE,
        'HS': HS
    }

def generar_grafica_presion_h(entradas=None, resultados=None, evaluacion=None,):
    """
    Genera un gráfico de Presiones vs Entalpías.

    Args:
        evaluacion (object, optional): Objeto de evaluación con datos de entrada. Defaults to None.
        entradas (list, optional): Lista de diccionarios con datos de entrada. Defaults to None.
        resultados (dict, optional): Diccionario con datos de resultados. Defaults to None.

    Returns:
        Un diccionario con el script y el div para incrustar el gráfico.
    """

    if evaluacion is not None:
        entradas = evaluacion.entradas_evaluacion.all()
        resultados = {
            'HE': [entrada.salidas.he for entrada in entradas],
            'HS': [entrada.salidas.hs for entrada in entradas]
        }

    y1 = [x['presion_in'] if isinstance(x, dict) else x.presion_in for x in entradas]
    y2 = [x['presion_out'] if isinstance(x, dict) else x.presion_out for x in entradas]

    p = figure(
        title="Presiones vs Entalpías",
        x_axis_label='Entalpías (kJ/kg)', y_axis_label='Presiones (bar)'
    )
    p.line(x=resultados['HE'], y=y1, color="blue", legend_label="H vs P Entrada") 
    p.line(x=resultados['HS'], y=y2, color="red", legend_label="H vs P Salida")
    script, div = components(p)
    return {'script': script, 'div': div}
        
def generar_presion_flujo(entradas=None, evaluacion=None):
    """
    Genera un gráfico de Presión vs Flujo Volumétrico.

    Args:
        entradas (list, optional): Lista de diccionarios con datos de entrada. Defaults to None.
        evaluacion (object, optional): Objeto de evaluación con datos de entrada. Defaults to None.

    Returns:
        Un diccionario con el script y el div para incrustar el gráfico.
    """

    p = figure(title="Presión vs Flujo Volumétrico",
               x_axis_label='Presión (bar)', y_axis_label='Flujo Volumétrico (m3/h)')

    if entradas is not None:
        flujo_volumetrico = [entrada['flujo_volumetrico'] for entrada in entradas]
        presion_entrada = [entrada['presion_in'] for entrada in entradas]

    elif evaluacion is not None:
        entradas = evaluacion.entradas_evaluacion.all()
        flujo_volumetrico = [entrada.flujo_volumetrico for entrada in entradas]
        presion_entrada = [entrada.presion_in for entrada in entradas]

    else:
        return {'script': '', 'div': ''} #Return empty values if no data is provided.

    x_coords = [fv / 1e2 for fv in flujo_volumetrico[:-1]]
    y_coords_start = [1000 - 25 * pe / 1e5 for pe in presion_entrada[:-1]]
    y_coords_end = [1000 - 25 * pe / 1e5 for pe in presion_entrada[1:]]

    p.segment(x0=y_coords_start, y0=x_coords, x1=y_coords_end, y1=x_coords[1:], color="blue", legend_label="Real")
    script, div = components(p)

    return {'script': script, 'div': div}

def generar_cabezal_flujo(entradas=None, resultados=None, evaluacion=None):
    if evaluacion:
        entradas = evaluacion.entradas_evaluacion.all()
        resultados = [entrada.salidas for entrada in entradas]
        entradas = [entrada for entrada in entradas]
    else:
        entradas = entradas[:-1]
        resultados_calculado = resultados['cabezal']
        resultados_isotropico = resultados['cabezal_iso']

    p = figure(title="Cabezales vs Flujo Volumétrico", x_axis_label='Flujo Volumétrico (m3/s)', 
               y_axis_label='Cabezal (m)')
    
    # Blue lines (Real)
    x_blue = [entrada.flujo_volumetrico / 1e2 if evaluacion else entrada['flujo_volumetrico'] / 1e2 for entrada in entradas]
    y_blue_start = [1000 - 0.08 * (resultados[i].cabezal_calculado if evaluacion else resultados_calculado[i]) for i in range(len(entradas))]
    y_blue_end = [1000 - 0.08 * (resultados[i + 1].cabezal_calculado if evaluacion else resultados_calculado[i + 1]) for i in range(len(entradas) - 1)]
    p.segment(x0=x_blue, y0=y_blue_start, x1=x_blue[1:], y1=y_blue_end, color="blue", legend_label="Real")

    # Red lines (Iso)
    y_red_start = [1000 - 0.08 * (resultados[i].cabezal_isotropico if evaluacion else resultados_isotropico[i]) for i in range(len(entradas))]
    y_red_end = [1000 - 0.08 * (resultados[i + 1].cabezal_isotropico if evaluacion else resultados_isotropico[i + 1]) for i in range(len(entradas) - 1)]
    p.segment(x0=x_blue, y0=y_red_start, x1=x_blue[1:], y1=y_red_end, color="red", legend_label="Isoentrópico")

    # Green lines (Hpoly)
    y_green_start = [1000 - 0.08 * (resultados[i].cabezal_calculado if evaluacion else resultados_calculado[i]) for i in range(len(entradas))]
    y_green_end = [1000 - 0.08 * (resultados[i + 1].cabezal_calculado if evaluacion else resultados_calculado[i + 1]) for i in range(len(entradas) - 1)]
    p.segment(x0=x_blue, y0=y_green_start, x1=x_blue[1:], y1=y_green_end, color="green", legend_label="Politrópico")

    script, div = components(p)
    return {'script': script, 'div': div}

