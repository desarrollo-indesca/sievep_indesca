
def evaluacion_bomba(bomba, temp_operacion, presion_succion, presion_descarga, 
                     altura_succion, altura_descarga, diametro_interno_succion,
                     diametro_interno_descarga, flujo, potencia, npshr):
    
    densidad, viscosidad, presion_vapor, cabezal_vapor = calcular_propiedades_termodinamicas_bomba()

    area_succion, area_descarga = calcular_area_bomba()
    velocidad_succion, velocidad_descarga = calcular_velocidad()

    nr_succion, nr_descarga = calcular_numero_reynolds()

    tipo_flujo_succion, factor_friccion_succion, factor_turbulento_succion = calcular_flujo_bomba()

    h_succion = perdida_tramos()
    h_descarga = perdida_tramos()

    h_total = h_succion + h_descarga

    cabezal = calcular_cabezal()
    potencia_calculada = calcular_potencia()
    eficiencia = calcular_eficiencia()
    ns = calcular_velocidad_especifica()
    npsha = calcular_npsha()
    cavita = calcular_cavita()
    
    res = {

    }

    return res
