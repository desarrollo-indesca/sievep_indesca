import threading, time 
from schedule import Scheduler
from django.db import transaction
from django.db.models import Prefetch

def run_continuously(self, interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):

        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run

Scheduler.run_continuously = run_continuously

def delete_ventilador_copies():
    from auxiliares.models import Ventilador, EvaluacionVentilador
    copias = Ventilador.objects.filter(copia=True).select_related(
        'condiciones_trabajo', 'condiciones_adicionales', 
        'condiciones_generales', 'especificaciones'
    ).prefetch_related(Prefetch('evaluaciones_ventilador', EvaluacionVentilador.objects.select_related(
        'entrada', 'salida'
    )))

    for copia in copias:
        condiciones_trabajo = copia.condiciones_trabajo
        condiciones_adicionales = copia.condiciones_adicionales
        condiciones_generales = copia.condiciones_generales
        especificaciones = copia.especificaciones

        for evaluacion in copia.evaluaciones_ventilador.all():
            evaluacion.delete()
            evaluacion.entrada.delete()
            evaluacion.salida.delete()

        copia.delete()
        condiciones_trabajo.delete()
        
        if(condiciones_adicionales):
            condiciones_adicionales.delete()
        
        condiciones_generales.delete()
        especificaciones.delete()

def delete_bombas_copies():
    from auxiliares.models import Bombas, EvaluacionBomba, SalidaSeccionesEvaluacionBomba

    copias = Bombas.objects.filter(copia=True).select_related(
        'especificaciones_bomba', 'detalles_motor', 'detalles_construccion', 
        'condiciones_diseno', 'instalacion_succion', 'instalacion_descarga'
    ).prefetch_related(
        'instalacion_succion__tuberias', 'instalacion_descarga__tuberias',
        Prefetch('evaluaciones_bomba', EvaluacionBomba.objects.select_related(
            'entrada', 'salida'
        ).prefetch_related(
            Prefetch('salida_secciones_evaluacionbomba', 
                     queryset=SalidaSeccionesEvaluacionBomba.objects.prefetch_related('datos_tramos_seccion')))
    ))

    for copia in copias:
        especificaciones_bomba = copia.especificaciones_bomba
        detalles_motor = copia.detalles_motor
        detalles_construccion = copia.detalles_construccion
        condiciones_diseno = copia.condiciones_diseno
        instalacion_succion = copia.instalacion_succion
        instalacion_descarga = copia.instalacion_descarga

        for tuberia in instalacion_succion.tuberias.all():
            tuberia.delete()

        for tuberia in instalacion_descarga.tuberias.all():
            tuberia.delete()

        for evaluacion in copia.evaluaciones_bomba.all():
            for x in evaluacion.salida_secciones_evaluacionbomba.all():
                x.datos_tramos_seccion.all().delete()
            
            evaluacion.salida_secciones_evaluacionbomba.all().delete()            
            evaluacion.delete()
            evaluacion.salida.delete()
            evaluacion.entrada.delete()

        copia.delete()
        especificaciones_bomba.delete()
        detalles_motor.delete()
        detalles_construccion.delete()
        condiciones_diseno.delete()
        instalacion_succion.delete()
        instalacion_descarga.delete()

def delete_precalentador_copies():
    from auxiliares.models import PrecalentadorAgua

    copias = PrecalentadorAgua.objects.filter(copia=True).select_related('datos_corrientes').prefetch_related(
        'secciones_precalentador', 'especificaciones_precalentador'
    )

    for copia in copias:        
        for evaluacion in copia.evaluacion_precalentador.all():
            salida = evaluacion.salida_general
            evaluacion.corrientes_evaluacion_precalentador_agua.all().delete()
            salida.delete()

        copia.datos_corrientes.corrientes_evaluacion_precalentador_agua.all().delete()
        datos_corrientes = copia.datos_corrientes
        copia.secciones_precalentador.all().delete()
        copia.especificaciones_precalentador.all().delete()
        copia.delete()
        datos_corrientes.delete()

