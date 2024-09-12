const cambio = () => {
    $("#resultados").html("");
    $(".change-blank").html("");
    $("#submit").val("calcular");
    $("#submit").html("Calcular Resultados");
}

const listeners_submit = () => {
    $("#submit").click((e) => {
        const suma_volumen = $('.porc-vol').toArray().reduce((acc, el) => {
            return acc + Number(el.value);
        }, 0).toFixed(2);
    
        const suma_aire = $('.porc-aire').toArray().reduce((acc, el) => { 
            return acc + Number(el.value);
        }, 0).toFixed(2);
    
        console.log(suma_aire, suma_volumen);
        
    
        if(suma_volumen != 100.00){
            e.preventDefault();
            alert("La suma de los porcentajes de volumen en la composición de los gases debe ser igual a 100.");
            return;
        }
    
        if(suma_aire != 100.00){
            e.preventDefault();
            alert("La suma de los porcentajes de aire en la composición del aire debe ser igual a 100.");
            return;
        }
    });
}
  
$("form").keyup((e) => {
    cambio();    
});
  
$("form").change((e) => {
    cambio();    
});

document.body.addEventListener("htmx:beforeRequest", function (evt) {
    if(confirm("¿Está seguro de que desea realizar esta acción?"))
        document.body.style.opacity = 0.8;
    else
        evt.preventDefault();
});

document.body.addEventListener("htmx:afterRequest", function (evt) {
    document.body.style.opacity = 1.0;
    if(evt.detail.failed){
        alert("Ha ocurrido un error al momento de realizar los cálculos. Por favor revise e intente de nuevo.");
    } else {
        listeners_submit();
    }
});

listeners_submit();