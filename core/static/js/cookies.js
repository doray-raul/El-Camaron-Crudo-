document.addEventListener('DOMContentLoaded', function() {
    // Verificar si ya existe la cookie de aceptación
    if (getCookie('cookies_aceptadas') === 'true') {
        // Si ya aceptó, ocultar el banner
        ocultarBanner();
    } else if (getCookie('cookies_aceptadas') === 'false') {
        // Si rechazó, también ocultamos el banner
        ocultarBanner();
    } else {
        // No ha decidido, mostrar el banner
        mostrarBanner();
    }
});

/**
 * Muestra el banner de cookies.
 */
function mostrarBanner() {
    var banner = document.getElementById('cookieBanner');
    if (banner) {
        banner.style.display = 'block';
    }
}

/**
 * Oculta el banner de cookies.
 */
function ocultarBanner() {
    var banner = document.getElementById('cookieBanner');
    if (banner) {
        banner.style.display = 'none';
    }
}

/**
 * Función para aceptar cookies.
 * Oculta el banner y guarda la preferencia por 1 año.
 */
function aceptarCookies() {
    document.cookie = "cookies_aceptadas=true; max-age=31536000; path=/";
    ocultarBanner();
    // Aquí puedes añadir lógica adicional, como cargar scripts de analytics
    console.log('Cookies aceptadas');
}

/**
 * Función para rechazar cookies.
 * Oculta el banner y guarda la preferencia por 1 año.
 */
function rechazarCookies() {
    document.cookie = "cookies_aceptadas=false; max-age=31536000; path=/";
    ocultarBanner();
    // Opcional: desactivar scripts que usen cookies
    console.log('Cookies rechazadas');
}

/**
 * Función auxiliar para leer el valor de una cookie por su nombre.
 * @param {string} name - Nombre de la cookie.
 * @returns {string|null} - Valor de la cookie o null si no existe.
 */
function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length === 2) {
        return parts.pop().split(";").shift();
    }
    return null;
}