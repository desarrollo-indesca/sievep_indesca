// Lógica de cuando se registrará un nuevo fluido

let fluidos_tubo = [];
let fluidos_carcasa = [];

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
            const valor = `${document.getElementById('nombre_compuesto_carcasa_cas').value}*${document.getElementById('cas_compuesto_carcasa').value}`;
            document.getElementById('fluido_carcasa').innerHTML += `<option value="${valor}" selected>${document.getElementById('nombre_compuesto_carcasa_cas').value.toUpperCase()}</option>`;
            
            if($('#temp_out_carcasa').val() !== '' && $('#temp_in_carcasa').val() !== '')
                ajaxCP($('#temp_in_carcasa').val(), $('#temp_out_carcasa').val(), $('#fluido_carcasa').val(), 'C');

            fluidos_carcasa.forEach(x => {
                x.selecto = false;
            });
    
            fluidos_carcasa.push({'nombre': document.getElementById('nombre_compuesto_carcasa_cas').value.toUpperCase(), 
                'valor': valor, 'selecto': true});
            
            $('#condiciones_diseno_fluido_carcasaClose').click();
        } else
            alert("Debe de colocarle un nombre válido al compuesto.");
    });
    
    $('#guardar_datos_cas').click((e) => {
        if(document.getElementById('nombre_compuesto_tubo_cas').value !== '' && document.getElementById('nombre_compuesto_tubo_cas').value.indexOf('*')){
            const valor = `${document.getElementById('nombre_compuesto_tubo_cas').value}*${document.getElementById('cas_compuesto_tubo').value}`;
            document.getElementById('fluido_tubo').innerHTML += `<option value="${valor}" selected>${document.getElementById('nombre_compuesto_tubo_cas').value.toUpperCase()}</option>`;
            
            if($('#temp_out_tubo').val() !== '' && $('#temp_in_tubo').val() !== '')
                ajaxCP($('#temp_in_tubo').val(), $('#temp_out_tubo').val(), $('#fluido_tubo').val(), 'T');

            fluidos_tubo.forEach(x => {
                x.selecto = false;
            });
        
            fluidos_tubo.push({'nombre': document.getElementById('nombre_compuesto_carcasa_cas').value.toUpperCase(), 
                'valor': valor, 'selecto': true});
            
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
        const valor = `${document.getElementById('nombre_compuesto_tubo').value}*${document.getElementById('cp_compuesto_tubo').value}`;
        document.getElementById('fluido_tubo').innerHTML += `<option value="${valor}" selected>${document.getElementById('nombre_compuesto_tubo').value.toUpperCase()}</option>`;
        document.getElementById('cp_tubo').value = document.getElementById('cp_compuesto_tubo').value;
        $('#condiciones_diseno_fluido_tuboLabel').click();

        fluidos_tubo.forEach(x => {
            x.selecto = false;
        });

        fluidos_tubo.push({'nombre': document.getElementById('nombre_compuesto_tubo').value.toUpperCase(), 
            'valor': valor, 'selecto': true});

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
        
        if(cambio_fase === 'S')
            document.getElementById('cp_carcasa').value = document.getElementById('cp_compuesto_carcasa').value;
        else if (cambio_fase !== '-'){
            document.getElementById('cp_liquido_carcasa').value = document.getElementById('cp_compuesto_carcasa').value;
            document.getElementById('cp_gas_carcasa').value = document.getElementById('cp_compuesto_carcasa').value;
        }

        fluidos_carcasa.forEach(x => {
            x.selecto = false;
        });

        fluidos_carcasa.push({'nombre': document.getElementById('nombre_compuesto_carcasa').value.toUpperCase(), 
            'valor': valor, 'selecto': true});

        $('#cp_carcasa').removeAttr('disabled');
        $('#cp_liquido_carcasa').removeAttr('disabled');
        $('#cp_gas_carcasa').removeAttr('disabled');

        $('#condiciones_diseno_fluido_carcasaClose').click();
        actualizar_tipos('C');
    });    
}

// Cálculo de Cp

function ajaxCP(t1,t2,fluido, lado = 'T'){
    console.log("A");
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
                        $('#cp_tubo').val(res.cp);
                    else{                        
                        $('#cp_liquido_tubo').val(res.cp_liquido);
                        $('#cp_gas_tubo').val(res.cp_gas);
                    }
                }
                else{
                    if(cambio_fase !== '-' && res.cp !== '' && $('#cambio_fase_tubo').val() !== '-')
                        $('button[type="submit"]').removeAttr('disabled');

                    if(cambio_fase === 'S')
                        $('#cp_carcasa').val(res.cp);
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
                    $('#cp_carcasa').val(Number(splitted[1]));
                else
                    ajaxCP($('#temp_in_carcasa').val(), $('#temp_out_carcasa').val(), val, 'C');
            }
        }
        
        fluidos_carcasa.forEach((x) => {
            x.selecto = x.valor === e.target.value;
        });

        actualizar_tipos('C');

        console.log(fluidos_carcasa);
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
                ajaxCP($('#temp_in_tubo').val(), $('#temp_out_tubo').val(), val, 'T');
            else{
                const splitted = val.split('*');
                if(Number(splitted[1]))
                    $('#cp_tubo').val(Number(splitted[1]));
                else
                    ajaxCP($('#temp_in_tubo').val(), $('#temp_out_tubo').val(), val, 'T');
            }
        }

        fluidos_tubo.forEach((x) => {
            x.selecto = x.valor === e.target.value;
        });

        actualizar_tipos('C');
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

$(document).ready(() => {
    $('#fluido_carcasa > option').toArray().forEach(elemento => {
        fluidos_tubo.push({'nombre': elemento.innerHTML, 'valor': elemento.value, 'selecto': $(elemento).is(':selected')})
        fluidos_carcasa.push({'nombre': elemento.innerHTML, 'valor': elemento.value, 'selecto': $(elemento).is(':selected')});
    });
});

function anadir_listeners() {
    anadir_listeners_registro();
    anadir_listeners_cp();
    anadir_listeners_unidades();
}

function actualizar_fluidos(lado = "T") {
    console.log(fluidos_carcasa);
    if(lado === 'T')
        fluidos_tubo.forEach((x) => {
            document.getElementById('fluido_tubo').innerHTML += `<option value=${x.valor} ${x.selecto ? 'selected' : ''}>${x.nombre}</option>`;
        });
    else
        fluidos_carcasa.forEach((x) => {
            document.getElementById('fluido_carcasa').innerHTML += `<option value=${x.valor} ${x.selecto ? 'selected' : ''}>${x.nombre}</option>`;
        });
}

function actualizar_tipos(lado = "T") {
    const id = lado === 'T' ? '#tipo_cp_tubo' : '#tipo_cp_carcasa';
    const id_fluido = lado === 'T' ? '#fluido_tubo' : '#fluido_carcasa';
    $(id).empty();

    if($(id_fluido).val().includes("*") && !$(id_fluido).val().split('*')[1].includes('-')){
        $(id).html(`
            <option value="M">Manual</option>
        `);
    } else{
        $(id).html(`
            <option value="A">Automático</option>
            <option value="M">Manual</option>
        `);  
    }
}

anadir_listeners();