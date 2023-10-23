const determinar_cambio_de_fase = (fve, fvs, fle, fls, lado="T") => {
    fve = Number(fve);
    fvs = Number(fvs);
    fle = Number(fle);
    fls = Number(fls);
    const validos = flujos_validos(fve, fvs, fle, fls);
    
    if(validos && (fve || fle) && (fvs || fls)){
        if(lado === 'T')
            $('#flujo_tubo').val(fls+fvs);
        else
            $('#flujo_carcasa').val(fls+fvs);

        $('button[type="submit"]').removeAttr('disabled');

        if(fve && fle)
            if(fve !== fvs)
                return "P";
            else
                return "S";

        if(fve)
            if(fve === fvs)
                return "S";
            else if(fve === fls)
                return "T";
            else
                return "P"
        else if(fle)
            if(fls === fle)
                return "S";
            else if(fle === fvs)
                return "T";
            else 
                return "P"
    }

    if(lado === 'T')
        $('#flujo_tubo').val('');
    else
        $('#flujo_carcasa').val('');

    $('button[type="submit"]').attr('disabled',true);

    return "-";
};

const determinar_cambio_de_fase_tubo = () => {
    const cambio_fase = determinar_cambio_de_fase(
        $('#flujo_vapor_in_tubo').val(),
        $('#flujo_vapor_out_tubo').val(),
        $('#flujo_liquido_in_tubo').val(),
        $('#flujo_liquido_out_tubo').val()    
    );

    $('#cambio_fase_tubo').val(cambio_fase).change();
}

const determinar_cambio_de_fase_carcasa = () => {
    const cambio_fase = determinar_cambio_de_fase(
        $('#flujo_vapor_in_carcasa').val(),
        $('#flujo_vapor_out_carcasa').val(),
        $('#flujo_liquido_in_carcasa').val(),
        $('#flujo_liquido_out_carcasa').val(),
        "C" 
    );

    $('#cambio_fase_carcasa').val(cambio_fase).change();
}

const flujos_validos = (fve, fvs, fle, fls) => {
    return fve + fle === fvs + fls;
}

$('#flujo_vapor_out_tubo').keyup(determinar_cambio_de_fase_tubo);
$('#flujo_vapor_in_tubo').keyup(determinar_cambio_de_fase_tubo);
$('#flujo_liquido_in_tubo').keyup(determinar_cambio_de_fase_tubo);
$('#flujo_liquido_out_tubo').keyup(determinar_cambio_de_fase_tubo);

$('#flujo_vapor_out_carcasa').keyup(determinar_cambio_de_fase_carcasa);
$('#flujo_vapor_in_carcasa').keyup(determinar_cambio_de_fase_carcasa);
$('#flujo_liquido_in_carcasa').keyup(determinar_cambio_de_fase_carcasa);
$('#flujo_liquido_out_carcasa').keyup(determinar_cambio_de_fase_carcasa);

if($('#flujo_vapor_out_tubo').val() && $('#flujo_vapor_in_tubo').val() && $('#flujo_liquido_in_tubo').val() && $('#flujo_liquido_out_tubo').val()){
    determinar_cambio_de_fase_tubo();
}

if($('#flujo_vapor_out_carcasa').val() && $('#flujo_vapor_in_carcasa').val() && $('#flujo_liquido_in_carcasa').val() && $('#flujo_liquido_out_carcasa').val()){
    determinar_cambio_de_fase_carcasa();
}