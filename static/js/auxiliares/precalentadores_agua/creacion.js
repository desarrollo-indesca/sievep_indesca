const anadir_listeners_dropboxes = (magnitud, seccion) => {
    const selector =  `select[name='seccion-${seccion}-${magnitud}_unidad']`;
    $(selector).change((e) => {
        const array = $(selector).toArray().slice(1);
    
        array.map((x) => {
          x.innerHTML =
            "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
        });
    });    
}


anadir_listeners_dropboxes('entalpia', 'drenaje');
anadir_listeners_dropboxes('entalpia', 'vapor');

anadir_listeners_dropboxes('temp', 'drenaje');
anadir_listeners_dropboxes('temp', 'agua');
anadir_listeners_dropboxes('temp', 'vapor');

anadir_listeners_dropboxes('presion', 'drenaje');
anadir_listeners_dropboxes('presion', 'agua');
anadir_listeners_dropboxes('presion', 'vapor');