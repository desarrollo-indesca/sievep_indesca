import numpy as np
from .unidades import transformar_unidades_temperatura, transformar_unidades_flujo, transformar_unidades_longitud, transformar_unidades_presion, transformar_unidades_cp
from ht import F_LMTD_Fakheri
from .termodinamicos import calcular_entalpia_entre_puntos, calcular_tsat_hvap

def evaluacion_tubo_carcasa(intercambiador, ti, ts, Ti, Ts, ft, Fc, nt, cp_gas_tubo = None, cp_liquido_tubo = None, cp_gas_carcasa = None, cp_liquido_carcasa = None, unidad_temp = 1, unidad_flujo = 6) -> dict:
    ti,ts,Ti,Ts = transformar_unidades_temperatura([ti,ts,Ti,Ts], unidad=unidad_temp)
    
    if(unidad_flujo != 10):
        ft,Fc = transformar_unidades_flujo([ft,Fc], unidad_flujo)

    q_tubo = calcular_calor(ft, ti, ts, cp_gas_tubo, cp_liquido_tubo, intercambiador, 'T') # W
    q_carcasa = calcular_calor(Fc, Ti, Ts, cp_gas_carcasa, cp_liquido_carcasa, intercambiador, 'C') # W

    print(q_tubo)
    print(q_carcasa)
    
    nt = nt if nt else float(intercambiador.numero_tubos)

    diametro_tubo = transformar_unidades_longitud([float(intercambiador.diametro_externo_tubos)], intercambiador.diametro_tubos_unidad.pk)[0]
    longitud_tubo = transformar_unidades_longitud([float(intercambiador.longitud_tubos)], intercambiador.longitud_tubos_unidad.pk)[0]

    area_calculada = np.pi*diametro_tubo*nt*longitud_tubo #m2
    dtml = abs(((Ts - ti) - (Ti - ts))/np.log(abs((Ts - ti)/(Ti - ts)))) #K
    num_pasos_carcasa = float(intercambiador.numero_pasos_carcasa)
    num_pasos_tubo = float(intercambiador.numero_pasos_tubo)

    factor = round(F_LMTD_Fakheri(Ti, Ts, ti, ts, num_pasos_carcasa),3) 
    
    print(f"FACTOR: {factor}")
    q_prom = np.mean([q_tubo,q_carcasa]) # W
    ucalc = q_prom/(area_calculada*dtml*factor) # Wm2/K
    RF = 1/ucalc - 1/float(intercambiador.u) 
    
    ct = ft*cp_gas_tubo if cp_gas_tubo else ft*cp_liquido_tubo 
    cc = Fc*cp_gas_carcasa if cp_gas_carcasa else Fc*cp_liquido_carcasa 

    if(ct < cc):
        cmin = ct
        cmax = cc
        minimo = 1
    else:
        cmin = cc
        cmax = ct
        minimo = 2

    c = cmin/cmax
    ntu = ucalc*area_calculada/cmin

    if(c == 0):
        eficiencia = 1 - np.exp(-1*ntu)
    else:
        if(num_pasos_tubo > 2):
            eficiencia1 = 2/(1+c+pow(1+pow(c,2),0.5)*(1+np.exp(-1*ntu*pow((1-pow(c,2)),0.5)))/(1-np.exp(-1*ntu*pow((1-pow(c,2)),0.5))))
            eficiencia = eficiencia1
        else:
            if(minimo == 1):
                eficiencia=1/c*(1-np.exp(-1*c*(1-1*np.exp(-1*ntu))))
            else:
                eficiencia=1-np.exp(-1/c*np.exp(1-np.exp(-1*ntu*c)))

        if(num_pasos_carcasa > 1):
            if(c == 1):
                eficiencia=num_pasos_carcasa*eficiencia1/(1+(num_pasos_carcasa-1)*eficiencia1)
            else:
                eficiencia=(pow((1-eficiencia1*c)/(1-eficiencia1),num_pasos_carcasa)-1)/(pow((1-eficiencia1*c)/(1-eficiencia1),num_pasos_carcasa)-c)

    efectividad = eficiencia*ntu

    resultados = {
        'q': round(q_prom,4),
        'area': round(area_calculada,4),
        'lmtd': round(dtml,4),
        'eficiencia': round(eficiencia*100,2),
        'efectividad': round(efectividad*100, 2),
        'ntu': round(ntu,4),
        'u': round(ucalc,8),
        'ua': round(ucalc*area_calculada,4),
        'factor_ensuciamiento': round(RF,4),
    }

    return resultados

