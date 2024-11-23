$(document).ready(function () {
    // Función para obtener el token CSRF
    function getCSRFToken() {
        return $('meta[name="csrf-token"]').attr('content');
    }

    // Configuración global de AJAX para incluir el CSRF token en los encabezados
    $.ajaxSetup({
        headers: {
            'X-CSRFToken': getCSRFToken()  // Incluir el token CSRF en el encabezado de cada solicitud
        }
    });

    // Función para cargar las notificaciones no leídas
    function cargarNotificaciones() {
        $.ajax({
            url: window.location.pathname,  // La URL de la vista actual
            type: 'POST',
            data: { action: 'search' },  // Acción para buscar las notificaciones
            dataType: 'JSON',
            success: function (data) {
                if (!data.hasOwnProperty('error')) {
                    // Si no hay error, generar HTML con las notificaciones
                    let html = '';
                    data.forEach(notificacion => {
                        html += `
                            <div class="notificacion ${notificacion.leido ? 'leida' : 'no-leida'}" data-id="${notificacion.id}">
                                <h3>${notificacion.titulo}</h3>
                                
                                <!-- Icono y descripción para la notificación -->
                                <p class="stock-status">
                                    <i class="icono fa fa-calendar"></i> 
                                    ${notificacion.created_at}
                                </p>
                                <p class="stock-status">
                                    <i class="icono fa fa-ban"></i> 
                                    ${notificacion.descripcion}
                                </p>
                                
                                <!-- Icono y descripción para el stock del producto -->
                                <p class="stock-status">
                                    <i class="icono fa fa-exclamation-triangle"></i> 
                                    Stock del Producto (${notificacion.producto_nombre}): ${notificacion.producto_stock}
                                </p>

                                <!-- Icono y descripción para el nombre del producto -->
                                <p class="stock-status">
                                    <i class="icono fa fa-arrow-down"></i> 
                                    Producto: ${notificacion.producto_nombre}
                                </p>

                                <button class="btn-marcar-leida" data-id="${notificacion.id}">
                                    <i class="fa fa-check"></i> Marcar como leída
                                </button>
                            </div>
                        `;
                    });
                    $('#notificaciones-list').html(html);  // Actualiza el contenedor con las notificaciones
                } else {
                    console.error(data.error);
                    alert(data.error);
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.error(`${textStatus}: ${errorThrown}`);
            }
        });
    }

    // Evento para marcar una notificación como leída
    $('#notificaciones-list').on('click', '.btn-marcar-leida', function () {
        const notificacionId = $(this).data('id');  // Obtener el ID de la notificación
        $.ajax({
            url: window.location.pathname,  // La misma URL que en el método 'search'
            type: 'POST',
            data: {
                action: 'mark_as_read',
                id: notificacionId
            },
            dataType: 'JSON',
            success: function (response) {
                if (!response.hasOwnProperty('error')) {
                    // Si no hay error, actualizamos la notificación en la UI
                    $(`.notificacion[data-id="${notificacionId}"]`).removeClass('no-leida').addClass('leida');
                    alert('Notificación marcada como leída');
                    
                    // Recargar las notificaciones que aún están no leídas
                    cargarNotificaciones();
                } else {
                    console.error(response.error);
                    alert(response.error);
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.error(`${textStatus}: ${errorThrown}`);
            }
        });
    });

    // Llamamos a cargarNotificaciones cuando la página se carga para obtener las notificaciones no leídas
    cargarNotificaciones();
});
