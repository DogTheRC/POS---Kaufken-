
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

    $('#table').DataTable({
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
            { data: "codigo_barra" },
            { data: "autor_nombre" },
            { data: "nombre" },
            { data: "precio" },
            { data: "stock" },
            { data: "marca_nombre" },
            { data: "categoria_nombre" },
            { 
                data: "imagen", 
                render: function(data) {
                    // Si la imagen existe, la mostramos; si no, mostramos un mensaje alternativo
                    return data ? `<img src="${data}" alt="Imagen" style="width: 50px; height: auto;">` : 'No disponible';
                }
            },
            { 
                data: null, 
                render: function(data, type, row) {
                    // Construir las URLs de edición y eliminación
                    var editUrl = baseUrl + 'editar/' + row.codigo_barra + '/';
                    var deleteUrl = baseUrl + 'delete/' + row.codigo_barra + '/';

                    var buttons = '<a href="' + editUrl + '" class="buttom_editar"><i class="fas fa-edit"></i> Editar</a> ';
                    buttons += '<a href="' + deleteUrl + '" class="buttom_eliminar"><i class="fas fa-trash-alt"></i> Eliminar</a>';
                    
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
});
