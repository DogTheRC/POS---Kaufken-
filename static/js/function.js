function alertError(obj) {
    var html = '';

    if (typeof (obj) === 'object') {
        $.each(obj, function(key, value) {
            html += '<p class="error-message">' + key + ':' + value + '</p>';
        });
    } else {
        html = '<p class="error-message">' + obj + '</p>';
    }
   
    Swal.fire({
        icon: 'error',
        title: 'Ha ocurrido un error',
        html: html, // Usamos 'html' para permitir el formato HTML
        confirmButtonText: 'Aceptar'
    });
}