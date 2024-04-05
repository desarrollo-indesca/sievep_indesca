const cargarEventListeners = (anadirListeners = true) => {
    $('.eliminar').click(e => {
        eliminar(e);
    });
    
    if(anadirListeners)
        $('.anadir').click(e => {
            anadir(e);
        });
}

const reindex = (lado) => {
    let forms = document.querySelectorAll(`.${lado}-form`);    
    let formRegex = RegExp(`formset-${lado}-(\\d)+-`,'g');

    console.log(forms);

    for(let i = 0; i < forms.length; i++){

        console.log(forms[i].innerHTML.indexOf(`formset-${lado}-${i}-`) === -1);
        if(forms[i].innerHTML.indexOf(`formset-${lado}-${i}-`) === -1)
            forms[i].innerHTML = forms[i].innerHTML.replace(formRegex, `formset-${lado}-${i}-`);
    }
}

const eliminar = e => {
    const lado = e.target.parentElement.parentElement.parentElement.id === 'forms-succion' ? 'succion' : 'descarga';
    let forms = document.querySelectorAll(`.${lado}-form`);
    let formNum = forms.length-1;
    let totalForms = document.querySelector(`#id_formset-${lado}-TOTAL_FORMS`);
    totalForms.setAttribute('value', `${formNum}`)
    e.target.parentElement.parentElement.remove();
    reindex(lado);

    cargarEventListeners(false);
};
    
const anadir = e => {
    const lado = e.target.parentElement.parentElement.parentElement.id === 'forms-succion' ? 'succion' : 'descarga';
    let forms = document.querySelectorAll(`.${lado}-form`);
    let formContainer = document.querySelector(`#forms-${lado}`);
    let totalForms = document.querySelector(`#id_formset-${lado}-TOTAL_FORMS`);
    let formNum = forms.length-1
    
    let newForm = forms[0].cloneNode(true)
    let formRegex = RegExp(`formset-${lado}-(\\d)+-`,'g')
    
    formNum++
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `formset-${lado}-${formNum}-`);

    let newElement;

    newElement = formContainer.insertBefore(newForm,e.target.parentNode.parentNode.lastChild.nextSibling);

    $(newElement).find('a.anadir').removeClass('btn-success').addClass('btn-danger').removeClass('anadir').addClass('eliminar');
    $(newElement).find('a.eliminar').html('-');

    reindex(lado);

    cargarEventListeners(false);

    totalForms.setAttribute('value', `${formNum+1}`);
};

cargarEventListeners();