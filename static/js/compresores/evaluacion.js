document.addEventListener('input', (e)=>{
        if(e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT'){
            document.getElementById('submit').outerHTML = ' <button type="submit" id="submit" name="submit" value="calcular" class="btn btn-danger">Calcular Resultados</button>';
            document.getElementById('resultados').innerHTML = '';
        }
    });

    const selects_flujo_volumetrico_unidad = document.querySelectorAll('select[name*="-flujo_volumetrico_unidad"]');
    selects_flujo_volumetrico_unidad.forEach((select1)=>{
        selects_flujo_volumetrico_unidad.forEach((select2)=>{
            if(select1.name === select2.name && select1 !== select2){
                select1.addEventListener('change', (e)=>{
                    select2.value = e.target.value;
                });
            }
        });
    });

    const selects_temperatura_unidad = document.querySelectorAll('select[name*="-temperatura_unidad"]');
    selects_temperatura_unidad.forEach((select1)=>{
        selects_temperatura_unidad.forEach((select2)=>{
            if(select1.name === select2.name && select1 !== select2){
                select1.addEventListener('change', (e)=>{
                    select2.value = e.target.value;
                });
            }
        });
    });

    const selects_presion_unidad = document.querySelectorAll('select[name*="presion_unidad"]');
    selects_presion_unidad.forEach((select)=>{
        select.innerHTML = select.innerHTML.replaceAll('</option>', 'g</option>');
    });

    const selects_presion_unidad2 = document.querySelectorAll('select[name*="-presion_unidad"]');
    selects_presion_unidad.forEach((select1)=>{
        selects_presion_unidad.forEach((select2)=>{
            if(select1.name === select2.name && select1 !== select2){
                select1.addEventListener('change', (e)=>{
                    select2.value = e.target.value;
                });
            }
        });
    });