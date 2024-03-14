def conseguir_largo(tupla : tuple, valor : str) -> str:
    '''
    Resumen:
        Función para conseguir los valores de las opciones en tuplas como se ve en algunos modelos.
    
    Parámetros:
        tupla : tuple -> Tupla con valores de la forma: (('A','B'),('C','D'))
        valor: str -> Llave a conseguir en los valores.

    Devuelve:
        str: Valor encontrado, o None si no se encuentra

    Ejemplo:
        conseguir_largo((('A','B'),('C','D')), 'A') -> 'B'
    '''
    for x in tupla:
        if(x[0] == valor):
            return x[1]
    
    return None