// Sugerencias al realizar una búsqueda de libros. (No es precisa).

document.addEventListener("DOMContentLoaded", function(){
    const inputNombre = document.getElementById("nombre");
    const sugerencias = document.getElementById("sugerencias");
    
    inputNombre.addEventListener("input", () => {
        const busqueda = inputNombre.value.trim();
        if (busqueda.length > 0) {
            // La siguiente API no necesita de una clave para su uso.
            fetch(`https://www.googleapis.com/books/v1/volumes?q=${busqueda}`)
                .then(response => response.json())
                .then(data => {
                    sugerencias.innerHTML = "";
    
                    if (data.items) {
                        data.items.forEach(libro => {
                            const sugerencia = document.createElement("div");
                            sugerencia.textContent = libro.volumeInfo.title;
                            sugerencia.addEventListener("click", () => {
                                inputNombre.value = libro.volumeInfo.title;
                                sugerencias.innerHTML = "";
                                realizarBusqueda();
                            });
                            sugerencias.appendChild(sugerencia);
                        });
                    }
                })
                .catch(error => {
                    console.error("Error al obtener sugerencias:", error);
                });
        } else {
            sugerencias.innerHTML = "";
        }
    });
    
    document.addEventListener("click", (event) => {
        if (!sugerencias.contains(event.target)) {
            sugerencias.innerHTML = "";
        }
    });
    
    function realizarBusqueda() {
        const formulario = document.querySelector("form");
        formulario.submit();
    }
})