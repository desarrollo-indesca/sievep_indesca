$("#id_especificaciones-caldera-temperatura_unidad").change(() => {
    $("select[name='especificaciones-caldera-temperatura_unidad']").val($("#id_especificaciones-caldera-temperatura_unidad").val())
});

$("#id_especificaciones-caldera-presion_unidad").change(() => {
    $("select[name='especificaciones-caldera-presion_unidad']").val($("#id_especificaciones-caldera-presion_unidad").val())
});

$("#id_tambor-temperatura_unidad").change(() => {
    $("select[name='tambor-temperatura_unidad']").val($("#id_tambor-temperatura_unidad").val())
});

$("#id_sobrecalentador-presion_unidad").change(() => {
    $("select[name='sobrecalentador-presion_unidad']").val($("#id_sobrecalentador-presion_unidad").val())
});

$("#id_sobrecalentador-presion_unidad").change(() => {
    $("select[name='sobrecalentador-presion_unidad']").val($("#id_sobrecalentador-presion_unidad").val())
});

$("#id_dimensiones-caldera-dimensiones_unidad").change(() => {
    $("select[name='dimensiones-caldera-dimensiones_unidad']").val($("#id_dimensiones-caldera-dimensiones_unidad").val())
});

$("#id_tambor-presion_unidad").change(() => {
    $("select[name='tambor-presion_unidad']").val($("#id_tambor-presion_unidad").val())
});

$("#id_chimenea-dimensiones_unidad").change(() => {
    $("select[name='chimenea-dimensiones_unidad']").val($("#id_chimenea-dimensiones_unidad").val())
});

$("#id_tambor-superior-dimensiones_unidad").change(() => {
    $("select[name='tambor-superior-dimensiones_unidad']").val($("#id_tambor-superior-dimensiones_unidad").val())
});

$("#id_tambor-inferior-dimensiones_unidad").change(() => {
    $("select[name='tambor-inferior-dimensiones_unidad']").val($("#id_tambor-inferior-dimensiones_unidad").val())
});

$("#id_combustible-liquido").change(e => {
    console.log(e.target.checked);
    if($(e.target).is(':checked'))
        $("#id_combustible-nombre_liquido").removeAttr("disabled");
    else{
        $("#id_combustible-nombre_liquido").val("");
        $("#id_combustible-nombre_liquido").attr("disabled","");
    }
});