
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

function alert_confirm(title, content, callback){
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                   callback() 
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    });
}

function showConfirmationAlert(title, text, icon, url) {
    Swal.fire({
        title: title,
        text: text,
        icon: icon,
        confirmButtonText: 'Aceptar'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = url;
        }
    });
}
function mostrarConfirmacionVenta() {
    return Swal.fire({
        title: '¿Estás seguro?',
        text: "¿Deseas registrar esta venta?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, continuar',
        cancelButtonText: 'No, cancelar'
    });
}
