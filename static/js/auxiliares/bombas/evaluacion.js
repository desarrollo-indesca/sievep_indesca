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

$('#id_fluido, #id_calculo_propiedades').change((e) => {
    if(e.target.value === 'A'){
        $('#id_viscosidad').attr('disabled', 'disabled');
        $('#id_presion_vapor').attr('disabled', 'disabled');
        $('#id_densidad').attr('disabled', 'disabled');
    } else{
        $('#id_viscosidad').removeAttr('disabled');
        $('#id_presion_vapor').removeAttr('disabled');
        $('#id_densidad').removeAttr('disabled');        
    }
});

$('#id_calculo_propiedades').change((e) => {
    if('MF'.indexOf(e.target.value) !== -1)
        $('button[type=submit]').removeAttr('disabled');
})

document.body.addEventListener('htmx:beforeRequest', function(evt) {
    const body = document.getElementsByTagName('body')[0]
    body.style.opacity = 0.25;

    if('MF'.indexOf(document.getElementById('id_calculo_propiedades')) !== -1 || 
        document.getElementById('id_temperatura_operacion').value === '' ||
        document.getElementById('id_presion_succion').value === ''
    ){
        evt.preventDefault();
        if('MF'.indexOf(document.getElementById('id_calculo_propiedades')) !== -1){
            $('#id_viscosidad').removeAttr('disabled');
            $('#id_presion_vapor').removeAttr('disabled');
            $('#id_densidad').removeAttr('disabled');
            $('#aviso').html('');
        }            
        body.style.opacity = 1.0;
    } else
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

document.body.addEventListener('htmx:afterRequest', function(evt) {
    document.body.style.opacity = 1.0;
});