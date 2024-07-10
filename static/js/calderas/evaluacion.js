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

$('#submit').click(e => {  
    // Verificar que la suma de ambos porcentajes correspondan al 100%
    const suma_volumen = $('.porc-vol').toArray().reduce((acc, el) => {
        return acc + Number(el.value);
    }, 0).toFixed(2);

    const suma_aire = $('.porc-aire').toArray().reduce((acc, el) => { 
        return acc + Number(el.value);
    }, 0).toFixed(2);

    console.log(suma_volumen, suma_aire);

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