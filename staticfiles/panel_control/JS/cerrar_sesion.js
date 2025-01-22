document.addEventListener('DOMContentLoaded', () => {
    const logoutButton = document.querySelector('.btn-logout');
    if (logoutButton) {
        logoutButton.addEventListener('click', (event) => {
            const confirmLogout = confirm('¿Estás seguro de que deseas cerrar sesión?');
            if (!confirmLogout) {
                // Evitar que el formulario se envíe si el usuario cancela
                event.preventDefault();
            }
        });
    }
});

///mendigo django no me deja sacar la ruta mejor uso el atributo script