// Lógica de cuando se registrará un nuevo fluido

function anadir_listeners_registro() {
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
                            document.getElementById('guardar_datos_cas_tubo').removeAttribute('disabled');
                        else{
                            document.getElementById('nombre_compuesto_tubo_cas').value += " (Ya Registrado)";
                            document.getElementById('guardar_datos_cas_tubo').setAttribute('disabled', true);
                        }
                    } else{
                        document.getElementById('nombre_compuesto_tubo_cas').value = "NO ENCONTRADO";
                        document.getElementById('guardar_datos_cas_tubo').setAttribute('disabled', true);
                    }
                }, error: (res) => {
                    document.getElementById('nombre_compuesto_tubo_cas').value = '';
                    document.getElementById('guardar_datos_cas_tubo').setAttribute('disabled', true);
                }
            });
        } else{
            document.getElementById('guardar_datos_cas_tubo').setAttribute('disabled', true);
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
            const valor = `${document.getElementById('nombre_compuesto_carcasa_cas').value}*${document.getElementById('cas_compuesto_carcasa').value}`;
            document.getElementById('fluido_carcasa').innerHTML += `<option value="${valor}" selected>${document.getElementById('nombre_compuesto_carcasa_cas').value.toUpperCase()}</option>`;
            
            if($('#temp_out_carcasa').val() !== '' && $('#temp_in_carcasa').val() !== '')
                ajaxCP($('#temp_in_carcasa').val(), $('#temp_out_carcasa').val(), $('#fluido_carcasa').val(), 'C');
            
            $('#condiciones_diseno_fluido_carcasaClose').click();
        } else
            alert("Debe de colocarle un nombre válido al compuesto.");
    });
    
    $('#guardar_datos_cas_tubo').click((e) => {
        if(document.getElementById('nombre_compuesto_tubo_cas').value !== '' && document.getElementById('nombre_compuesto_tubo_cas').value.indexOf('*')){
            const valor = `${document.getElementById('nombre_compuesto_tubo_cas').value}*${document.getElementById('cas_compuesto_tubo').value}`;
            document.getElementById('fluido_tubo').innerHTML += `<option value="${valor}" selected>${document.getElementById('nombre_compuesto_tubo_cas').value.toUpperCase()}</option>`;
            
            if($('#temp_out_tubo').val() !== '' && $('#temp_in_tubo').val() !== '')
                ajaxCP($('#temp_in_tubo').val(), $('#temp_out_tubo').val(), $('#fluido_tubo').val(), 'T');
            
            $('#condiciones_diseno_fluido_tuboClose').click();
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
        const valor = `${document.getElementById('nombre_compuesto_tubo').value}*${document.getElementById('cp_compuesto_tubo').value}`;
        const cambio_fase = $('#cambio_fase_tubo').val();

        document.getElementById('fluido_tubo').innerHTML += `<option value="${valor}" selected>${document.getElementById('nombre_compuesto_tubo').value.toUpperCase()}</option>`;

        if(cambio_fase === 'S'){
            // De acuerdo a lo flujos dados determinar cual se activa y desactiva
            if(Number($('#flujo_liquido_in_tubo').val()) !== 0 && Number($('#flujo_liquido_in_tubo').val()) === Number($('#flujo_liquido_out_tubo').val())){
                $('#cp_liquido_tubo').removeAttr('disabled');
                $('#cp_liquido_tubo').val(document.getElementById('cp_compuesto_tubo').value);
                $('#cp_gas_tubo').attr('disabled', true);
                $('#cp_gas_tubo').val('');             
            }
            else if(Number($('#flujo_vapor_in_tubo').val()) !== 0 && Number($('#flujo_vapor_in_tubo').val()) === Number($('#flujo_vapor_out_tubo').val())){
                $('#cp_gas_tubo').removeAttr('disabled');
                $('#cp_gas_tubo').val(document.getElementById('cp_compuesto_tubo').value);
                $('#cp_liquido_tubo').attr('disabled', true);
                $('#cp_liquido_tubo').val('');            
            }
        }
        else if (cambio_fase !== '-'){
            $('#cp_liquido_tubo').removeAttr('disabled');
            $('#cp_gas_tubo').removeAttr('disabled');
            document.getElementById('cp_liquido_tubo').value = document.getElementById('cp_compuesto_tubo').value;
            document.getElementById('cp_gas_tubo').value = document.getElementById('cp_compuesto_tubo').value;
        }

        $('#condiciones_diseno_fluido_tuboClose').click();
        actualizar_tipos('T');
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
        const valor = `${document.getElementById('nombre_compuesto_carcasa').value}*${document.getElementById('cp_compuesto_carcasa').value}`;
        const cambio_fase = $('#cambio_fase_carcasa').val();
        document.getElementById('fluido_carcasa').innerHTML += `<option value="${valor}" selected>${document.getElementById('nombre_compuesto_carcasa').value.toUpperCase()}</option>`;
        
        if(cambio_fase === 'S'){
            // De acuerdo a lo flujos dados determinar cual se activa y desactiva
            if(Number($('#flujo_liquido_in_carcasa').val()) !== 0 && Number($('#flujo_liquido_in_carcasa').val()) === Number($('#flujo_liquido_out_carcasa').val())){
                $('#cp_liquido_carcasa').removeAttr('disabled');
                $('#cp_liquido_carcasa').val(document.getElementById('cp_compuesto_carcasa').value);
                $('#cp_gas_carcasa').attr('disabled', true);
                $('#cp_gas_carcasa').val('');             
            }
            else if(Number($('#flujo_vapor_in_carcasa').val()) !== 0 && Number($('#flujo_vapor_in_carcasa').val()) === Number($('#flujo_vapor_out_carcasa').val())){
                $('#cp_gas_carcasa').removeAttr('disabled');
                $('#cp_gas_carcasa').val(document.getElementById('cp_compuesto_carcasa').value);
                $('#cp_liquido_carcasa').attr('disabled', true);  
                $('#cp_liquido_carcasa').val('');          
            }
        }
        else if (cambio_fase !== '-'){
            $('#cp_liquido_carcasa').removeAttr('disabled');
            $('#cp_gas_carcasa').removeAttr('disabled');
            document.getElementById('cp_liquido_carcasa').value = document.getElementById('cp_compuesto_carcasa').value;
            document.getElementById('cp_gas_carcasa').value = document.getElementById('cp_compuesto_carcasa').value;
        }

        $('#condiciones_diseno_fluido_carcasaClose').click();
        actualizar_tipos('C');
    });    
}

