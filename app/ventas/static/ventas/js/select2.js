
function getCSRFToken() {
    return $('meta[name="csrf-token"]').attr('content');
}

var venta = {
    items: {
        total: 0.00,
        productos: [],
        pagos:[],
    },
    get_ids: function () {
        var ids = [];
        $.each(this.items.productos, function (key,value){
            ids.push(value.id);
        });
        return ids;
    },
    calcular_invoice: function(){
        var total = 0.00;
        $.each(this.items.productos, function(pos, dict){
            dict.pos = pos;
            dict.subtotal = dict.cantidad * parseFloat(dict.precio);
            total += dict.subtotal;
        });
        this.items.total = total;
        $('input[name="total"]').val(total);
    },
    add: function(item) {
        var existe = this.items.productos.find(prod => prod.codigo_barra === item.codigo_barra);
        if (existe) {
            existe.cantidad += 1;
        } else {
            this.items.productos.push(item);
        }
        this.listar();
    },
    addPago: function(item){
        this.items.pagos.push(item);
    },
    listar : function(){
        console.log(this.get_ids());
        this.calcular_invoice();
        // Configurar AJAX para incluir el token CSRF en los encabezados
        $.ajaxSetup({
            headers: {
                'X-CSRFToken': getCSRFToken()  // Incluir el token CSRF en el encabezado
            }
        });
        
        // Obtener la URL base para editar y eliminar
        var baseUrl = window.location.pathname.replace('inventario/', '');  // Elimina la parte 'inventario' para tener la URL base
        
        tabla = $('#table').DataTable({
            responsive: true,
            destroy: true,
            data: this.items.productos,
            columns: [
                { data: "id" },
                { data: "text" },
                { data: "categoria" },
                { data: "marca" },
                { data: "precio" },
                { data: "stock" },
                { data: "cantidad" },
                { data: "subtotal" }
            ],
            columnDefs: [
                {
                    targets: [0],  // Columna de acciones
                    class: 'text-center',
                    orderable: false,
                    render: function(data, type, row) {
                        return `
                        <a rel="remove" class="buttom_eliminar">
                        <i class="fas fa-trash-alt"></i></a>`;
                    }
                },
                {
                    targets: [-4, -1],  // Columna de precio y subtotal
                    class: 'text-center',
                    orderable: false,
                    render: function(data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],  // Columna de cantidad
                    class: 'text-center',
                    orderable: false,
                    render: function(data, type, row) {
                        return `
                            <input 
                            type="text" 
                            name="cantidad" 
                            class="form-control form-control-sm input-sm" 
                            autocomplete="off" 
                            value="${row.cantidad}" 
                            pattern="^[1-9][0-9]*$" 
                            title="Ingrese un número entero ">
                    `;
                    }
                }
            ],
            rowCallback( row, data, displayNum, displayIndex, dataIndex ){
                $(row).find('input[name="cantidad"]').TouchSpin({
                    min: 1,
                    max: data.stock,
                    step: 1,
                })
            },
        });

        if (this.items.productos.length === 0) {
            $('#id_metodo_pago').val('');
            venta.items.pagos = [];
            $('#id_metodo_pago').attr('disabled', 'disabled');  // Deshabilitar si no hay productos
        } else {
            $('#id_metodo_pago').removeAttr('disabled');  // Habilitar si hay productos
        }
    },

}
$(function () {
    // Inicialización de select2 para el elemento con nombre "search"
    $('.select2[name="search"]').select2({
        language: "es",
        allowClear: true,
        ajax: {
            delay: 250,
            url: window.location.pathname,
            type: 'POST',
            data: function (params) {
                return {
                    term: params.term,  // Término de búsqueda ingresado por el usuario
                    action: 'autocomplete',  // Acción a realizar en el backend
                    ids: JSON.stringify(venta.get_ids())
                };
            },
            headers: {
                'X-CSRFToken': getCSRFToken()  // Añadir token CSRF aquí
            },
            processResults: function (data) {
                return {
                    results: data.results.map(function (item) {
                        return {
                            id: item.id,
                            text: item.text,  // Nombre del producto
                            imagen: item.imagen,
                            categoria: item.categoria,
                            marca: item.marca,
                            codigo_barra: item.codigo_barra,
                            precio: item.precio,
                            stock: item.stock
                        };
                    })
                };
            }
        },
        placeholder: "Ingrese una descripción",  // Texto mostrado cuando el campo está vacío
        minimumInputLength: 1,  // Número mínimo de caracteres para activar la búsqueda
        templateResult: function (data) {
            // Plantilla para mostrar los resultados en el dropdown
            var $container = $('<div class="product-result">');
            var $image = $('<img class="img-fluid" width="50" height="50" />').attr('src', data.imagen);
            var $text = $('<div class="product-info">')
                .append('<strong>' + data.text + '</strong><br>')
                .append('<span>' + (data.categoria || '') + ' | ' + (data.marca || '') + '</span>');

            if (data.codigo_barra) {
                $text.append('<br><span>' + data.codigo_barra + '</span>');  // Mostrar código de barras si existe
            }

            $container.append($image).append($text);
            return $container;
        },
        templateSelection: function (data) {
            // Plantilla para mostrar el elemento seleccionado
            return data.text || "Seleccione un producto";  // Nombre del producto o texto por defecto
        }
    });
    $('.select2[name="search"]').on('select2:select', function (event) {
        console.clear();
        var selectedItem = event.params.data;  // Obtenemos los datos seleccionados
        selectedItem.cantidad = 1;  // Establecemos la cantidad por defecto a 1
        selectedItem.subtotal = 0;
        venta.add(selectedItem);
        console.log("Datos actuales de venta.items:", venta.items);
    });

    $('.eliminar_todo').on('click', function(){
        alert_confirm("Notificaciones", "Estas Seguro de eliminar todo los items?",
            function(){
                venta.items.productos = [];
                venta.listar();
            }
        )
    });
     

    
    //envento Eliminar 
    $('#table tbody')
    .on('click', 'a[rel="remove"]', function() {
        var tr = tabla.cell($(this).closest('td, li')).index();
        venta.items.productos.splice(tr.row,1);
        venta.listar()
    })
    .on('change', 'input[name="cantidad"]', function() {
        var cantidad = parseInt($(this).val());
        var tr = tabla.cell($(this).closest('td, li')).index();
        venta.items.productos[tr.row].cantidad = cantidad;
        venta.calcular_invoice();
        $('td:eq(7)',tabla.row(tr.row).node()).html('$'+venta.items.productos[tr.row].subtotal.toFixed(2));
    });
    
    $('#formRegistrarVenta').on('submit', function(e) {
        e.preventDefault();
    
        if (venta.items.productos.length === 0) {
            alertError("Debe tener al menos un item en su detalle de venta");
            return; // Salir de la función si no hay productos en la venta
        }
    
        // Llamamos a la función de confirmación
        mostrarConfirmacionVenta().then((result) => {
            if (result.isConfirmed) {
                // Si el usuario confirma, proceder con el envío de la solicitud AJAX
    
                // Crear un objeto FormData para enviar los datos del formulario, incluyendo archivos
                var formData = new FormData(this);
                
                // Añadir los datos de ventas al FormData
                formData.append('action', 'add');
                formData.append('ventas', JSON.stringify(venta.items));
                
                // Verificar que el CSRF Token es válido
                var csrfToken = getCSRFToken();
                if (!csrfToken) {
                    alert("Error: CSRF Token no válido o no encontrado.");
                    return;
                }
            
                $.ajax({
                    url: window.location.pathname,
                    type: 'POST',
                    data: formData,
                    processData: false,  // Evitar que jQuery procese los datos
                    contentType: false,  // Evitar que jQuery establezca el content-type
                    headers: {
                        'X-CSRFToken': csrfToken  // Añadir token CSRF
                    },
                    success: function(data) {
                        // Si no hay error, mostrar mensaje de éxito y redirigir
                        if (!data.hasOwnProperty('error')) {
                            showConfirmationAlert('Operación exitosa',
                                'La venta se ha registrado correctamente', 
                                'success',
                                '/ventas/venta/');
                        } else {
                            // Si hay un error, mostrarlo
                            alertError(data.error); // Asegúrate de que esta función esté definida
                        }
                    },
                    fail: function(jqXHR, textStatus, errorThrown) {
                        // En caso de fallo en la solicitud AJAX
                        alert(textStatus + ':' + errorThrown);
                    }
                });
            } else {
                // Si el usuario cancela, no hace nada
                console.log('Operación cancelada por el usuario');
            }
        });
    });
    

/////////////// Proceso de Pago  ////////////////


    function actualizarSaldoRestante() {
        let total = venta.items.total;
        let montoIngresado = parseFloat($("#id_monto").val()) || 0;
        let saldoRestante = total - montoIngresado;
        
        // Asegurar que el saldo no sea negativo
        saldoRestante = Math.max(0, saldoRestante);
        
        // Actualizar el span de saldo restante
        $("#saldo-restante").text(`Efectivo Restante: $${saldoRestante.toFixed(2)}`);
    }
   
    
    $("#id_metodo_pago").on("change", function() {
        let metodoPagoSeleccionado = $(this).val();
        
        // Resetear todos los campos y pagos previos
        $("#primer_pago, #segundo-pago, #vuelto").addClass('d-none');
        venta.items.pagos = []; // Limpiar pagos anteriores
        
        // Resetear saldo restante
        $("#saldo-restante").text(`Saldo Restante: $${venta.items.total.toFixed(2)}`);
    
        if (metodoPagoSeleccionado === "EF") {
            $("#primer_pago").removeClass('d-none');
            
            $('#id_monto').off('input').on('input', function() {
                let input = $(this);
                let valorOriginal = input.val();
            
                // Eliminar cualquier carácter que no sea número
                let valorLimpio = valorOriginal.replace(/[^0-9]/g, '');
                
                // Validar que comience con número entre 1-9
                if (valorLimpio && !/^[1-9]/.test(valorLimpio)) {
                    // Si no comienza con número entre 1-9, limpiar el input
                    input.val('');
                    return;
                }
                
                // Actualizar el input con solo números
                input.val(valorLimpio);

                // Convertir a número positivo
                let monto = Math.abs(parseFloat(valorLimpio) || 0);

                if (monto > 1000000) {
                    input.val('1000000');
                    monto = 1000000;
                    Math.abs(parseFloat(monto) || 0)
                }


                let total = venta.items.total;
    
                // Actualizar saldo restante
                actualizarSaldoRestante();
    
                // Limpiar pagos anteriores antes de agregar nuevos
                venta.items.pagos = [];
    
                if (monto > total) {
                    // Caso de pago completo con vuelto
                    let vuelto = monto - total;
                    
                    $("#vuelto").removeClass('d-none');
                    $("#vuelto-efectivo").val(vuelto.toFixed(2));
                    $("#segundo-pago").addClass('d-none');
    
                    // Agregar pago único en efectivo
                    venta.addPago({
                        monto: monto,
                        metodo_pago: "EF"
                    });
                } 
                else if (monto < total) {
                    // Pago parcial con segundo método
                    let montoSegundo = total - monto;
                    
                    $("#segundo-pago").removeClass('d-none');
                    $("#vuelto").addClass('d-none');
                    $("#monto_segundo").val(montoSegundo.toFixed(2));
    
                    $("#metodo_pago_segundo").val("TD");
                    $("#metodo_pago_segundo").prop('disabled', true);
    
                    // Agregar dos pagos: efectivo y débito
                    venta.addPago({
                        monto: monto,
                        metodo_pago: "EF"
                    });
    
                    venta.addPago({
                        monto: montoSegundo,
                        metodo_pago: "TD"
                    });
                } 
                else {
                    // Pago exacto
                    $("#vuelto").addClass('d-none');
                    $("#segundo-pago").addClass('d-none');
    
                    venta.addPago({
                        monto: monto,
                        metodo_pago: "EF"
                    });
                }
                console.clear();
                console.log("Pagos actuales:", venta.items.pagos);
            });
        } 
        else {
            // Otros métodos de pago
            $("#primer_pago, #segundo-pago").addClass('d-none');
            venta.items.pagos = []; // Limpiar pagos anteriores
            $('#id_monto').val(venta.items.total);
            venta.addPago({
                monto: venta.items.total,
                metodo_pago: metodoPagoSeleccionado
            });
            console.log(venta.items);
        }
    });
    
    $("#eliminar-segundo-pago").on("click", function() {
        // Ocultar el segundo pago
        $("#segundo-pago").addClass('d-none');
        
        // Resetear el monto del segundo pago
        $("#monto_segundo").val('');
        $("#id_monto").val(''); 
        
        // Resetear saldo restante
        $("#saldo-restante").text(`Saldo Restante: $${venta.items.total.toFixed(2)}`);
        
        // Limpiar el array de pagos
        venta.items.pagos = [];
        console.clear();
        console.log(venta.items);
    });
    venta.listar();
    
});
