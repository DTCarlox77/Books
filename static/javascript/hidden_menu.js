// Menú hamburguesa de la aplicación.

document.addEventListener("DOMContentLoaded", function() {
    const menu = document.getElementById("hidden-HM-menu");
    const boton_cambio_mostrado = document.getElementById("H-menu");
    const boton_cambio_oculto = document.getElementById("H-menu-hidden");

    boton_cambio_mostrado.addEventListener("click", function() {
        menu.classList.remove("menu-oculto");
        menu.classList.add("menu-mostrado");
    });

    boton_cambio_oculto.addEventListener("click", function() {
        menu.classList.remove("menu-mostrado");
        menu.classList.add("menu-oculto");
    });
});  