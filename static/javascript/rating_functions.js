/* Permite la realización del gráfico en función de las opiniones en el apartado de libros, también otorga las funciones que
permiten realizar calificaciones de libros de manera dinámica. */

document.addEventListener("DOMContentLoaded", function(){

    const stars = document.querySelectorAll('.star');
    const result = document.getElementById('rating');
    const ratingInput = document.getElementById('rating_input');
    const initialRating = parseInt(document.getElementById('rating').textContent);

    let rating = initialRating;

    stars.forEach(star => {
        star.addEventListener('click', () => {
            const clickedRating = parseInt(star.getAttribute('data-rating'));
            rating = clickedRating;
            updateRating();
            updateStars();
        });
    
        star.addEventListener('mouseover', () => {
            const hoveredRating = parseInt(star.getAttribute('data-rating'));
            highlightStars(hoveredRating);
        });
    
        star.addEventListener('mouseout', () => {
            highlightStars(rating);
        });
    });
    
    result.addEventListener('input', () => {
        const newRating = parseInt(result.textContent);
        if (newRating >= 1 && newRating <= 5) {
            rating = newRating;
            updateStars();
        }
    });
    
    function updateRating() {
        result.textContent = rating;
        ratingInput.value = rating;
    }
    
    function highlightStars(num) {
        stars.forEach(star => {
            const starRating = parseInt(star.getAttribute('data-rating'));
            if (starRating <= num) {
                star.classList.add('active');
            } else {
                star.classList.remove('active');
            }
        });
    }
    
    function updateStars() {
        stars.forEach(star => {
            const starRating = parseInt(star.getAttribute('data-rating'));
            if (starRating <= rating) {
                star.classList.add('active');
            } else {
                star.classList.remove('active');
            }
        });
    }
    
    function initializeStars() {
        stars.forEach(star => {
            const starRating = parseInt(star.getAttribute('data-rating'));
            if (starRating <= initialRating) {
                star.classList.add('active');
            } else {
                star.classList.remove('active');
            }
        });
    }
    
    initializeStars();
    
    const stars_h = document.querySelectorAll(".star");
    const ratingDisplay = document.getElementById("rating");
    
    stars_h.forEach(star => {
        star.addEventListener("click", function () {
            const rating = this.getAttribute("data-rating");
            ratingInput.value = rating;
            ratingDisplay.innerText = rating;
        });
    });
    
    console.log(ratingInput);
    
    // Creación de la gráfica de reseñas.
    const elementosEstrellas = document.querySelectorAll('h1[class^="estrella-"]');
    const opinionesPorEstrella = [];
    
    elementosEstrellas.forEach(elemento => {
        const votaciones = parseInt(elemento.textContent);
        opinionesPorEstrella.push(votaciones);
    });
    
    // Cálculo del total de opiniones.
    const totalOpiniones = opinionesPorEstrella.reduce((total, cantidad) => total + cantidad, 0);
    
    // Elemento HTML para mostrar el total de opiniones.
    const totalOpinionesElement = document.createElement('div');
    
    // Contenedor HTML para las barras de calificación.
    const contenedorBarras = document.createElement('div');
    contenedorBarras.className = 'bar-container';
    
    // Creación de las barras de calificación dinámicamente.
    for (let i = 0; i < opinionesPorEstrella.length; i++) {
        const barContainer = document.createElement('div');
        barContainer.className = 'bar-container';
    
        const starElement = document.createElement('div');
        starElement.className = 'star-total';
    
        const barElement = document.createElement('div');
        barElement.className = 'bar';
        const filledBarElement = document.createElement('div');
        filledBarElement.className = 'filled-bar';
    
        const calificacion = i + 1;
        const porcentaje = (opinionesPorEstrella[i] / totalOpiniones) * 100;
        filledBarElement.style.width = `${porcentaje}%`;
        barElement.appendChild(filledBarElement);
    
        const calificacionElement = document.createElement('div');
        calificacionElement.className = 'Numeros-totales';
        calificacionElement.textContent = `${opinionesPorEstrella[i]} Opiniones`;
    
        barContainer.appendChild(starElement);
        barContainer.appendChild(barElement);
        barContainer.appendChild(calificacionElement);
    
        contenedorBarras.appendChild(barContainer);
    }
    
    // Obtención del contenedor dedicado a las reseñas,
    const informacionRattingContainer = document.querySelector('.informacion_ratting');
    
    // Anexar la información al contenedor de las reseñas.
    informacionRattingContainer.appendChild(totalOpinionesElement);
    informacionRattingContainer.appendChild(contenedorBarras);
})