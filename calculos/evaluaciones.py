from .termodinamicos import calcular_cp
import numpy as np

def evaluacion_tubo_carcasa(intercambiador, ti, ts, Ti, Ts, ft, Fc, nt, cp_tubo = None, cp_carcasa = None):
    
    if cp_tubo == None:
        cp_tubo = calcular_cp(intercambiador.fluido_tubo.cas, float(ti), float(ts)) if intercambiador.fluido_tubo else float(intercambiador.condicion_tubo().fluido_cp)
    else:
        cp_tubo = cp_tubo

    if cp_carcasa == None:
        cp_carcasa = calcular_cp(intercambiador.fluido_carcasa.cas, float(Ti), float(Ts)) if intercambiador.fluido_carcasa else float(intercambiador.condicion_carcasa().fluido_cp)
    else:
        cp_carcasa = cp_carcasa

    q_tubo = cp_tubo*ft*abs(ti-ts)
    q_carcasa = cp_carcasa*Fc*abs(Ti-Ts)
    nt = nt if nt else float(intercambiador.numero_tubos)

    diametro_tubo = float(intercambiador.diametro_interno_tubos)
    longitud_tubo = float(intercambiador.longitud_tubos)

    area_calculada = np.pi*diametro_tubo*nt*longitud_tubo

    try:
        dtml = abs(((Ti - ti) - (Ts - ts))/np.log(abs((Ti - ti)/(Ts - ts))))
    except:
        dtml = abs(((Ti - ti) - (Ts - ts + 1e-5))/np.log(abs((Ti - ti)/(Ts - ts + 1e-5))))

    P = abs((ts - ti)/(Ti - ti))
    R = abs((Ti - Ts)/(ts - ti))

    num_pasos_carcasa = float(intercambiador.numero_pasos_carcasa)
    num_pasos_tubo = float(intercambiador.numero_pasos_tubo)

    if(num_pasos_tubo > 1):
        a = 1.8008
        b = -0.3711
        c = -1.2487
        d = 0.0487
        e = 0.2458
        factor = a+b*R+c*P+d*pow(R,2)+e*pow(P,2)
    elif(num_pasos_carcasa >= 2):
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

    print(intercambiador.u)

    q_prom = np.mean([q_tubo,q_carcasa])
    ucalc = q_prom/(area_calculada*dtml*factor)
    RF=1/ucalc-1/float(intercambiador.u)
    
    ct = ft*cp_tubo
    cc = Fc*cp_carcasa

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
        'cp_tubo': round(cp_tubo,4),
        'cp_carcasa': round(cp_carcasa,4),
        'factor_ensuciamiento': round(RF,4),
    }

    print(resultados)

    return resultados