def delete_turbinas_vapor_copies():
    from turbinas.models import TurbinaVapor, Evaluacion, CorrienteEvaluacion

    copias = TurbinaVapor.objects.filter(copia=True).select_related('especificaciones', 'generador_electrico', 'datos_corrientes').prefetch_related(
        Prefetch('evaluaciones_turbinasvapor', Evaluacion.objects.select_related(
            'entrada', 'salida'
        ).prefetch_related(
            Prefetch('corrientes_evaluacion', CorrienteEvaluacion.objects.select_related('entrada', 'salida'))
        ))
    )

    for copia in copias:
        for evaluacion in copia.evaluaciones_turbinasvapor.all():
            corrientes_evaluacion = evaluacion.corrientes_evaluacion

            for corriente in corrientes_evaluacion.all():
                corriente.delete()  
                corriente.entrada.delete()
                corriente.salida.delete()

            evaluacion.delete()
            evaluacion.entrada.delete()
            evaluacion.salida.delete()    

        especificaciones = copia.especificaciones
        generador_electrico = copia.generador_electrico
        datos_corrientes = copia.datos_corrientes

        copia.delete()

        for corriente in datos_corrientes.corrientes.all():
            corriente.delete()
        
        datos_corrientes.delete()
        especificaciones.delete()
        generador_electrico.delete()

def delete_intercambiador_copies():
    from intercambiadores.models import Intercambiador

    copias = Intercambiador.objects.filter(copia=True).select_related(
        'tipo'
    ).prefetch_related(
        'evaluaciones', 'datos_dobletubo', 
        'condiciones', 'datos_tubo_carcasa'
    )

    for copia in copias:
        print(copia.tipo.nombre)
        print(copia.tag)
        propiedades = copia.datos_tubo_carcasa if copia.tipo.nombre == "TUBO/CARCASA" else copia.datos_dobletubo
        condiciones = copia.condiciones
        evaluaciones = copia.evaluaciones

        propiedades.delete()
        condiciones.all().delete()
        evaluaciones.all().delete()
        copia.delete()

def delete_calderas_copies():
    from calderas.models import Caldera, Evaluacion

    copias = Caldera.objects.filter(copia=True).select_related(
            "sobrecalentador", "sobrecalentador__dims", "tambor",
            "dimensiones", "especificaciones", "combustible", 
            "chimenea", "economizador"
    ).prefetch_related(
        "tambor__secciones_tambor", "combustible__composicion_combustible_caldera",
        "caracteristicas_caldera", "corrientes_caldera",
        Prefetch("equipo_evaluacion_caldera", Evaluacion.objects.select_related(
                "salida_flujos", "salida_fracciones", "salida_balance_energia",
                "salida_lado_agua"
            ).prefetch_related(
                "entradas_fluidos_caldera", "composiciones_evaluacion"
            )
        )
    )

    for copia in copias:
        sobrecalentador = copia.sobrecalentador
        dims_sobrecalentador = sobrecalentador.dims
        tambor = copia.tambor
        dimensiones = copia.dimensiones
        especificaciones = copia.especificaciones
        combustible = copia.combustible
        chimenea = copia.chimenea
        economizador = copia.economizador
        evaluaciones = copia.equipo_evaluacion_caldera

        copia.caracteristicas_caldera.all().delete()
        copia.corrientes_caldera.all().delete()

        for evaluacion in evaluaciones.all():
            evaluacion.entradas_fluidos_caldera.all().delete()
            evaluacion.composiciones_evaluacion.all().delete()
            evaluacion.delete()
            evaluacion.salida_flujos.delete()
            evaluacion.salida_fracciones.delete()
            evaluacion.salida_balance_energia.delete()
            evaluacion.salida_lado_agua.delete()
        
        tambor.secciones_tambor.all().delete()
        combustible.composicion_combustible_caldera.all().delete()
        copia.delete()
        combustible.delete()
        tambor.delete()
        sobrecalentador.delete()
        dims_sobrecalentador.delete()
        dimensiones.delete()
        especificaciones.delete()
        chimenea.delete()
        economizador.delete()

def delete_copies():
    with transaction.atomic():
        delete_ventilador_copies()
        delete_bombas_copies()
        delete_precalentador_copies()
        delete_turbinas_vapor_copies()
        delete_intercambiador_copies()
        delete_calderas_copies()

def start_deleting_job():
    scheduler = Scheduler()
    scheduler.every(10).seconds.do(delete_copies)
    scheduler.run_continuously()