// Cálculo de Cp

function ajaxCP(t1,t2,fluido, lado = 'T'){
    if(lado === 'T' && $('#cambio_fase_tubo').val() !== '-' && $('#tipo_cp_tubo').val() === 'A' 
    || lado === 'C' && $('#cambio_fase_carcasa').val() !== '-' && $('#tipo_cp_carcasa').val() === 'A'){
        let cambio_fase = lado === 'C' ? $('#cambio_fase_carcasa').val() : $('#cambio_fase_tubo').val();
        $.ajax({
            url: '/intercambiadores/calcular_cp/',
            data: {
                t1,
                t2,
                fluido,
                unidad: $('#unidad_temperaturas').val(),
                unidad_salida: $('#unidad_cp').val(),
                cambio_fase,
                presion: lado === 'C' ? $('#presion_entrada_carcasa').val() : $('#presion_entrada_tubo').val(),
                unidad_presiones: $('#unidad_presiones').val(),
                flujo_vapor_in: lado === 'C' ? $('#flujo_vapor_in_carcasa').val() : $('#flujo_vapor_in_tubo').val(),
                flujo_vapor_out: lado === 'C' ? $('#flujo_vapor_out_carcasa').val() : $('#flujo_vapor_out_tubo').val(),
                flujo_liquido_in: lado === 'C' ? $('#flujo_liquido_in_carcasa').val() : $('#flujo_liquido_in_tubo').val(),
                flujo_liquido_out: lado === 'C' ? $('#flujo_liquido_out_carcasa').val() : $('#flujo_liquido_out_tubo').val()
            },
            success: (res) => {
                if(lado === 'T'){
                    if(cambio_fase !== '-' && res.cp !== '' && $('#cambio_fase_carcasa').val() !== '-')
                        $('button[type="submit"]').removeAttr('disabled');

                    if(cambio_fase === 'S')
                        if(res.fase === 'g'){
                            $('#cp_gas_tubo').val(res.cp);
                            $('#cp_liquido_tubo').val('');
                        }
                        else{
                            $('#cp_liquido_tubo').val(res.cp);
                            $('#cp_gas_tubo').val('');
                        }
                    else{                        
                        $('#cp_liquido_tubo').val(res.cp_liquido);
                        $('#cp_gas_tubo').val(res.cp_gas);
                    }
                }
                else{
                    if(cambio_fase !== '-' && res.cp !== '' && $('#cambio_fase_tubo').val() !== '-')
                        $('button[type="submit"]').removeAttr('disabled');

                    if(cambio_fase === 'S')
                        if(res.fase === 'g'){
                            $('#cp_gas_carcasa').val(res.cp);
                            $('#cp_liquido_carcasa').val('');
                        }
                        else{
                            $('#cp_liquido_carcasa').val(res.cp);
                            $('#cp_gas_carcasa').val('');
                        }
                    else{                        
                        $('#cp_liquido_carcasa').val(res.cp_liquido);
                        $('#cp_gas_carcasa').val(res.cp_gas);
                    }
                }
            }, 
            error: (res) => {
                $('button[type="submit"]').attr('disabled', true);
            }
        });
    }
}

