// home/static/home/script.js

document.addEventListener("DOMContentLoaded", function() {
    const dropdownToggle = document.querySelector('.dropdown-toggle');
    const dropdownMenu = document.querySelector('.dropdown');

    dropdownToggle.addEventListener('click', function(e) {
        e.preventDefault(); // Evita el comportamiento predeterminado del enlace
        dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
    });
});
