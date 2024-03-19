function anadir_listeners_dropboxes() {
    $('#id_id_unidad').change((e) => {
        const array = $('select[name="id_unidad"]').toArray().slice(1);
    
        array.map((x) => {
            x.innerHTML = "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
        });
    });
    
    $('#id_presion_unidad').change((e) => {
        const array = $('select[name="presion_unidad"]').toArray().slice(1);
    
        array.map((x) => {
            x.innerHTML = "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
        });
    });

    $('#id_temperatura_unidad').change((e) => {
        const array = $('select[name="temperatura_unidad"]').toArray().slice(1);
    
        array.map((x) => {
            x.innerHTML = "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
        });
    });
    
    $('#id_concentracion_unidad').change((e) => {
        const array = $('select[name="concentracion_unidad"]').toArray().slice(1);
    
        array.map((x) => {
            x.innerHTML = "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
        });
    });

    $('#id_tipo_carcasa1').change((e) => {
        if(e.target.value)
            $('#id_tipo_carcasa2').removeAttr('disabled');
        else
            $('#id_tipo_carcasa2').attr('disabled','disabled');
    });

    $('#id_fluido, #id_calculo_propiedades').change((e) => {
        if(e.target.value === 'M'){
            $('#id_viscosidad').removeAttr('disabled');
            $('#id_presion_vapor').removeAttr('disabled');
            $('#id_densidad').removeAttr('disabled');
        } else{
            $('#id_viscosidad').attr('disabled', 'disabled');
            $('#id_presion_vapor').attr('disabled', 'disabled');
            $('#id_densidad').attr('disabled', 'disabled');
        }
    });
}

const anadir_listeners_htmx = () => {
    document.body.addEventListener('htmx:beforeRequest', function(evt) {
        if(document.getElementById('id_calculo_propiedades').value === 'M' || !document.getElementById('id_temperatura_presion_vapor').value){
            evt.preventDefault();
            if(document.getElementById('id_calculo_propiedades').value === 'M'){
                $('#id_viscosidad').removeAttr('disabled');
                $('#id_presion_vapor').removeAttr('disabled');
                $('#id_densidad').removeAttr('disabled');
            }            
        }
    });

    document.body.addEventListener('htmx:afterRequest', function(evt) {
        if(evt.detail.failed){
            alert("Ha ocurrido un error al momento de llevar a cabo los cálculos de las propiedades termodinámicas. Verifique que los datos corresponden a la fase líquida del fluido ingresado.");
            $('button["type"="submit"]').attr('disabled');
        }
        else
            $('button[type=submit]').removeAttr('disabled');
    });
}

anadir_listeners_htmx();
anadir_listeners_dropboxes();