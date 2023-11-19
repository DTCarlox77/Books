# Functions.py es un archivo almacena funciones especiales que se utilizan en la aplicación principal.
from functools import wraps
from application import session, redirect, url_for
import os

# Comprueba si existe un ID almacenado en la sesión.
def esta_autenticado():
    return "id" in session

# Decorador de función para verificar que un usuario esté logueado.
def inicio_requerido(ruta):
    @wraps(ruta)
    
    def verificacion_autenticacion(*args, **kwargs):
        
        if not esta_autenticado():
            return redirect(url_for('login'))
        
        return ruta(*args, **kwargs)
    
    return verificacion_autenticacion

# Clave de conexión con la API de Google Books.
api_key = os.getenv("API_KEY")

# Si no hay una clave, cerrar el servidor.
if not api_key:
    raise("Recuerda asiginar la clave API de Google Books.")

# La siguiente función se encarga de extraer información específica de los objetos retornados por la API para así evitar información de más a la página.
def formatear(libros):
    libros_resultantes = []

    for elemento in libros:
        items = elemento.get('items', [])
        for libro in items:
            volume_info = libro.get('volumeInfo', {})
            
            title = volume_info.get('title', 'Título no encontrado')
            authors = volume_info.get('authors', [])
            
            # Buscamos el identificador ISBN_10 y lo extraemos
            isbn_10 = None
            for identifier in volume_info.get('industryIdentifiers', []):
                if identifier.get('type') == 'ISBN_10':
                    isbn_10 = identifier.get('identifier', 'ISBN no encontrado')
                    break
            
            categories = volume_info.get('categories', [])
            averageRating = volume_info.get('averageRating', 'No disponible')
            ratingsCount = volume_info.get('ratingsCount', 'No disponible')
            thumbnail = volume_info.get('imageLinks', {}).get('thumbnail', None)
            infoLink = volume_info.get('infoLink', 'No disponible')
            description = volume_info.get('description', 'Descripción no disponible')
            publishedDate = volume_info.get('publishedDate', 'Fecha de publicación no disponible')
            pageCount = volume_info.get('pageCount', 'Número de páginas no disponible')
            
            libro_dict = {
                'title': title,
                'authors': authors,
                'isbn': isbn_10,
                'categories': categories,
                'averageRating': averageRating,
                'ratingsCount': ratingsCount,
                'thumbnail': thumbnail,
                'infoLink': infoLink,
                'description': description,
                'publishedDate': publishedDate,
                'pageCount': pageCount
            }
            
            libros_resultantes.append(libro_dict)

    return libros_resultantes