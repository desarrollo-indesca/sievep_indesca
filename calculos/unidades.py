from pint import UnitRegistry

ur = UnitRegistry()
Q_ = ur.Quantity

def normalizar_unidades_temperatura(args, unidad):
    regresar = []
    unidad = ur.degC if unidad == 1 else ur.degR if unidad == 8 else ur.degF
    for x in args:
        regresar.append(Q_(x, unidad).to(ur.kelvin).magnitude)

    return regresar