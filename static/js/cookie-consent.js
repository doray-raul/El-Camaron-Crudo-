document.addEventListener('DOMContentLoaded', function() {
    // Verificar si ya se aceptaron las cookies
    if (!localStorage.getItem('cookiesAccepted') && !localStorage.getItem('cookiesRejected')) {
        document.getElementById('cookieBanner').style.display = 'flex';
    }

    document.getElementById('acceptCookies').addEventListener('click', function() {
        localStorage.setItem('cookiesAccepted', 'true');
        document.getElementById('cookieBanner').style.display = 'none';
    });

    document.getElementById('rejectCookies').addEventListener('click', function() {
        localStorage.setItem('cookiesRejected', 'true');
        document.getElementById('cookieBanner').style.display = 'none';
    });
});