def calcular_calor(flujo: float, t1: float, t2: float, cp_gas: float, cp_liquido: float,  intercambiador, lado: str = 'T') -> float:
    """
    Resumen:
        Esta función calcula el calor intercambiado en uno de los lados de un intercambiador.
    
    Parámetros:
        flujo: float -> Flujo másico (Kg/s)
        t1: float -> Temperatura de Entrada (K)
        t2: float -> Temperatura de Salida (K)
        intercambiador: Intercambiador -> Intercambiador al cual se le calculará el calor.
        cp: float -> Cp en J/KgK del fluido
        lado: str -> T si es el calor del lado del tubo, C si es el calor de la carcasa.

    Devuelve:
        float -> Q (W) del lado del intercambiador
    """

    fluido = intercambiador.fluido_tubo if lado == 'T' else intercambiador.fluido_carcasa
    datos = intercambiador.condicion_tubo() if lado == 'T' else intercambiador.condicion_carcasa()
    presion = transformar_unidades_presion([float(datos.presion_entrada)], datos.unidad_presion)[0]

    if(fluido == None):
        fluido = datos.fluido_etiqueta if lado == 'T' else datos.fluido_etiqueta

    if(datos.cambio_de_fase == 'S'): # Caso 1: Sin Cambio de Fase
        return flujo * cp_liquido * abs(t2-t1) if cp_liquido else flujo * cp_gas * abs(t2-t1)
    elif(datos.cambio_de_fase == 'P'):
        flujo_vapor_in = float(datos.flujo_vapor_entrada)
        flujo_vapor_out = float(datos.flujo_vapor_salida)
        flujo_liquido_in = float(datos.flujo_liquido_entrada)
        flujo_liquido_out = float(datos.flujo_liquido_salida)
        cdf = determinar_cambio_parcial(flujo_vapor_in, flujo_vapor_out, flujo_liquido_in, flujo_liquido_out)
        calidad = flujo_vapor_out/(flujo_liquido_out+flujo_vapor_out)

        if(type(fluido) != str):
                _,hvap = calcular_tsat_hvap(fluido.cas, presion)
        else:
            hvap = float(datos.hvap) if datos.hvap else 5000

        if(cdf == 'DD'):
            return hvap*calidad*flujo
        elif(cdf == 'DL'):
            return abs(flujo*(-hvap*calidad + (t2-t1)*cp_liquido))
        elif(cdf == 'DV'):
            return flujo*(hvap*calidad + (t2-t1)*cp_gas)
        elif(cdf == 'LD'):
            return flujo*((t2-t1)*cp_liquido + hvap*calidad)
        elif(cdf == 'VD'):
            return abs(flujo*((t2-t1)*cp_gas - hvap*calidad))
    else: # Caso 2: Cambio de Fase Total
        if(datos.tipo_cp == 'A'):
            return flujo*calcular_entalpia_entre_puntos(fluido.cas, t1, t2, presion)
        else:
            if(type(fluido) != str):
                tsat,hvap = calcular_tsat_hvap(fluido.cas, presion)
            else:
                tsat = transformar_unidades_temperatura([float(datos.tsat)], datos.temperaturas_unidad)[0]
                hvap = float(datos.hvap) if datos.hvap else 5000
            
            fluido_cp_gas, fluido_cp_liquido = transformar_unidades_cp([cp_gas,cp_liquido], datos.unidad_cp)

            if(t1 <= t2): # Vaporización
                return flujo*(fluido_cp_gas*(t2-tsat)+hvap+fluido_cp_liquido*(tsat-t1))
            else: # Condensación
                return abs(flujo*(fluido_cp_gas*(tsat-t1)-hvap+fluido_cp_liquido*(t2-tsat)))
                       
    # elif(datos.cambio_de_fase == 'P'): # Caso 3: Cambio de Fase Parcial
        # pass  

