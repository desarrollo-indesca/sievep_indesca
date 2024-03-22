const cargarEventListeners = () => {
    $('.eliminar').click(e => {
        eliminar(e);
    })
    
    $('.anadir').click(e => {
        anadir(e);
    })
}

const reindex = (lado) => {
    let forms = document.querySelectorAll(`.${lado}-form`);    
    let formRegex = RegExp(`formset-${lado}-(\\d)+-`,'g');

    for(let i = 0; i < forms.length; i++){
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

    cargarEventListeners();
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
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `formset-${lado}-${formNum}-`)
    const newElement = formContainer.insertBefore(newForm,e.target.parentNode.parentNode);

    if(formNum === 1){
        $(newElement).find('a').removeClass('btn-success');
        $(newElement).find('a').addClass('btn-danger');
        $(newElement).find('a').removeClass('anadir');
        $(newElement).find('a').addClass('eliminar');
        $(newElement).find('a').html('-');
    }

    reindex(lado);

    cargarEventListeners();

    totalForms.setAttribute('value', `${formNum+1}`);
};

cargarEventListeners();