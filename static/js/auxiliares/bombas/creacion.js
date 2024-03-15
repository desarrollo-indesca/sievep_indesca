function anadir_listeners_dropboxes() {
    $('#id_id_unidad').change((e) => {
        const array = $('select[name="id_unidad"]').toArray().slice(1);
    
        array.map((x) => {
            x.innerHTML = "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
        });
    });
    
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
    
    $('#id_concentracion_unidad').change((e) => {
        const array = $('select[name="concentracion_unidad"]').toArray().slice(1);
    
        array.map((x) => {
            x.innerHTML = "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
        });
    });

    $('#id_tipo_carcasa1').change((e) => {
        if(e.target.value)
            $('#id_tipo_carcasa2').removeAttr('disabled');
        else
            $('#id_tipo_carcasa2').attr('disabled','disabled');
    });
}

anadir_listeners_dropboxes();