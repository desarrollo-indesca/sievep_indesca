$('.porc-vol').keyup(e => 
    $('#total-vol').val(
        $('.porc-vol').toArray().reduce((acc, el) => {
            return acc + Number(el.value);
        }, 0).toFixed(2)
    )
);

$('.porc-aire').keyup(e =>
    $('#total-aire').val(
        $('.porc-aire').toArray().reduce((acc, el) => {
            return acc + Number(el.value);
        }, 0).toFixed(2)
    )
);

const inicializarEventListeners = () => {
    $('#submit').click(e => {  
        // Verificar que la suma de ambos porcentajes correspondan al 100%
        const suma_volumen = $('.porc-vol').toArray().reduce((acc, el) => {
            return acc + Number(el.value);
        }, 0).toFixed(2);
    
        const suma_aire = $('.porc-aire').toArray().reduce((acc, el) => { 
            return acc + Number(el.value);
        }, 0).toFixed(2);
    
        console.log(suma_volumen, suma_aire);

        if (!Array.from(document.querySelectorAll('.form-control, .form-select')).every(el => el.checkValidity())) {
            e.preventDefault();
            alert("Todos los campos deben ser llenados para poder realizar los cálculos correspondientes.");
            return;
        }
    
        if(suma_volumen != 100.00){
            e.preventDefault();
            alert("La suma de los porcentajes de volumen en la composición del combustible debe ser igual a 100.");
            return;
        }
    
        if(suma_aire != 100.00){
            e.preventDefault();
            alert("La suma de los porcentajes de aire en la composición del combustible debe ser igual a 100.");
            return;
        }
    
        if(!confirm("¿Está seguro que desea realizar esta acción?"))
            e.preventDefault();
    });
}

const inicializarResultados = () => {
    $('#resultados').html(`
        <div class="d-flex justify-content-center w-100">
            <button type="submit" id="submit" class="btn btn-danger w-full">Calcular Resultados</button>
        </div>`
    );
}

$('.form-control, .form-select').change(e => {
    inicializarResultados();
    inicializarEventListeners();
});

$('.form-control').keyup(e => {
    inicializarResultados();
    inicializarEventListeners();
});

document.addEventListener("htmx:beforeRequest", function (evt) {
    document.body.style.opacity = 0.8;
  });

document.addEventListener("htmx:afterRequest", function (evt) {
  document.body.style.opacity = 1.0;
  inicializarEventListeners();
});