from pint import UnitRegistry

ur = UnitRegistry()
Q_ = ur.Quantity

def normalizar_unidades_temperatura(args, unidad):
    actualizadas = []
    unidad = ur.degC if unidad == 1 else ur.degR if unidad == 8 else ur.degF
    for x in args:
        actualizadas.append(Q_(x, unidad).to(ur.kelvin).magnitude)

    return actualizadas if len(actualizadas) != 0 else args

def normalizar_unidades_flujo(args, unidad):
    actualizadas = []
    print(unidad)
    if unidad == 6:
        for x in args:
            actualizadas.append(Q_(x, ur.kilogram/ur.hour).to(ur.kilogram/ur.second).magnitude)
    elif unidad == 18:
        print("?")
        for x in args:
            actualizadas.append(Q_(x, ur.pound/ur.second).to(ur.kilogram/ur.second).magnitude)
    elif unidad == 19:
        print("??")
        for x in args:
            actualizadas.append(Q_(x, ur.pound/ur.hour).to(ur.kilogram/ur.second).magnitude)

    return actualizadas if len(actualizadas) != 0 else args

def normalizar_unidades_longitud(args, unidad):
    actualizadas = []

    if unidad != 4:
        if unidad == 5:
            for x in args:
                actualizadas.append(Q_(x, ur.millimeter).to(ur.meter).magnitude)
        elif unidad == 12:
            for x in args:
                actualizadas.append(Q_(x, ur.centimeter).to(ur.meter).magnitude)
        elif unidad == 14:
            for x in args:
                actualizadas.append(Q_(x, ur.feet).to(ur.meter).magnitude)
        elif unidad == 16:
            for x in args:
                actualizadas.append(Q_(x, ur.inch).to(ur.meter).magnitude)

    return actualizadas if len(actualizadas) != 0 else args

def normalizar_unidades_area(args, unidad):
    actualizadas = []

    if unidad != 3:
        if unidad == 20:
            for x in args:
                actualizadas.append(Q_(x, ur.feet ** 2).to(ur.meter ** 2).magnitude)
        elif unidad == 21:
            for x in args:
                actualizadas.append(Q_(x, ur.inch ** 2).to(ur.meter ** 2).magnitude)

    return actualizadas if len(actualizadas) != 0 else args

def normalizar_unidades_presion(args, unidad):
    actualizadas = []

    if unidad != 3:
        if unidad == 23:
            for x in args:
                actualizadas.append(Q_(x, ur.atm).to(ur.bar).magnitude)
        elif unidad == 17:
            for x in args:
                actualizadas.append(Q_(x, ur.pound_force_per_square_inch).to(ur.bar).magnitude)
        elif unidad == 22:
            for x in args:
                actualizadas.append(Q_(x, ur.mmHg).to(ur.bar).magnitude)
        elif unidad == 26:
            for x in args:
                actualizadas.append(Q_(x, ur.kPa).to(ur.bar).magnitude)

    return actualizadas if len(actualizadas) != 0 else args

def normalizar_unidades_entropia_especifica(args, unidad):
    actualizadas = []

    if unidad != 3:
        if unidad == 23:
            for x in args:
                actualizadas.append(Q_(x, ur.Btu_it/ur.pound/ur.delta_degF).to(ur.joule/ur.kilogram/ur.kelvin).magnitude)

    return actualizadas if len(actualizadas) != 0 else args

def normalizar_unidades_calor(args, unidad):
    actualizadas = []

    if unidad != 3:
        if unidad == 24:
            for x in args:
                actualizadas.append(Q_(x, ur.Btu_it/ur.hour).to(ur.watt).magnitude)
        elif unidad == 25:
            for x in args:
                actualizadas.append(Q_(x, ur.Btu_it/ur.second).to(ur.watt).magnitude)

    return actualizadas if len(actualizadas) != 0 else args