
$(function() {
    // Función para obtener el token CSRF
    function getCSRFToken() {
        return $('meta[name="csrf-token"]').attr('content');
    }

    // Configurar AJAX para incluir el token CSRF en los encabezados
    $.ajaxSetup({
        headers: {
            'X-CSRFToken': getCSRFToken()  // Incluir el token CSRF en el encabezado
        }
    });

    // Obtener la URL base para editar y eliminar
    var baseUrl = window.location.pathname.replace('inventario/', '');  // Elimina la parte 'inventario' para tener la URL base

    var table = $('#table').DataTable({
        responsive: true,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,  // URL actual de la página
            type: 'POST',
            data: {
                'action': 'search'  // Pasar la acción 'search' para que el servidor lo reconozca
            },
            dataSrc: "",  // Los datos son una lista directa (no hay envoltorio adicional)
            error: function(xhr, error, code) {
                console.error('Error en la carga de datos:', error);
                alert('Hubo un error cargando los datos.');
            }
        },
        columns: [
            { className: 'dt-control', orderable: false, data: null, defaultContent: '' },
            { data: "id" },
            { data: "usuario_nombre" },
            { data: "create_at" },
            {
                data: "total",
                render: function(data, type, row) {
                    var total = parseFloat(data);
                    return '$' + total.toString().replace(/\d(?=(\d{3})+\.)/g, '$&,');
                }
            },
            { 
                data: null, 
                render: function(data, type, row) {
                    // Construir las URLs de edición y eliminación
                    var deleteUrl = baseUrl + 'delete/' + row.id + '/';
                    buttons ='<a href="' + deleteUrl + '" class="buttom_eliminar"><i class="fas fa-trash-alt"></i> Eliminar</a>';        
                    return buttons;
                }
            }
        ],
        columnDefs: [
            {
                targets: [-1],  // Columna de acciones
                class: 'text-center',
            }
        ],
        initComplete: function(settings, json) {
            console.log('Tabla cargada con éxito.');
        }
    });
    $('#table tbody').on('click', 'td.dt-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);  // Ahora table.row debería funcionar correctamente

        if (row.child.isShown()) {
            row.child.hide();
        } else {
            // Mostrar los detalles de la venta
            row.child(format(row.data().detalles, row.data().pagos)).show();
        }
    });

    // Función para formatear los datos de la fila (esto es un ejemplo)
    function format(detalles, pagos) {
        var detalleHtml = '<table class="detalle-tabla"><thead><tr><th class="detalle-campo">Producto</th><th class="detalle-campo">Cantidad</th><th class="detalle-campo">Precio Unitario</th><th class="detalle-campo">Subtotal</th></tr></thead><tbody>';
        detalles.forEach(function(detalle) {
            detalleHtml += `
                <tr>
                    <td class="detalle-valor">${detalle.producto_nombre}</td>
                    <td class="detalle-valor">${detalle.cantidad}</td>
                    <td class="detalle-valor">$${detalle.precio_unitario}</td>
                    <td class="detalle-valor">$${detalle.subtotal}</td>
                </tr>
            `;
        });
        detalleHtml += '</tbody></table>';

        // Agregar los pagos en la tabla expandida
        detalleHtml += '<table class="detalle-tabla"><thead><tr><th class="detalle-campo">Método de Pago</th><th class="detalle-campo">Monto</th><th class="detalle-campo">Fecha</th></tr></thead><tbody>';
        pagos.forEach(function(pago) {
            detalleHtml += `
                <tr>
                    <td class="detalle-valor">${pago.metodo_pago}</td>
                    <td class="detalle-valor">$${parseFloat(pago.monto)}</td>
                    <td class="detalle-valor">${pago.fecha_pago}</td>
                </tr>
            `;
        });
        detalleHtml += '</tbody></table>';

        return detalleHtml;
    }
});
