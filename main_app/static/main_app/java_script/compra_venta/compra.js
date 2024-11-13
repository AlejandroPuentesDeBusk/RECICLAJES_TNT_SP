document.addEventListener('DOMContentLoaded', function () {
    //declaramos todas la constantes que nos traemos del HTML
    const checkboxes = document.querySelectorAll('.cajita');
    const lista_Material = document.getElementById('lista_material_comprar');
    const tipoCargoSelect = document.getElementById('tipo_cargo'); // Select para tipo de precio
    const total_final = document.getElementById ('total_general');
    const discount_int = document.getElementById('discount');
    const extra_charge_int = document.getElementById('extra_charge')

    // AQUI VEMOS SI ES MAYOREO O MENUDEO
    function obtenerPrecio(materialCheckbox) {
        return tipoCargoSelect.value === "Wholesale_Purchase_Price" 
               ? materialCheckbox.getAttribute('data-wholesale_purchase_price')
               : materialCheckbox.getAttribute('data-retail_purchase_price');
    }

    //Esta va a checar el carrito de compras que se creo y hacemos la suma, descuentos etc

    function actualizar_total(){
        let total_general = 0;

        lista_Material.querySelectorAll('.precio_total').forEach(span =>{
            total_general += parseFloat(span.textContent) || 0;
        });

        const discount = parseFloat(discount_int.value) || 0;
        const extra_charge = parseFloat(extra_charge_int.value) || 0;

        const total_modified = total_general - discount + extra_charge;

        total_final.textContent = `${total_modified.toFixed(2)} MXN`;
    }

    
    function actualizarMaterialSeleccionado(checkbox) {
        //primero nos traemos los datos desde la bd pero porque tambien estan relacionados con el html
        //las partes de data-material es para sacar eso de bd
        const material = checkbox.getAttribute('data-material');
        const price = obtenerPrecio(checkbox);
        const image =checkbox.getAttribute('data-image');

        // Crear o actualizar el elemento de lista
        let listItem = lista_Material.querySelector(`li[data-material="${material}"]`);
        
        if (checkbox.checked) {
            if (!listItem) {
                listItem = document.createElement('li');
                listItem.setAttribute('data-material', material);
                lista_Material.appendChild(listItem);
            }
            listItem.innerHTML = `<span> <strong> ${material}</strong></span> 
                                  <span><strong>Precio:</strong> ${price} </span>
                                  <span>
                                    <img src="${image}" alt="${material}" class="imagen">
                                  </span>
                                  <span>
                                    <input type="number" placeholder="cant(kg)" class="cant_total" required min="0" step="1">
                                  </span>
                                  <span><strong>Total:</strong> <span class="precio_total">0 MXN</span></span>`;

            const kg_input = listItem.querySelector('.cant_total');
            const precio_total = listItem.querySelector('.precio_total');


            kg_input.addEventListener('input', function(){
                const cantidad = parseFloat(kg_input.value) || 0;
                const total = (cantidad * price ).toFixed(2);
                precio_total.textContent = `${total} MXN`;
                actualizar_total();
            
            })




        } else {
            if (listItem) {
                lista_Material.removeChild(listItem);
                actualizar_total();
            }
        }
    }

    // CON ESTO VA A ESTAR CHECANDO EL ESTADO DE LAS CAJITAS
    checkboxes.forEach((checkbox) => {
        checkbox.addEventListener('change', function () {
            actualizarMaterialSeleccionado(checkbox);
        });
    });

    // CAMBIA EL PRECIO SENGUN ES MAYOREO O MENUDEO, ESTA CHECANDO ESE SELECT Y LAS CAJITAS QUE AGARRA
    tipoCargoSelect.addEventListener('change', function () {
        checkboxes.forEach((checkbox) => {
            if (checkbox.checked) {
                actualizarMaterialSeleccionado(checkbox);
            }
        });
        actualizar_total();
    });

    discount_int.addEventListener('input', actualizar_total);
    extra_charge_int.addEventListener('input', actualizar_total);
});



