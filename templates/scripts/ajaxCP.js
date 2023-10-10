$('.no-submit').click((e) => {
    e.preventDefault();
});

$('#cas_compuesto_tubo').keyup((e) => {
    let valor = document.getElementById('cas_compuesto_tubo').value;
    if(valor.split('').filter(x => x === '-').length == 2){
        $.ajax({
            url: '/intercambiadores/consultar_cas/', data: {
                'cas': document.getElementById('cas_compuesto_tubo').value
            }, success: (res) => {
                if(res.estado === 1 || res.estado === 2){
                    document.getElementById('nombre_compuesto_tubo_cas').value = res.nombre;
                    if(res.estado === 1)
                        document.getElementById('guardar_datos_cas').removeAttribute('disabled');
                    else{
                        document.getElementById('nombre_compuesto_tubo_cas').value += " (Ya Registrado)";
                        document.getElementById('guardar_datos_cas').setAttribute('disabled', true);
                    }
                } else{
                    document.getElementById('nombre_compuesto_tubo_cas').value = "NO ENCONTRADO";
                    document.getElementById('guardar_datos_cas').setAttribute('disabled', true);
                }
            }, error: (res) => {
                document.getElementById('nombre_compuesto_tubo_cas').value = '';
                document.getElementById('guardar_datos_cas').setAttribute('disabled', true);
            }
        });
    } else{
        document.getElementById('guardar_datos_cas').setAttribute('disabled', true);
    }
});

$('#cas_compuesto_carcasa').keyup((e) => {
    let valor = document.getElementById('cas_compuesto_carcasa').value;
    if(valor.split('').filter(x => x === '-').length == 2){
        $.ajax({
            url: '/intercambiadores/consultar_cas/', data: {
                'cas': document.getElementById('cas_compuesto_carcasa').value
            }, success: (res) => {
                if(res.estado === 1 || res.estado === 2){
                    document.getElementById('nombre_compuesto_carcasa_cas').value = res.nombre;
                    if(res.estado === 1)
                        document.getElementById('guardar_datos_cas_carcasa').removeAttribute('disabled');
                    else{
                        document.getElementById('nombre_compuesto_carcasa_cas').value += " (Ya Registrado)";
                        document.getElementById('guardar_datos_cas_carcasa').setAttribute('disabled', true);
                    }
                } else{
                    document.getElementById('nombre_compuesto_carcasa_cas').value = "NO ENCONTRADO";
                    document.getElementById('guardar_datos_cas_carcasa').setAttribute('disabled', true);
                }
            }, error: (res) => {
                document.getElementById('nombre_compuesto_carcasa_cas').value = '';
                document.getElementById('guardar_datos_cas_carcasa').setAttribute('disabled', true);
            }
        });
    } else{
        document.getElementById('guardar_datos_cas_carcasa').setAttribute('disabled', true);
    }
});

$('#guardar_datos_cas_carcasa').click((e) => {
    if(document.getElementById('nombre_compuesto_carcasa_cas').value !== '' && document.getElementById('nombre_compuesto_carcasa_cas').value.indexOf('*')){
        document.getElementById('fluido_carcasa').innerHTML += `<option value="${document.getElementById('nombre_compuesto_carcasa_cas').value}*${document.getElementById('cas_compuesto_carcasa').value}" selected>${document.getElementById('nombre_compuesto_carcasa_cas').value.toUpperCase()}</option>`;
        
        if($('#temp_out_carcasa').val() !== '' && $('#temp_in_carcasa').val() !== '')
            ajaxCP($('#temp_in_carcasa').val(), $('#temp_out_carcasa').val(), $('#fluido_carcasa').val(), 'C');
        
        $('#condiciones_diseno_fluido_carcasaClose').click();
    } else
        alert("Debe de colocarle un nombre válido al compuesto.");
});

