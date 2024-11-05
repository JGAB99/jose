document.addEventListener('DOMContentLoaded', function() {
    // Animación para la barra de progreso
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        const targetWidth = progressBar.getAttribute('aria-valuenow') + '%';
        progressBar.style.width = '0%';
        setTimeout(() => {
            progressBar.style.transition = 'width 1s ease-in-out';
            progressBar.style.width = targetWidth;
        }, 100);
    }

    // Tooltip para los logros
    const achievementIcons = document.querySelectorAll('.achievement-icon');
    achievementIcons.forEach(icon => {
        new bootstrap.Tooltip(icon);
    });
});