function ajaxCPCarcasa(){
    if($('#temp_out_carcasa').val() !== '' && $('#temp_in_carcasa').val() !== '' && $('#fluido_carcasa').val() !== ''){
        ajaxCP($('#temp_in_carcasa').val(), $('#temp_out_carcasa').val(), $('#fluido_carcasa').val(), 'C');
    }
}

function ajaxCPTubo(){
    if($('#temp_out_tubo').val() !== '' && $('#temp_in_tubo').val() !== '' && $('#fluido_tubo').val() !== ''){
        ajaxCP($('#temp_in_tubo').val(), $('#temp_out_tubo').val(), $('#fluido_tubo').val(), 'T');
    }
}

function anadir_listeners_cp() {
    $('#temp_in_carcasa').keyup((e) => {
        ajaxCPCarcasa();
    });
    
    $('#temp_out_carcasa').keyup((e) => {
        ajaxCPCarcasa();
    });
    
    $('#fluido_carcasa').change((e) => {
        if($('#temp_out_carcasa').val() !== '' && $('#temp_in_carcasa').val() !== '' && $('#fluido_carcasa').val() !== ''){
            const val = $('#fluido_carcasa').val();
            if(Number(val))
                ajaxCP($('#temp_in_carcasa').val(), $('#temp_out_carcasa').val(), $('#fluido_carcasa').val(), 'C');
            else{
                const splitted = val.split('*');
                if(Number(splitted[1]))
                   console.log("carcasa");
                else
                    ajaxCP($('#temp_in_carcasa').val(), $('#temp_out_carcasa').val(), val, 'C');
            }
        }

        actualizar_tipos('C');

        if($('#cambio_fase_carcasa').val() === 'T' && $('#tipo_cp_carcasa').val() === 'M')
            $('#sat_carcasa').removeAttr('hidden');
        else
            $('#sat_carcasa').attr('hidden', true);
    });
    
    $('#temp_in_tubo').keyup((e) => {
        ajaxCPTubo();
    });
    
    $('#temp_out_tubo').keyup((e) => {
        ajaxCPTubo();
    });
    
    $('#fluido_tubo').change((e) => {
        if($('#temp_out_tubo').val() !== '' && $('#temp_in_tubo').val() !== '' && $('#fluido_tubo').val() !== ''){
            const val = $('#fluido_tubo').val();
            if(Number(val))
                ajaxCPTubo();
            else{
                const splitted = val.split('*');
                if(Number(splitted[1]))
                    console.log("tubo");
                else
                    ajaxCPTubo();
            }
        }

        actualizar_tipos('T');
        if($('#cambio_fase_tubo').val() === 'T' && $('#tipo_cp_tubo').val() === 'M')
            $('#sat_tubo').removeAttr('hidden');
        else
            $('#sat_tubo').attr('hidden', true);
    });
    
    $('#presion_entrada_carcasa').keyup((e) => {
        ajaxCPCarcasa();
    });
    
    $('#presion_entrada_tubo').keyup((e) => {
        ajaxCPTubo();
    });
}