$('#guardar_datos_cas').click((e) => {
    if(document.getElementById('nombre_compuesto_tubo_cas').value !== '' && document.getElementById('nombre_compuesto_tubo_cas').value.indexOf('*')){
        document.getElementById('fluido_tubo').innerHTML += `<option value="${document.getElementById('nombre_compuesto_tubo_cas').value}*${document.getElementById('cas_compuesto_tubo').value}" selected>${document.getElementById('nombre_compuesto_tubo_cas').value.toUpperCase()}</option>`;
        
        if($('#temp_out_tubo').val() !== '' && $('#temp_in_tubo').val() !== '')
            ajaxCP($('#temp_in_tubo').val(), $('#temp_out_tubo').val(), $('#fluido_tubo').val(), 'T');
        
        $('#condiciones_diseno_fluido_tuboLabel').click();
    } else
        alert("Debe de colocarle un nombre válido al compuesto.");
});

$('#nombre_compuesto_tubo').keyup((e) => {
    if(e.target.value !== '' && $('#cp_compuesto_tubo').val() !== ''){
        document.getElementById('enviar_compuesto_tubo_ficha').removeAttribute('disabled');
    } else
        document.getElementById('enviar_compuesto_tubo_ficha').setAttribute('disabled', true);               
});

$('#cp_compuesto_tubo').keyup((e) => {
    if(e.target.value !== '' && $('#nombre_compuesto_tubo').val() !== ''){
        document.getElementById('enviar_compuesto_tubo_ficha').removeAttribute('disabled');
    } else
        document.getElementById('enviar_compuesto_tubo_ficha').setAttribute('disabled', true);            
});

$('#enviar_compuesto_tubo_ficha').click((e) => {
    document.getElementById('fluido_tubo').innerHTML += `<option value="${document.getElementById('nombre_compuesto_tubo').value}*${document.getElementById('cp_compuesto_tubo').value}" selected>${document.getElementById('nombre_compuesto_tubo').value.toUpperCase()}</option>`;
    document.getElementById('cp_tubo').value = document.getElementById('cp_compuesto_tubo').value;
    $('#condiciones_diseno_fluido_tuboLabel').click();
});

$('#nombre_compuesto_carcasa').keyup((e) => {
    if(e.target.value !== '' && $('#cp_compuesto_carcasa').val() !== ''){
        document.getElementById('enviar_compuesto_carcasa_ficha').removeAttribute('disabled');
    } else
        document.getElementById('enviar_compuesto_carcasa_ficha').setAttribute('disabled', true);               
});

$('#cp_compuesto_carcasa').keyup((e) => {
    if(e.target.value !== '' && $('#nombre_compuesto_carcasa').val() !== ''){
        document.getElementById('enviar_compuesto_carcasa_ficha').removeAttribute('disabled');
    } else
        document.getElementById('enviar_compuesto_carcasa_ficha').setAttribute('disabled', true);            
});

$('#enviar_compuesto_carcasa_ficha').click((e) => {
    document.getElementById('fluido_carcasa').innerHTML += `<option value="${document.getElementById('nombre_compuesto_carcasa').value}*${document.getElementById('cp_compuesto_carcasa').value}" selected>${document.getElementById('nombre_compuesto_carcasa').value.toUpperCase()}</option>`;
    document.getElementById('cp_carcasa').value = document.getElementById('cp_compuesto_carcasa').value;
    $('#condiciones_diseno_fluido_carcasaClose').click();
});

$('#temp_in_carcasa').change((e) => {
    if($('#temp_out_carcasa').val() !== '' && $('#temp_in_carcasa').val() !== ''){
        ajaxCP($('#temp_in_carcasa').val(), $('#temp_out_carcasa').val(), $('#fluido_carcasa').val(), 'C');
    }
});

$('#temp_out_carcasa').change((e) => {
    if($('#temp_out_carcasa').val() !== '' && $('#temp_in_carcasa').val() !== ''){
        ajaxCP($('#temp_in_carcasa').val(), $('#temp_out_carcasa').val(), $('#fluido_carcasa').val(), 'C');
    }
});

$('#fluido_carcasa').change((e) => {
    if($('#temp_out_carcasa').val() !== '' && $('#temp_in_carcasa').val() !== ''){
        const val = $('#fluido_carcasa').val();
        if(Number(val))
            ajaxCP($('#temp_in_carcasa').val(), $('#temp_out_carcasa').val(), $('#fluido_carcasa').val(), 'C');
        else{
            const splitted = val.split('*');
            if(Number(splitted[1]))
                $('#cp_carcasa').val(Number(splitted[1]));
            else
                ajaxCP($('#temp_in_carcasa').val(), $('#temp_out_carcasa').val(), val, 'C');
        }
    }
});

