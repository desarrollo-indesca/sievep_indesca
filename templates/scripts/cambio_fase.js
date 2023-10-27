$('#tipo_cp_carcasa').change(() => {
    cambiar_segun_tipo_y_cambio();
    actualizar_fluidos("C");
});

function cambiar_segun_tipo_y_cambio(lado = 'C') {
    if(lado === 'C'){
        $.ajax({
            url: '/intercambiadores/renderizar/', data: {
                'lado': 'C',
                'cambio_fase': $('#cambio_fase_carcasa').val()
            }, success: (res) => {
                $('#parte_dinamica_carcasa').html(res);
            }, error: (res) => {
                console.log(res);
            },
            async: false
        });

        if($('#cambio_fase_carcasa').val() === 'S'){
            if($('#tipo_cp_carcasa').val() === 'A'){
                ajaxCPCarcasa();
                $('#cp_carcasa').attr('disabled',true);
            }
            else
                $('#cp_carcasa').removeAttr('disabled'); 
        }
        else if($('#cambio_fase_carcasa').val() === 'P' || $('#cambio_fase_carcasa').val() === 'T'){
            // Actualizar formulario de acuerdo a si el Cp es activo o inactivo
            if($('#tipo_cp_carcasa').val() === 'A'){
                ajaxCPCarcasa();
                $('#cp_liquido_carcasa').attr('disabled',true);
                $('#cp_gas_carcasa').attr('disabled',true);
            }
            else{
                $('#cp_liquido_carcasa').removeAttr('disabled');
                $('#cp_gas_carcasa').removeAttr('disabled');                
            }
        }
        else if($('#cambio_fase_carcasa').val() === '-')
            $('#cp_carcasa').attr('disabled',true);

        anadir_listeners();
    }
}