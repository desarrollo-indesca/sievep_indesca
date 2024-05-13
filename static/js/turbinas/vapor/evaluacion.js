$('select[name="flujo_entrada_unidad"]').change(e => {
    $('select[name="flujo_entrada_unidad"]').val(e.target.value);
});

$('select[name="presion_unidad"]').html($('select[name="presion_unidad"]').html().replaceAll('</option>', 'g</option>'));

$('form').change(e => {
    $('.resultado').html("");
    $('form').removeClass('was-validated');

    $('#submit').html("Calcular Resultados");
    $('#submit').val("calcular");
});

document.body.addEventListener('htmx:beforeRequest', function(evt) {
    if($('input.form-control').toArray().filter(x => x.value === '' && !x.disabled).length || $('select').toArray().filter(x => x.value === '' && !x.disabled).length){
        evt.preventDefault();
        alert("Todos los campos deben haber sido llenados para poder calcular.");
    }

    if(!$('form')[0].checkValidity()){
        evt.preventDefault();
        alert("Ocurrió un error al momento de evaluar la turbina. Por favor verifique los datos ingresados.");
    }
});

document.body.addEventListener('htmx:afterRequest', function(evt) {
    if(evt.detail.failed)
        alert("Ocurrió un error al momento de evaluar la turbina. Por favor verifique los datos ingresados.");
});