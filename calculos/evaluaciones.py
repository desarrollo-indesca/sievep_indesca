import numpy as np
from .unidades import transformar_unidades_temperatura, transformar_unidades_area, transformar_unidades_flujo, transformar_unidades_longitud, transformar_unidades_presion, transformar_unidades_cp, transformar_unidades_u
from ht import F_LMTD_Fakheri
from .termodinamicos import calcular_tsat_hvap

def evaluacion_tubo_carcasa(intercambiador, ti, ts, Ti, Ts, ft, Fc, nt, cp_gas_tubo = None, cp_liquido_tubo = None, cp_gas_carcasa = None, cp_liquido_carcasa = None, unidad_temp = 1, unidad_flujo = 6) -> dict:
    '''
    Resumen:
        Función para evaluar un intercambiador de calor de tubo y carcasa.

    Parámetros:
        intercambiador: Intercambiador -> Intercambiador a evaluar.
        ti: float -> Temperatura de entrada del fluido en los tubos.
        ts: float -> Temperatura de salida del fluido en los tubos.
        Ti: float -> Temperatura de entrada del fluido en la carcasa.
        Ts: float -> Temperatura de salida del fluido en la carcasa.
        ft: float -> Flujo másico del fluido en los tubos.
        Fc: float -> Flujo másico del fluido en la carcasa.
        nt: float -> Número de tubos.
        cp_gas_tubo: float -> Cp del gas en los tubos (J/KgK).
        cp_liquido_tubo: float -> Cp del líquido en los tubos (J/KgK).
        cp_gas_carcasa: float -> Cp del gas en la carcasa (J/KgK).
        cp_liquido_carcasa: float -> Cp del líquido en la carcasa (J/KgK).
        unidad_temp: int -> Unidad de temperatura de entrada. De no dar ninguna, se asume en K.
        unidad_flujo: int -> Unidad de flujo másico. De no dar ninguna, se asume en Kg/s.

    Devuelve:
        dict -> Diccionario con los resultados de la evaluación (calor intercambiado, área de transferencia, lmtd, eficiencia, efectividad, ntu, u, ua, factor_ensuciamiento).
    '''

    ti,ts,Ti,Ts = transformar_unidades_temperatura([ti,ts,Ti,Ts], unidad=unidad_temp) # ti,ts = temperatura de los tubos, Ti,Ts = temperaturas de la carcasa
    
    if(unidad_flujo != 10): # Transformación de los flujos ft (flujo tubo) y Fc (flujo carcasa) a Kg/s para calcular
        ft,Fc = transformar_unidades_flujo([ft,Fc], unidad_flujo)

    q_tubo = calcular_calor(ft, ti, ts, cp_gas_tubo, cp_liquido_tubo, intercambiador, 'T') # Calor del tubo (W)
    q_carcasa = calcular_calor(Fc, Ti, Ts, cp_gas_carcasa, cp_liquido_carcasa, intercambiador, 'C') # Calor de la carcasa (W)

    print(q_carcasa, q_tubo)
    
    nt = nt if nt else float(intercambiador.numero_tubos) # Número de los tubos

    # diametro_tubo = transformar_unidades_longitud([float(intercambiador.diametro_externo_tubos)], intercambiador.diametro_tubos_unidad.pk)[0] # Diametro (OD), transformacion a m
    # longitud_tubo = transformar_unidades_longitud([float(intercambiador.longitud_tubos)], intercambiador.longitud_tubos_unidad.pk)[0] # Longitud, transformacion a m

    # area_calculada = np.pi*diametro_tubo*nt*longitud_tubo #m2

    area_calculada = transformar_unidades_area([float(intercambiador.area/intercambiador.numero_tubos)*nt], intercambiador.area_unidad.pk)[0] #m2

    num_pasos_carcasa = float(intercambiador.numero_pasos_carcasa)
    num_pasos_tubo = float(intercambiador.numero_pasos_tubo)
    dtml = abs(((Ti - ts) - (Ts - ti))/np.log(abs((Ti - ts)/(Ts - ti)))) # Delta T Medio Logarítmico

    factor = round(F_LMTD_Fakheri(Ti, Ts, ti, ts, num_pasos_carcasa),3)  # Factor de corrección
    
    print(f"FACTOR: {factor}")
    q_prom = np.mean([q_tubo,q_carcasa]) # Promedio del calor (W)
    ucalc = q_prom/(area_calculada*dtml*factor) # U calculada (Wm2/K)
    udiseno = transformar_unidades_u([float(intercambiador.u)], intercambiador.u_unidad.pk)[0] # transformación de la U de diseño
    RF = 1/ucalc - 1/udiseno # Factor de Ensuciamiento respecto a la U de diseño (K/Wm2)

    condicion_tubo = intercambiador.condicion_tubo()
    condicion_carcasa = intercambiador.condicion_carcasa()

    ct = obtener_c_eficiencia(condicion_tubo, ft, cp_gas_tubo, cp_liquido_tubo) # Obtención de la C de tubo
    cc = obtener_c_eficiencia(condicion_carcasa, Fc, cp_gas_carcasa, cp_liquido_carcasa) # Obtención de la C de carcasa

    # Determinación de la Cmín y la Cmáx
    if(ct < cc):
        cmin = ct
        cmax = cc
        minimo = 1
    else:
        cmin = cc
        cmax = ct
        minimo = 2

    if(condicion_carcasa.cambio_de_fase in ['T','P'] or condicion_tubo.cambio_de_fase in ['T','P']):
        cmax = np.Infinity
    
    # Relación de las C
    c = cmin/cmax
    ntu = ucalc*area_calculada/cmin

    if(c == 0): # Cálculo de la Efectividad y la NTU si C = 0
        efectividad = 1 - np.exp(-1*ntu)
    else: # Cálculo si C es distinto de  0
        if(num_pasos_tubo > 2): # Fórmulas cuando el número de pasos de tubo es mayor a 2
            efectividad1 = 2/(1+c+pow(1+pow(c,2),0.5)*(1+np.exp(-1*ntu*pow((1-pow(c,2)),0.5)))/(1-np.exp(-1*ntu*pow((1-pow(c,2)),0.5))))
            efectividad = efectividad1
        else: # Fórmulas cuando no
            if(minimo == 1):
                efectividad=1/c*(1-np.exp(-1*c*(1-1*np.exp(-1*ntu))))
            else:
                efectividad=1-np.exp(-1/c*np.exp(1-np.exp(-1*ntu*c)))

        if(num_pasos_carcasa > 1): # Cuando el número de carcasa es mayor a 1
            if(c == 1):
                efectividad=num_pasos_carcasa*efectividad1/(1+(num_pasos_carcasa-1)*efectividad1)
            else:
                efectividad=(pow((1-efectividad1*c)/(1-efectividad1),num_pasos_carcasa)-1)/(pow((1-efectividad1*c)/(1-efectividad1),num_pasos_carcasa)-c)

    eficiencia = efectividad/ntu # Cálculo de la Eficiencia

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

