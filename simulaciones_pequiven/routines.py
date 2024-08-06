
def delete_ventilador_copies():
    from auxiliares.models import Ventilador
    copias = Ventilador.objects.filter(copia=True)

    for copia in copias:
        copia.delete()

def delete_copies():
    delete_ventilador_copies()