// Cambio automático de unidades

function anadir_listeners_unidades() {
    $('#unidad_temperaturas').change((e) => {
        if($('#temp_out_carcasa').val() !== '' && $('#temp_in_carcasa').val() !== '' && $('#fluido_carcasa').val() !== ''){
            ajaxCP($('#temp_in_carcasa').val(), $('#temp_out_carcasa').val(), $('#fluido_carcasa').val(), 'C');
        }
    
        if($('#temp_out_tubo').val() !== '' && $('#temp_in_tubo').val() !== '' && $('#fluido_tubo').val() !== ''){
            ajaxCP($('#temp_in_tubo').val(), $('#temp_out_tubo').val(), $('#fluido_tubo').val(), 'T');
        }
    });
    
    $('#unidad_cp').change((e) => {
        if($('#temp_out_carcasa').val() !== '' && $('#temp_in_carcasa').val() !== '' && $('#fluido_carcasa').val() !== ''){
            ajaxCP($('#temp_in_carcasa').val(), $('#temp_out_carcasa').val(), $('#fluido_carcasa').val(), 'C');
        }
    
        if($('#temp_out_tubo').val() !== '' && $('#temp_in_tubo').val() !== '' && $('#fluido_tubo').val() !== ''){
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
    
    $('#unidad_diametros').change((e) => {
        const array = $('select[name="unidad_diametros"]').toArray().slice(1);
    
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
    
    $('#unidad_cp').change((e) => {
        const array = $('select[name="unidad_cp"]').toArray().slice(1);
    
        array.map((x) => {
            x.innerHTML = "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
        });
    });    
}

function anadir_listeners() {
    anadir_listeners_registro();
    anadir_listeners_cp();
    anadir_listeners_unidades();
}

function actualizar_tipos(lado = "T") { // Actualización de Tipos de Cálculo de Cp
    const id = lado === 'T' ? '#tipo_cp_tubo' : '#tipo_cp_carcasa';
    const id_fluido = lado === 'T' ? '#fluido_tubo' : '#fluido_carcasa';
    const id_cdf = lado === 'T' ? '#cambio_fase_tubo' : '#cambio_fase_carcasa';
    $(id).empty();

    if($(id_fluido).val() === '' || $(id_fluido).val().includes("*") && !$(id_fluido).val().split('*')[1].includes('-')){
        $(id).html(`
            <option value="M">Manual</option>
        `);

        if($(id_cdf).val() === 'S'){
            cambiar_accesibilidad_por_fase(lado);
        }
        else{
            const id_cp_liq = lado === 'T' ? '#cp_liquido_tubo' : '#cp_liquido_carcasa';
            const id_cp_gas = lado === 'T' ? '#cp_gas_tubo' : '#cp_gas_carcasa';
            $(id_cp_liq).removeAttr('disabled');  
            $(id_cp_gas).removeAttr('disabled');   
            
            if($(id_cdf).val() === 'T'){
                const id_tsat_hvap = lado === 'T' ? '#sat_tubo' : '#sat_carcasa';
                $(id_tsat_hvap).removeAttr('hidden'); 
            }

        }
        
    } else{
        $(id).html(`
            <option value="A">Automático</option>
            <option value="M">Manual</option>
        `);

        const id_cp_liq = lado === 'T' ? '#cp_liquido_tubo' : '#cp_liquido_carcasa';
        const id_cp_gas = lado === 'T' ? '#cp_gas_tubo' : '#cp_gas_carcasa';
        $(id_cp_liq).attr('disabled', true);  
        $(id_cp_gas).attr('disabled', true);            
    }
}

anadir_listeners();