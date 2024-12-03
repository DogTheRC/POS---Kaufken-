
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
        scrollX: true,
        ajax: {
            url: window.location.pathname,  
            type: 'POST',
            data: {
                'action': 'search'  
            },
            dataSrc: "", 
            error: function(xhr, error, code) {
                console.error('Error en la carga de datos:', error);
                alert('Hubo un error cargando los datos.');
            }
        },
        columns: [
            { className: 'dt-control', orderable: false, data: null, defaultContent: '' },
            { data: "codigo_barra" },
            { data: "autor_nombre" },
            { data: "nombre" },
            {
                data: "precio",
                render: function(data, type, row) {
                    var precio = parseFloat(data);
                    return '$' + precio.toString().replace(/\d(?=(\d{3})+\.)/g, '$&,');
                }
            },
            { data: "stock" },
            { data: "marca_nombre" },
            { data: "categoria_nombre" },
            {
                data: "imagen",
                render: function(data) {
                    return data ? `<img src="${data}" alt="Imagen" style="width: 50px; height: auto;">` : 'No disponible';
                }
            },
            { data: "is_active" },
            {
                data: null,
                render: function(data, type, row) {
                    var editUrl = baseUrl + 'editar/' + row.codigo_barra + '/';
                    var deleteUrl = baseUrl + 'delete/' + row.codigo_barra + '/';
                    var buttons = '<a href="' + editUrl + '" class="buttom_editar"><i class="fas fa-edit"></i> Editar</a> ';
                    buttons += '<a href="' + deleteUrl + '" class="buttom_eliminar"><i class="fas fa-trash-alt"></i> Eliminar</a>';
                    return buttons;
                }
            }
        ],
        initComplete: function(settings, json) {
            console.log('Tabla cargada con éxito.');
            console.log(table);  // Imprimir table en consola para verificar que es un objeto DataTable
        }
    });

    console.log(table);  

    $('#table tbody').on('click', 'td.dt-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);  // Ahora table.row debería funcionar correctamente

        if (row.child.isShown()) {
            row.child.hide();
        } else {
            row.child(format(row.data())).show();
        }
    });

    // Función para formatear los datos de la fila (esto es un ejemplo)
    function format(d) {
        return `
            <table class="detalle-tabla">
                <thead>
                    <tr>
                        <th class="detalle-campo">Nombre</th>
                        <th class="detalle-campo">Fecha de Vencimiento</th>
                        <th class="detalle-campo">Stock Crítico</th>
                        <th class="detalle-campo">Stock Mínimo</th>
                        <th class="detalle-campo">Descripción</th>
                        <th class="detalle-campo">Fecha de Creación</th>
                        <th class="detalle-campo">Fecha de Actualización</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="detalle-valor">${d.nombre}</td>
                        <td class="detalle-valor">${d.fecha_vencimiento}</td>
                        <td class="detalle-valor">${d.stock_critico}</td>
                        <td class="detalle-valor">${d.stock_minimo}</td>
                        <td class="detalle-valor">${d.descripcion}</td>
                        <td class="detalle-valor">${d.created_at}</td>
                        <td class="detalle-valor">${d.update_at}</td>
                    </tr>
                </tbody>
            </table>
        `;
    }
    
    

});
