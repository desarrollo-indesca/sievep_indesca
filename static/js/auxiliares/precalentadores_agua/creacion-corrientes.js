const cargarEventListeners = (anadirListeners = true) => {
  $(".eliminar").click((e) => {
    eliminar(e);
  });

  if (anadirListeners)
    $(".anadir").click((e) => {
      anadir(e);
    });
};

const reindex = (anadir = false) => {
  let forms = document.querySelectorAll(`.form`);
  let formRegex = RegExp(`form-(\\d)+-`, "g");
  let valores = {};

  for (let i = 0; i < forms.length; i++) {
    let current_prefix = `form-${i}-`;

    forms[i].querySelectorAll("input,select").forEach((e) => {
      if (!(anadir && i === forms.length - 1 && e.id.indexOf("-id") !== -1))
        valores[e.id.replace(formRegex, current_prefix)] = e.value;
      else valores[e.id.replace(formRegex, current_prefix)] = "";
    });

    if (forms[i].innerHTML.indexOf(current_prefix) === -1) {
      forms[i].innerHTML = forms[i].innerHTML.replace(
        formRegex,
        current_prefix
      );
    }

    forms[i].querySelectorAll("input,select").forEach((e) => {
      e.value = valores[e.id];
    });

    valores = {};
  }
};

const eliminar = (e) => {
  let forms = document.querySelectorAll(`.form`);
  let formNum = forms.length - 1;
  let totalForms = document.querySelector(`#id_form-TOTAL_FORMS`);
  totalForms.setAttribute("value", `${formNum}`);
  e.target.parentElement.parentElement.remove();
  reindex();
  cargarEventListeners(false);
  $(".entrada").change();
};

const anadir = (e) => {
  let forms = document.querySelectorAll(`.form`);
  let formContainer = document.querySelector(`#forms-corrientes`);
  let totalForms = document.querySelector(`#id_form-TOTAL_FORMS`);
  let formNum = forms.length - 1;

  let newForm = forms[0].cloneNode(true);
  let formRegex = RegExp(`form-(\\d)+-`, "g");
  formNum++;
  let formPrefix = `form-${formNum}-`;

  newForm.innerHTML = newForm.innerHTML.replace(formRegex, formPrefix);

  let newElement;

  newElement = formContainer.insertBefore(
    newForm,
    e.target.parentNode.parentNode.lastSibling
  );

  $(newElement)
    .find("a.anadir")
    .removeClass("btn-success")
    .addClass("btn-danger")
    .removeClass("anadir")
    .addClass("eliminar");
  $(newElement).find("a.eliminar").html("-");

  reindex(true);

  cargarEventListeners(false);

  totalForms.setAttribute("value", `${formNum + 1}`);

  formPrefix = `form-${formNum}-`;
  $(`#id_${formPrefix}numero_corriente`).val("");
  $(`#id_${formPrefix}descripcion_corriente`).val("");
  $(`#id_${formPrefix}entalpia`).val("");
  $(`#id_${formPrefix}flujo`).val("");
  $(`#id_${formPrefix}presion`).val("");
  $(`#id_${formPrefix}temperatura`).val("");
  $(`#id_${formPrefix}fase`).val("");
  $(`#id_${formPrefix}entrada`).removeAttr("checked");

  $(".entrada").change();
};

cargarEventListeners();

$("button[type=submit]").click((e) => {
  if (!confirm("¿Está seguro que desea realizar esta acción?"))
    e.preventDefault();

  const arrayNumerosCarcasa = $(".numero-corriente-carcasa")
    .toArray()
    .map((x) => x.value);
  const arrayNumerosTubos = $(".numero-corriente-tuvos")
    .toArray()
    .map((x) => x.value);
  
  if (new Set(arrayNumerosCarcasa).size !== arrayNumerosCarcasa.length) {
    e.preventDefault();
    alert("Los números de corrientes de la carcasa deben ser TODOS distintos.");
    return;
  }
  if (new Set(arrayNumerosTubos).size !== arrayNumerosTubos.length) {
    e.preventDefault();
    alert("Los números de corrientes de los tubos deben ser TODOS distintos.");
    return;
  }
});

$("#id_presion_unidad").change((e) => {
  const array = $('select[name="presion_unidad"]').toArray().slice(1);

  array.map((x) => {
    x.innerHTML =
      "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
  });
});

$("#id_temperatura_unidad").change((e) => {
  const array = $('select[name="temperatura_unidad"]').toArray().slice(1);

  array.map((x) => {
    x.innerHTML =
      "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
  });
});

$("#id_entalpia_unidad").change((e) => {
  const array = $('select[name="entalpia_unidad"]').toArray().slice(1);

  array.map((x) => {
    x.innerHTML =
      "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
  });
});

$("#id_densidad_unidad").change((e) => {
  const array = $('select[name="densidad_unidad"]').toArray().slice(1);

  array.map((x) => {
    x.innerHTML =
      "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
  });
});

$("#id_flujo_unidad").change((e) => {
  const array = $('select[name="flujo_unidad"]').toArray().slice(1);

  array.map((x) => {
    x.innerHTML =
      "<option>" + $(`#${e.target.id} option:selected`).html() + "</option>";
  });
});

$("form").submit((e) => {
  $("#submit").attr("disabled", "disabled");
});
