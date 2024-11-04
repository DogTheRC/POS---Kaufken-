//save guardar/actualizar
document.body.addEventListener('htmx:afterRequest', function(event) {
    const detail = event.detail;
    if (detail.xhr && detail.xhr.getResponseHeader('HX-Trigger')) {
        const response = JSON.parse(detail.xhr.getResponseHeader('HX-Trigger'));
        if (response.showMessage) {
            Swal.fire({
                position: "center",
                icon: "success",
                title: response.showMessage,  // Usa el mensaje del servidor
                showConfirmButton: false,
                timer: 1500
            });
        }
    }
});

function removerProducto(id) {
    const productoId = id;
    const modal = document.querySelector('.modal');
    const modalInstance = bootstrap.Modal.getInstance(modal);
    modalInstance.hide();
    console.log(`Eliminando producto con ID: ${productoId}`);
    Swal.fire({
        title: "¿Estás seguro?",
        text: "¡No podrás revertir esto!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, ¡bórralo!"
    }).then((result) => {
        if (result.isConfirmed) {
            // Realizar la solicitud de eliminación
            fetch(`/productos/eliminarProducto/${productoId}/`, {  // ruta definida en urls.py
                method: 'GET', // Usa DELETE o POST según tu configuración
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}', // Asegúrate de incluir el token CSRF
                    'HX-Request': 'true' // Indica que es una solicitud HTMX
                }
            })
            .then(response => {
                if (response.ok) {
                Swal.fire({
                    title: "¡Eliminado!",
                    text: "Tu producto ha sido removido.",
                    icon: "success"
                }).then(() => {
                    window.location.reload(); // Recargar la página
                    });
                } else {
                    throw new Error('Error en la eliminación'); // Manejo de errores
                }
            })
            .catch(error => {
                Swal.fire({
                    title: "Error",
                    text: "No se pudo eliminar el producto.",
                    icon: "error"
                });
            });
        }
    });
}