def obtener_cambio_fase(flujo_vapor_in: float, flujo_vapor_out: float, flujo_liquido_in: float, flujo_liquido_out: float) -> str:
    """
    Resumen:
        Función que determina el tipo de cambio de fase dados los flujos en líquido y en vapor.
    
    Parámetros:
        flujo_vapor_in: float -> Flujo de vapor de entrada.
        flujo_vapor_out float -> Flujo de vapor de salida.
        flujo_liquido_in: float -> Flujo de líquido de entrada.
        flujo_liquido_out: float -> Flujo de líquido de salida.
    
    Devuelve:
        str -> Letra indicando el cambio de fase. P si es parcial. S si no tiene. T si es total.
    """

    if(flujo_vapor_in and flujo_liquido_in):
        if(flujo_vapor_in != flujo_vapor_out):
            return "P"
        else:
           return "S"

    if(flujo_vapor_in):
        if(flujo_vapor_in == flujo_vapor_out):
            return "S"
        elif(flujo_vapor_in == flujo_liquido_out):
            return "T"
        else:
            return "P"
    elif(flujo_liquido_in):
        if(flujo_liquido_out == flujo_liquido_in):
            return "S"
        elif(flujo_liquido_in == flujo_vapor_out):
            return "T"
        else:
            return "P"

def determinar_cambio_parcial(flujo_vapor_in: float, flujo_vapor_out: float, flujo_liquido_in: float, flujo_liquido_out: float):
    if(flujo_vapor_in == 0): # Líquido a Domo
        return "LD"
    elif(flujo_liquido_in == 0): # Vapor a Domo
        return "VD"
    elif(flujo_liquido_out == 0): # Domo a Vapor
        return "DV"
    elif(flujo_vapor_out == 0): # Domo a Líquido
        return "DL"
    else: # Domo a Domo
        return "DD"

def truncar(numero: float, decimales: int = 2) -> float:
    """
    Resumen:
        Rutina para truncar los números a la cantidad de decimales enviada (por defecto 2).

    Parámetros:
        numero: float -> Número a truncar.
        decimales: int -> Cantidad de decimales.

    Devuelve:
        float -> Número truncado.
    """
    factor = 10**decimales
    return int(numero*factor)/factor

def factor_correccion_tubo_carcasa(ti, ts, Ti, Ts, num_pasos_tubo, num_pasos_carcasa) -> float:
    '''
    Resumen:
        Rutina aproximada para el factor de corrección de LMTD.
    '''
    try:
        P = abs((ts - ti)/(Ti - ti))
    except:
        P = abs((ts-ti)/0.01)
    
    try:
        R = abs((Ti - Ts)/(ts - ti))
    except:
        R = abs((Ti - Ts)/(0.01))    
    
    if(num_pasos_carcasa > 1):
        a = 1.8008
        b = -0.3711
        c = -1.2487
        d = 0.0487
        e = 0.2458
        factor = a+b*R+c*P+d*pow(R,2)+e*pow(P,2)
    elif(num_pasos_tubo >= 2):
        a = 2.3221
        b = -1.3983
        c = -8.9291
        d = 1.4344
        e = 36.1973
        f = -0.7422
        g = -72.4922
        h =  0.1799
        i = 68.5452
        j = -0.0162
        k = -25.3014
        factor = a+b*R+c*P+d*pow(R,2)+e*pow(P,2)+f*pow(R,3)+g*pow(P,3)+h*pow(R,4)+i*pow(P,4)+j*pow(R,5)+k*pow(P,5)
    else:
        factor = 1

    return factor

def determinar_flujo(flujos: dict):
    return 1 if float(flujos['flujo_liquido_in']) != 0 else 2

def determinar_hvap_cdf_total(calor: float, flujo: float, cp_gas: float, cp_liquido: float, t1: float, t2: float, tsat: float):
    """
    Resumen:
        
    Parámetros:
        calor: float -> Calor de diseño (W)
        flujo: float -> Flujo Másico total (Kg/s)
        cp_gas: float -> Cp de gas (Kg/s)
        cp_liquido: float -> Cp de líquido (Kg/s)
        t1: float -> Temperatura 1 (K)
        t2: float -> Temperatura 2 (K)
        tsat: float -> Temperatura de Saturación (K)
    """
    # Determinar dirección del flujo gas -> liquido o liquido -> gas

    # Calcular segun el caso

    # Devolver Hvap calculado
    return calor/flujo - cp_gas*(tsat-t1) - cp_liquido*(t2-tsat)