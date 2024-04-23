function anadir_listeners_dropboxes() {    
    $('#id_presion_unidad').change((e) => {
        const array = $('select[name="presion_unidad"]').toArray().slice(1);
    
        array.map((x) => {
            x.innerHTML = "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
        });
    });

    $('#id_adicional-presion_unidad').change((e) => {
        const array = $('select[name="adicional-presion_unidad"]').toArray().slice(1);
    
        array.map((x) => {
            x.innerHTML = "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
        });
    });

    $('#id_espesor_unidad').change((e) => {
        const array = $('select[name="espesor_unidad"]').toArray().slice(1);
    
        array.map((x) => {
            x.innerHTML = "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
        });
    });

    $('#id_potencia_freno_unidad').change((e) => {
        const array = $('select[name="potencia_freno_unidad"]').toArray().slice(1);
    
        array.map((x) => {
            x.innerHTML = "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
        });
    });

    $('#id_adicional-potencia_freno_unidad').change((e) => {
        const array = $('select[name="adicional-potencia_freno_unidad"]').toArray().slice(1);
    
        array.map((x) => {
            x.innerHTML = "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
        });
    });

    $('#id_temp_ambiente_unidad').change((e) => {
        const array = $('select[name="temp_ambiente_unidad"]').toArray().slice(1);
    
        array.map((x) => {
            x.innerHTML = "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
        });
    });

    $('#id_presion_barometrica_unidad').change((e) => {
        const array = $('select[name="presion_barometrica_unidad"]').toArray().slice(1);
    
        array.map((x) => {
            x.innerHTML = "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
        });
    });

    $('#id_calculo_densidad').change((e) => {
        if(e.target.value === 'M')
            $('#id_densidad').removeAttr('disabled');
        else
            $('#id_densidad').attr('disabled', 'disabled');
    });

    $('#id_adicional-calculo_densidad').change((e) => {
        if(e.target.value === 'M')
            $('#id_adicional-densidad').removeAttr('disabled');
        else
            $('#id_adicional-densidad').attr('disabled', 'disabled');
    });
}

const anadir_listeners_htmx = () => {
    document.body.addEventListener('htmx:beforeRequest', function(evt) {
        const body = document.getElementsByTagName('body')[0]
        body.style.opacity = 0.25;

        if(document.getElementById('id_calculo_propiedades').value === 'M' || 
            document.getElementById('id_temperatura_presion_vapor').value === '' ||
            document.getElementById('id_fluido').value === '' ||
            isNaN(Number(document.getElementById('id_fluido').value)) ||
            document.getElementById('id_temperatura_operacion').value === '' ||
            document.getElementById('id_presion_succion').value === ''
        ){
            evt.preventDefault();
            if(document.getElementById('id_calculo_propiedades').value === 'M'){
                $('#id_viscosidad').removeAttr('disabled');
                $('#id_presion_vapor').removeAttr('disabled');
                $('#id_densidad').removeAttr('disabled');
                $('#aviso').html('');
            }            
            body.style.opacity = 1.0;
        }  else
            $('button[type=submit]').attr('disabled', 'disabled');
    });

    document.body.addEventListener('htmx:afterRequest', function(evt) {
        if(evt.detail.failed){
            alert("Ha ocurrido un error al momento de llevar a cabo los cálculos de las propiedades termodinámicas. Verifique que los datos corresponden a la fase líquida del fluido ingresado y no sobrepase la temperatura crítica.");
            $('button[type=submit]').attr('disabled', 'disabled');
            $('#id_viscosidad').val("");
            $('#id_presion_vapor').val("");
            $('#id_densidad').val("");
            $('#aviso').html('');
            document.body.style.opacity = 1.0;
        }
        else
            $('button[type=submit]').removeAttr('disabled');
    });
}

document.body.addEventListener('htmx:afterRequest', function(evt) {
    document.body.style.opacity = 1.0;
});

$('#submit').click(e => {
    if(!confirm("¿Está seguro que desea realizar esta acción?"))
        evt.preventDefault();
})

anadir_listeners_htmx();
anadir_listeners_dropboxes();