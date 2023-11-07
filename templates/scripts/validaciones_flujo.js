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

    if(cambio_fase !== '-'){
        if($('#fluido_tubo').val() !== '' && (Number($('#fluido_tubo').val()) || $('#fluido_tubo').val().split('*')[1].includes('-')))
            // Si tiene un tipo de cambio de fase y es un fluido puro
            cambiar_segun_tipo_y_cambio('T');
        else{
            // Si tiene un tipo de cambio de fase y es un fluido no registrado, se trata todo manual
            if(cambio_fase === 'S')
                cambiar_accesibilidad_por_fase('T');
            else{
                $('#cp_liquido_tubo').removeAttr('disabled');
                $('#cp_gas_tubo').removeAttr('disabled');
            }
        }

        if(cambio_fase === 'P')
            $('#sat_tubo').attr("hidden", true);        
        
        actualizar_tipos('T');
    }

    anadir_listeners();
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

    if(cambio_fase !== '-'){
        if($('#fluido_carcasa').val() !== '' && (Number($('#fluido_carcasa').val()) || $('#fluido_carcasa').val().split('*')[1].includes('-')))
            // Si tiene un tipo de cambio de fase y es un fluido puro
            cambiar_segun_tipo_y_cambio();
        else{
            // Si tiene un tipo de cambio de fase y es un fluido no registrado, se trata todo manual
            if(cambio_fase === 'S')
                cambiar_accesibilidad_por_fase('T');
            else{
                $('#cp_liquido_carcasa').removeAttr('disabled');
                $('#cp_gas_carcasa').removeAttr('disabled');
            }   
        }

        if(cambio_fase === 'P')
            $('#sat_carcasa').attr("hidden", true);

        // {% if intercambiador %}
        actualizar_tipos('C');
        // {% endif %}
    }
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

// {% if not intercambiador %}

if($('#flujo_vapor_out_tubo').val() && $('#flujo_vapor_in_tubo').val() && $('#flujo_liquido_in_tubo').val() && $('#flujo_liquido_out_tubo').val()){
    determinar_cambio_de_fase_tubo();
}

if($('#flujo_vapor_out_carcasa').val() && $('#flujo_vapor_in_carcasa').val() && $('#flujo_liquido_in_carcasa').val() && $('#flujo_liquido_out_carcasa').val()){
    determinar_cambio_de_fase_carcasa();
}

// {% endif %}