def evaluacion_doble_tubo(intercambiador, ti, ts, Ti, Ts, ft, Fc, nt, cp_gas_in = None, cp_liquido_in = None, cp_gas_ex = None, cp_liquido_ex = None, unidad_temp = 1, unidad_flujo = 6) -> dict:   
    ti,ts,Ti,Ts = transformar_unidades_temperatura([ti,ts,Ti,Ts], unidad=unidad_temp) # ti,ts = temperatura de los tubos, Ti,Ts = temperaturas de la carcasa
    
    if(unidad_flujo != 10): # Transformación de los flujos ft (flujo tubo) y Fc (flujo carcasa) a Kg/s para calcular
        ft,Fc = transformar_unidades_flujo([ft,Fc], unidad_flujo)

    q_ex = calcular_calor(ft, ti, ts, cp_gas_ex, cp_liquido_ex, intercambiador, 'T') # Calor del tubo (W)
    q_in = calcular_calor(Fc, Ti, Ts, cp_gas_in, cp_liquido_in, intercambiador, 'C') # Calor de la carcasa (W)
    
    nt = nt if nt else float(intercambiador.numero_tubos) # Número de los tubos

    diametro_tubo = transformar_unidades_longitud([float(intercambiador.diametro_externo_tubos)], intercambiador.diametro_tubos_unidad.pk)[0] # Diametro (OD), transformacion a m
    longitud_tubo = transformar_unidades_longitud([float(intercambiador.longitud_tubos)], intercambiador.longitud_tubos_unidad.pk)[0] # Longitud, transformacion a m

    area_calculada = np.pi*diametro_tubo*nt*longitud_tubo #m2

    arreglo_flujo = intercambiador.arreglo_flujo

    if(arreglo_flujo == 'c'): # Si el arreglo de flujo es en contracorriente
        dtml = abs(((Ti - ts) - (Ts - ti))/np.log(abs((Ti - ts)/(Ts - ti)))) # Delta T Medio Logarítmico
    if(arreglo_flujo == 'C'): # Si el arreglo de flujo es en cocorriente
        dtml = ((Ti - ti) - (Ts - ts))/np.log(abs((Ti - ti)/(Ts - ts))) # Delta T Medio Logarítmico
   
    q_prom = np.mean([q_in,q_ex]) # Promedio del calor (W)
    ucalc = q_prom/(area_calculada*dtml) # U calculada (Wm2/K)
    udiseno = transformar_unidades_u([float(intercambiador.u)], intercambiador.u_unidad.pk)[0] # transformación de la U de diseño
    RF = 1/ucalc - 1/udiseno # Factor de Ensuciamiento respecto a la U de diseño (K/Wm2)

    condicion_tubo = intercambiador.condicion_tubo()
    condicion_carcasa = intercambiador.condicion_carcasa()

    ct = obtener_c_eficiencia(condicion_tubo, ft, cp_gas_in, cp_liquido_in) # Obtención de la C de tubo
    cc = obtener_c_eficiencia(condicion_carcasa, Fc, cp_gas_ex, cp_liquido_ex) # Obtención de la C de carcasa

    # Determinación de la Cmín y la Cmáx
    if(ct < cc):
        cmin = ct
        cmax = cc
        minimo = 1
    else:
        cmin = cc
        cmax = ct
        minimo = 2

    if(condicion_carcasa.cambio_de_fase in ['T','P'] or condicion_tubo.cambio_de_fase in ['T','P']):
        cmax = np.Infinity

    # Relación de las C
    c = cmin/cmax
    ntu = ucalc*area_calculada/cmin

    if(c == 0): # Cálculo de la Efectividad y la NTU si C = 0
        efectividad = 1 - np.exp(-1*ntu)
    else: # Cálculo si C es distinto de  0
        if(c == 1):
            eficiencia=ntu/(ntu+1)
        else:
            if(arreglo_flujo == 'C'): # Si el arreglo de flujo es en cocorriente
                eficiencia=(1-np.exp(-1*ntu*(1+c)))/(1+c)
            elif(arreglo_flujo == 'c'): # Si el arreglo de flujo es en contracorriente
                if(c != 1):
                    eficiencia=(1-np.exp(-1*ntu*(1-c)))/(1-c*np.exp(-1*ntu*(1-c)))
                else:
                    eficiencia=ntu/(ntu+1)

    eficiencia = efectividad/ntu # Cálculo de la Eficiencia

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
        cp: float -> Cp del fluido (J/KgK)
        lado: str -> T si es el calor del lado del tubo, C si es el calor de la carcasa.

    Devuelve:
        float -> Q (W) del lado del intercambiador
    """

    fluido = intercambiador.fluido_tubo if lado == 'T' else intercambiador.fluido_carcasa
    datos = intercambiador.condicion_tubo() if lado == 'T' else intercambiador.condicion_carcasa()
    presion = transformar_unidades_presion([float(datos.presion_entrada)], datos.unidad_presion.pk)[0]

    if(fluido == None):
        fluido = datos.fluido_etiqueta if lado == 'T' else datos.fluido_etiqueta

    if(datos.cambio_de_fase == 'S'): # Caso 1: Sin Cambio de Fase
        return calcular_calor_scdf(flujo,cp_liquido,t1,t2) if cp_liquido else calcular_calor_scdf(flujo,cp_gas,t1,t2)
    elif(datos.cambio_de_fase == 'P'): # Caso 2: Cambio de Fase Parcial
        flujo_vapor_in = float(datos.flujo_vapor_entrada)
        flujo_vapor_out = float(datos.flujo_vapor_salida)
        flujo_liquido_in = float(datos.flujo_liquido_entrada)
        flujo_liquido_out = float(datos.flujo_liquido_salida)
        [flujo_vapor_in,flujo_vapor_out,flujo_liquido_in,flujo_liquido_out] = transformar_unidades_flujo([flujo_vapor_in, flujo_vapor_out, flujo_liquido_in, flujo_liquido_out], datos.flujos_unidad.pk)

        caso = determinar_cambio_parcial(flujo_vapor_in, flujo_vapor_out, flujo_liquido_in, flujo_liquido_out)

        if(type(fluido) != str):
            if(caso[1] == 'D'):
                print(t2)
                _,hvap = calcular_tsat_hvap(fluido.cas, presion, t2)
            else:
                print(t1)
                _,hvap = calcular_tsat_hvap(fluido.cas, presion, t1)
        else:
            hvap = float(datos.hvap) if datos.hvap else 5000

        return calcular_calor_cdfp(flujo_vapor_in,flujo_vapor_out,flujo_liquido_in,flujo_liquido_out,flujo,t1,t2,hvap,cp_gas,cp_liquido)
    else: # Caso 3: Cambio de Fase Total
        return calcular_calor_cdft(flujo,t1,t2,fluido,presion,datos,cp_gas,cp_liquido)

def calcular_calor_scdf(flujo, cp, t1, t2) -> float:
    '''
    Resumen:
        Función para calcular el calor de un fluido sin cambio de fase.

    Parámetros:
        flujo: float -> Flujo másico (Kg/s)
        cp: float -> Cp del fluido (J/KgK)

    Devuelve:
        float -> Q (W) del lado del intercambiador
    '''
    return flujo * cp * abs(t2-t1)

def calcular_calor_cdfp(flujo_vapor_in,flujo_vapor_out,flujo_liquido_in,flujo_liquido_out,flujo,t1,t2,hvap,cp_gas,cp_liquido) -> float:
        '''
        Resumen:
            Función para calcular el calor de un fluido con cambio de fase parcial.

        Parámetros:
            flujo_vapor_in: float -> Flujo de vapor de entrada (Kg/s)
            flujo_vapor_out: float -> Flujo de vapor de salida (Kg/s)
            flujo_liquido_in: float -> Flujo de líquido de entrada (Kg/s)
            flujo_liquido_out: float -> Flujo de líquido de salida (Kg/s)
            flujo: float -> Flujo másico (Kg/s)
            t1: float -> Temperatura de Entrada (K)
            t2: float -> Temperatura de Salida (K)
            hvap: float -> Calor latente de vaporización (J/Kg)
            cp_gas: float -> Cp del gas (J/KgK)
            cp_liquido: float -> Cp del líquido (J/KgK)

        Devuelve:
            float -> Q (W) del lado del intercambiador
        '''
        cdf = determinar_cambio_parcial(flujo_vapor_in, flujo_vapor_out, flujo_liquido_in, flujo_liquido_out)
        calidad = abs(flujo_vapor_out-flujo_vapor_in)/(flujo_liquido_in+flujo_vapor_in)

        if(cdf == 'DD'):
            return hvap*calidad*flujo
        elif(cdf == 'DL'):
            return abs(flujo*(-hvap*calidad + (t2-t1)*cp_liquido))
        elif(cdf == 'DV'):
            return flujo*(hvap*calidad + (t2-t1)*cp_gas)
        elif(cdf == 'LD'):
            return flujo*((t2-t1)*cp_liquido + hvap*calidad)
        elif(cdf == 'VD'):
            print(flujo, t2, t1, cp_gas, calidad, hvap, calidad)
            return abs(flujo*((t2-t1)*cp_gas - hvap*calidad))

def  calcular_calor_cdft(flujo,t1,t2,fluido,presion,datos,cp_gas,cp_liquido) -> float:
    '''
    Resumen:
        Función para calcular el calor de un fluido con cambio de fase total.

    Parámetros:
        flujo: float -> Flujo másico (Kg/s)
        t1: float -> Temperatura de Entrada (K)
        t2: float -> Temperatura de Salida (K)
        fluido: str -> Etiqueta del fluido
        presion: float -> Presión de entrada (Pa)
        datos: Condicion -> Condición del fluido
        cp_gas: float -> Cp del gas (J/KgK)
        cp_liquido: float -> Cp del líquido (J/KgK)

    Devuelve:
        float -> Q (W) del lado del intercambiador
    '''
    if(type(fluido) != str):
        tsat,hvap = calcular_tsat_hvap(fluido.cas, presion)
    else:
        tsat = transformar_unidades_temperatura([float(datos.tsat)], datos.temperaturas_unidad.pk)[0]
        hvap = float(datos.hvap) if datos.hvap else datos

    try:
        fluido_cp_gas, fluido_cp_liquido = transformar_unidades_cp([cp_gas,cp_liquido], datos.unidad_cp.pk, 29)
    except:
        fluido_cp_gas, fluido_cp_liquido = cp_gas, cp_liquido

    if(t1 <= t2): # Vaporización
        return flujo*(fluido_cp_gas*(t2-tsat)+hvap+fluido_cp_liquido*(tsat-t1))
    else: # Condensación
        return abs(flujo*(fluido_cp_gas*(tsat-t1)-hvap+fluido_cp_liquido*(t2-tsat)))

def obtener_c_eficiencia(condicion, flujo: float, cp_gas: float, cp_liquido: float) -> float:
    '''
    Resumen:
        Función para obtener la C de un lado de un intercambiador para el posterior cálculo de la eficiencia.

    Parámetros:
        condicion: Condicion -> Condición del fluido
        flujo: float -> Flujo másico (Kg/s)
        cp_gas: float -> Cp del gas (J/KgK)
        cp_liquido: float -> Cp del líquido (J/KgK)

    Devuelve:
        float -> C de eficiencia del fluido.
    '''
    if(condicion.cambio_de_fase == 'S'): # Caso 1: Sin Cambio de Fase
        c = flujo*cp_gas if cp_gas else flujo*cp_liquido # Se usa el Cp correspondiente
    elif(condicion.cambio_de_fase == 'T'): # Caso 2: Cambio de Fase Total
        if(condicion.flujo_vapor_salida != 0): # Se usa el Cp correspondiente de la salida del fluido
            c = flujo*cp_gas
        else:
            c = flujo*cp_liquido
    else: # Caso 3: Cambio de Fase Parcial
        if(float(condicion.flujo_vapor_salida) == flujo): # Si sale líquido o vapor, se usa el cp correspondiente
            c = flujo * cp_gas
        elif(float(condicion.flujo_liquido_salida) == flujo):
            c = flujo * cp_liquido
        else:
            if(condicion.hvap):
                c = condicion.flujo_vapor_salida/(condicion.flujo_vapor_salida+condicion.flujo_vapor_entrada)*condicion.hvap
            else:
                presion = transformar_unidades_presion([float(condicion.presion_entrada)], condicion.unidad_presion.pk)[0]

                if(condicion.lado == 'C' and condicion.intercambiador.fluido_carcasa or 
                        condicion.lado == 'T' and condicion.intercambiador.fluido_tubo):
                    cas = condicion.intercambiador.fluido_carcasa.cas if condicion.lado == 'C' else condicion.intercambiador.fluido_tubo.cas
                    _,hvap = calcular_tsat_hvap(cas, presion)
                else:
                    hvap = float(condicion.hvap) if condicion.hvap else 5000

                calidad = float(condicion.flujo_vapor_salida/(condicion.flujo_vapor_salida+condicion.flujo_liquido_salida))
                c = calidad*hvap
    return float(c)

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

def determinar_cambio_parcial(flujo_vapor_in: float, flujo_vapor_out: float, flujo_liquido_in: float, flujo_liquido_out: float) -> str:
    '''
    Resumen:
        Función que determina el tipo de cambio de fase parcial.

    Parámetros:
        flujo_vapor_in: float -> Flujo de vapor de entrada.
        flujo_vapor_out float -> Flujo de vapor de salida.
        flujo_liquido_in: float -> Flujo de líquido de entrada.
        flujo_liquido_out: float -> Flujo de líquido de salida.

    Devuelve:
        str -> Letra indicando el cambio de fase parcial. DD si es domo a domo. DL si es domo a líquido. DV si es domo a vapor. LD si es líquido a domo. VD si es vapor a domo.
    '''
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