$('#temp_in_tubo').change((e) => {
    if($('#temp_out_tubo').val() !== '' && $('#temp_in_tubo').val() !== ''){
         ajaxCP($('#temp_in_tubo').val(), $('#temp_out_tubo').val(), $('#fluido_tubo').val(), 'T');
    }
});

$('#temp_out_tubo').change((e) => {
    if($('#temp_out_tubo').val() !== '' && $('#temp_in_tubo').val() !== ''){
         ajaxCP($('#temp_in_tubo').val(), $('#temp_out_tubo').val(), $('#fluido_tubo').val(), 'T');
    }
});

$('#fluido_tubo').change((e) => {
    if($('#temp_out_tubo').val() !== '' && $('#temp_in_tubo').val() !== ''){
        const val = $('#fluido_tubo').val();
        if(Number(val))
            ajaxCP($('#temp_in_tubo').val(), $('#temp_out_tubo').val(), val, 'T');
        else{
            const splitted = val.split('*');
            if(Number(splitted[1]))
                $('#cp_tubo').val(Number(splitted[1]));
            else
                ajaxCP($('#temp_in_tubo').val(), $('#temp_out_tubo').val(), val, 'T');
        }
    }
});

function ajaxCP(t1,t2,fluido, lado = 'T'){
    if(lado === 'T'){
        $('#cp_tubo').val('');
        document.getElementById('cp_tubo').setAttribute('disabled', true);
    }
    else{
        $('#cp_carcasa').val('');
        document.getElementById('cp_carcasa').setAttribute('disabled', true);
    }
    
    $.ajax({
        url: '/intercambiadores/calcular_cp/',
        data: {
            t1,
            t2,
            fluido,
            unidad: $('#unidad_temperaturas').val()
        },
        success: (res) => {
            if(res.cp !== '')
                if(lado === 'T'){
                    $('#cp_tubo').val(res.cp);
                    $('#cp_tubo').removeAttr('disabled');
                }
                else{
                    $('#cp_carcasa').val(res.cp);
                    $('#cp_carcasa').removeAttr('disabled');
                }
        }, 
        error: (res) => {
            console.log(res);
            $('#cp_tubo').removeAttr('disabled');
            $('#cp_carcasa').removeAttr('disabled');
        }
    });
}

$('#unidad_temperaturas').change((e) => {
    if($('#temp_out_carcasa').val() !== '' && $('#temp_in_carcasa').val() !== ''){
        ajaxCP($('#temp_in_carcasa').val(), $('#temp_out_carcasa').val(), $('#fluido_carcasa').val(), 'C');
    }

    if($('#temp_out_tubo').val() !== '' && $('#temp_in_tubo').val() !== ''){
        ajaxCP($('#temp_in_tubo').val(), $('#temp_out_tubo').val(), $('#fluido_tubo').val(), 'T');
    }
});

$('#unidad_temperaturas').change((e) => {
    const array = $('select[name="unidad_temperaturas"]').toArray().slice(1);

    array.map((x) => {
        x.innerHTML = "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
    });
});

$('#unidad_presiones').change((e) => {
    const array = $('select[name="unidad_presiones"]').toArray().slice(1);

    array.map((x) => {
        x.innerHTML = "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
    });
});

$('#unidad_flujos').change((e) => {
    const array = $('select[name="unidad_flujos"]').toArray().slice(1);

    array.map((x) => {
        x.innerHTML = "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
    });
});

$('#unidad_fouling').change((e) => {
    const array = $('select[name="unidad_fouling"]').toArray().slice(1);

    array.map((x) => {
        x.innerHTML = "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
    });
});

$('#unidades_pitch').change((e) => {
    const array = $('select[name="unidad_diametros"]').toArray().slice(1);

    array.map((x) => {
        x.innerHTML = "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
    });
});