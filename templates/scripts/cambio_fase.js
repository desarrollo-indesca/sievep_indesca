$('#tipo_cp_carcasa').change(() => {
    cambiar_segun_tipo_y_cambio();
});

$('#tipo_cp_tubo').change(() => {
    cambiar_segun_tipo_y_cambio("T");
});

function cambiar_accesibilidad_por_fase(lado = 'T'){
    if(lado === 'C'){ // Lado Carcasa
        if(Number($('#flujo_liquido_in_carcasa').val()) !== 0 && Number($('#flujo_liquido_in_carcasa').val()) === Number($('#flujo_liquido_out_carcasa').val())){
            console.log("A");
            $('#cp_liquido_carcasa').removeAttr('disabled');
            $('#cp_gas_carcasa').val('');
            $('#cp_gas_carcasa').attr('disabled', true);             
        }
        else if(Number($('#flujo_vapor_in_carcasa').val()) !== 0 && Number($('#flujo_vapor_in_carcasa').val()) === Number($('#flujo_vapor_out_carcasa').val())){
            $('#cp_gas_carcasa').removeAttr('disabled');
            $('#cp_liquido_carcasa').val('');
            $('#cp_liquido_carcasa').attr('disabled', true);             
        }
    }
    else{ // Lado Tubo
        if(Number($('#flujo_liquido_in_tubo').val()) !== 0 && Number($('#flujo_liquido_in_tubo').val()) === Number($('#flujo_liquido_out_tubo').val())){
            $('#cp_liquido_tubo').removeAttr('disabled');
            $('#cp_gas_tubo').attr('disabled', true);  
            $('#cp_gas_tubo').val('');             
        }
        else if(Number($('#flujo_vapor_in_tubo').val()) !== 0 && Number($('#flujo_vapor_in_tubo').val()) === Number($('#flujo_vapor_out_tubo').val())){
            $('#cp_gas_tubo').removeAttr('disabled');
            $('#cp_liquido_tubo').attr('disabled', true);
            $('#cp_liquido_tubo').val('');             
        }
    }
}

function cambiar_segun_tipo_y_cambio(lado = 'C') {
    if(lado === 'C'){
        const cambio_fase = $('#cambio_fase_carcasa').val();
        if(cambio_fase !== '-'){ // Verificación de si hay un tipo de cambio de fase puesto
            if($('#tipo_cp_carcasa').val() === 'A'){
                ajaxCPCarcasa();
                $('#cp_liquido_carcasa').attr('disabled',true);
                $('#cp_gas_carcasa').attr('disabled',true);
            }
            else{
                if(cambio_fase === 'S')
                    cambiar_accesibilidad_por_fase('C');
                else{ 
                    $('#cp_liquido_carcasa').removeAttr('disabled');
                    $('#cp_gas_carcasa').removeAttr('disabled'); 
                }            
            }
        }
        else{
            $('#cp_liquido_carcasa').attr('disabled',true);
            $('#cp_gas_carcasa').attr('disabled',true);            
        }
    } else if(lado === 'T'){
        const cambio_fase = $('#cambio_fase_tubo').val();
        if(cambio_fase !== '-'){ // Verificación de si hay un tipo de cambio de fase puesto
            if($('#tipo_cp_tubo').val() === 'A'){
                ajaxCPTubo();
                $('#cp_liquido_tubo').attr('disabled',true);
                $('#cp_gas_tubo').attr('disabled',true);
            }
            else{
                if(cambio_fase === 'S')
                    cambiar_accesibilidad_por_fase('T');
                else{
                    $('#cp_liquido_tubo').removeAttr('disabled');
                    $('#cp_gas_tubo').removeAttr('disabled');  
                }            
            }
        }
        else{
            $('#cp_liquido_tubo').attr('disabled',true);
            $('#cp_gas_tubo').attr('disabled',true);            
        }
    }
}