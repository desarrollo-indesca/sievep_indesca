from pint import UnitRegistry

ur = UnitRegistry()
Q_ = ur.Quantity

def normalizar_unidades_temperatura(args, unidad):
    actualizadas = []
    unidad = ur.degC if unidad == 1 else ur.degR if unidad == 8 else ur.degF
    for x in args:
        actualizadas.append(Q_(x, unidad).to(ur.kelvin).magnitude)

    return actualizadas

def normalizar_unidades_flujo(args, unidad):
    actualizadas = []
    unidad = ur.kilogram/ur.hour

    if unidad != 6:
        for x in args:
            actualizadas.append(Q_(x, unidad).to(ur.kilogram/ur.second).magnitude)

    print(actualizadas)

    return actualizadas

print(normalizar_unidades_flujo([2.5, 2], 10))