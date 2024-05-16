const cargarEventListeners = (anadirListeners = true) => {
    $('.eliminar').click(e => {
        eliminar(e);
    });

    $('.entrada').change(e => {
        if($(`#${e.target.id}`).is(':checked'))
            $('.entrada').toArray().filter(el => el !== e.target).map(el => {
                $(el).attr('disabled','disabled');
            });
        else
            $('.entrada').toArray().filter(el => el !== e.target).map(el => {
                $(el).removeAttr('disabled');
            });
    });
    
    if(anadirListeners)
        $('.anadir').click(e => {
            anadir(e);
        });
}

const reindex = (anadir = false) => {
    let forms = document.querySelectorAll(`.form`);    
    let formRegex = RegExp(`form-(\\d)+-`,'g');
    let valores = {};

    for(let i = 0; i < forms.length; i++){
        let current_prefix = `form-${i}-`;

        forms[i].querySelectorAll('input,select').forEach(e => {
            if(!(anadir && i === forms.length - 1 && e.id.indexOf('-id') !== -1))
                valores[e.id.replace(formRegex, current_prefix)] = e.value;
            else
                valores[e.id.replace(formRegex, current_prefix)] = '';
        });

        if(forms[i].innerHTML.indexOf(current_prefix) === -1){
            forms[i].innerHTML = forms[i].innerHTML.replace(formRegex, current_prefix);
        }

        forms[i].querySelectorAll('input,select').forEach(e => {
            e.value = valores[e.id];
         });

        valores = {};
    }
}

const eliminar = e => {
    let forms = document.querySelectorAll(`.form`);
    let formNum = forms.length-1;
    let totalForms = document.querySelector(`#id_form-TOTAL_FORMS`);
    totalForms.setAttribute('value', `${formNum}`)
    e.target.parentElement.parentElement.remove();
    reindex();
    cargarEventListeners(false);
};
    
const anadir = e => {
    let forms = document.querySelectorAll(`.form`);
    let formContainer = document.querySelector(`#forms-corrientes`);
    let totalForms = document.querySelector(`#id_form-TOTAL_FORMS`);
    let formNum = forms.length-1
   
    let newForm = forms[0].cloneNode(true);
    let formRegex = RegExp(`form-(\\d)+-`,'g');
    formNum++;
    let formPrefix =  `form-${formNum}-`;
    
    
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, formPrefix);

    let newElement;

    newElement = formContainer.insertBefore(newForm,e.target.parentNode.parentNode.lastSibling);

    $(newElement).find('a.anadir').removeClass('btn-success').addClass('btn-danger').removeClass('anadir').addClass('eliminar');
    $(newElement).find('a.eliminar').html('-');

    reindex(true);

    cargarEventListeners(false);

    totalForms.setAttribute('value', `${formNum+1}`);
    
    formPrefix =  `form-${formNum}-`;
    $(`#id_${formPrefix}numero_corriente`).val("");
    $(`#id_${formPrefix}descripcion_corriente`).val("");
    $(`#id_${formPrefix}entalpia`).val("");
    $(`#id_${formPrefix}flujo`).val("");
    $(`#id_${formPrefix}presion`).val("");
    $(`#id_${formPrefix}temperatura`).val("");
    $(`#id_${formPrefix}fase`).val("");
    $(`#id_${formPrefix}entrada`).removeAttr("checked");
};

cargarEventListeners();

$('button[type=submit]').click( (e) => {
        const presiones = $('.presion').toArray().filter(x => x.value === '').length;
        const entradas = $('.entrada').toArray().filter(x => $(`#${x.id}`).is(':checked')).length;

        console.log(presiones, entradas);
        
        if(presiones > 1){
            e.preventDefault();
            alert("Debe existir solo una presión en las corrientes que esté vacía.")
            return;
        } else if(presiones < 1){
            e.preventDefault();
            alert("Debe haber una presión vacía a efectos de determinar la corriente de salida.")
            return;
        }

        if(entradas > 1){
            e.preventDefault();
            alert("Solo puede haber una corriente de entrada.");
            return;
        } else if(entradas === 0){
            e.preventDefault();
            alert("Debe haber una corriente de entrada.");
            return;
        }

        const arrayNumeros = $('.numero-corriente').toArray().map(x => x.value);
        if((new Set(arrayNumeros)).size !== arrayNumeros.length){
            e.preventDefault();
            alert("Los números de corrientes deben ser TODOS distintos.");
            return;
        }
        
        if(entradas === 1){
            const entrada = $('.entrada').toArray().filter(x => $(`#${x.id}`).is(':checked'))[0];
            const number = entrada.name.replaceAll('form','').replaceAll('-','').replaceAll(/[a-zA-Z]+/g, '');
            console.log(number);
            if($(`input[name="form-${number}-presion"]`).val() === ""){
                e.preventDefault();
                alert("La corriente de entrada no puede ser la misma que la de salida.");
                return;
            }

            if($(`select[name="form-${number}-fase"]`).val() != 'V'){
                e.preventDefault();
                alert("La turbina solo puede tener vapor en la corriente de entrada.");
                return;
            }
        }
    }
)

$('form').submit(e => {
    $('#submit').attr('disabled','disabled');
})