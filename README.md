# Project 1: Books

¡Bienvenido a Books App! A continuación, encontrarás una descripción general del proyecto, una lista de los archivos incluidos y las instrucciones para ejecutar la aplicación en tu entorno local.

## Descripción del Proyecto

Books App es una plataforma que te permite buscar libros, obtener detalles sobre ellos y dejar reseñas con calificaciones. Puedes buscar libros por título, autor o ISBN, y la aplicación te proporcionará información detallada sobre cada libro, incluyendo su portada, calificaciones promedio y reseñas de otros usuarios. Además, recibirás recomendaciones aleatorias de libros cuando te encuentres en la pestaña principal. Para comenzar a utilizar la aplicación, puedes registrarte como usuario y, una vez dentro, podrás dejar tus propias reseñas y explorar libros de tu interés.

## Video tutorial

   **Youtube**: https://youtu.be/es2CdR8Ud64?si=uVSd_oEVmdQbdVP-

## Archivos en el Proyecto

- **application.py**: Este archivo contiene el corazón de la aplicación Flask, con las rutas y funciones para manejar la funcionalidad de la aplicación web.

- **create.py**: Con este archivo, puedes crear las tablas necesarias en tu base de datos para el correcto funcionamiento de la aplicación.

- **database.py**: Aquí encontrarás todas las funciones relacionadas con el CRUD de la base de datos.

- **functions.py**: En este archivo se encuentran funciones auxiliares que respaldan diversas funcionalidades de la aplicación, como la validación de usuarios, el formateo de resultados de la API de Google Books y la autenticación del usuario.

- **import_books.py**: Este script te permitirá cargar los libros desde el archivo books.csv a la base de datos PostgreSQL.

- **templates/**: Esta carpeta contiene archivos HTML que definen la estructura y apariencia de las páginas web de la aplicación. En adición, también se encuentra el Javascript de las plantillas HTML.

- **static/**: Aquí encontrarás archivos estáticos como hojas de estilo CSS, fuentes y otros recursos utilizados en las plantillas HTML.

- **.env.txt**: Un archivo de ejemplo que muestra cómo deben configurarse las variables de entorno, como la URL de la base de datos y la clave de API de Google Books.

- **books.csv**: Son los libros que deben contener la base de datos; este mismo fue otorgado en la documentación que define cómo realizar este proyecto.

- **querys.sql**: En este archivo SQL se encuentran las consultas para la creación de las tablas que la aplicación requiere para su funcionamiento.

## Ejecución de la Aplicación

1. Asegúrate de tener Python 3.11 instalado en tu sistema.

2. Instala las dependencias de Python utilizando el siguiente comando:

   ```
   pip install -r requirements.txt
   ```

3. Crea una base de datos PostgreSQL y configura la URL de la base de datos en el archivo `.env.txt` con las credenciales necesarias.

   ```
   export DATABASE_URL="URL de tu base de datos PostgreSQL."
   ```

4. Renombra el archivo `.env.txt` a `.env` y configura la clave de la API de Google Books.

   ```
   export API_KEY="Tu clave API de Google Books."
   ```

5. Al final tu archivo `.env` debe tener la siguiente estructura:

   ```
   export DATABASE_URL="URL de tu base de datos PostgreSQL."
   export FLASK_APP=application.py
   export FLASK_DEBUG=1

   export API_KEY="Tu clave API de Google Books."
   export API_URL=https://www.googleapis.com/books/v1/mylibrary/bookshelves/0/clearVolumes
   ```

6. Cuando hayas finalizado los pasos anteriores, ejecuta el archivo Python llamado `create.py`, este se encargará de crear las tablas con sus campos necesarios en tu base de datos. 

   ```
   python create.py
   ```

7. La base de datos necesitará de los libros otorgados en el archivo `books.csv`, por lo tanto, ahora ejecuta el script `import.py` y espera a que todos los libros sean subidos a la base de datos.

   ```
   python import.py
   ```

8. Ejecuta la aplicación de Flask con el siguiente comando:
   ```
   flask run
   ```

9. Abre tu navegador web y accede a `http://localhost:5000` para comenzar a usar la aplicación.

10. Regístrate en el apartado `/sign_in` y luego inicia sesión en `/login` y disfruta de la aplicación.

## Notas Adicionales

- Asegúrate de tener los archivos de la aplicación con la siguiente jerarquía:
   ```
   application.py
   create.py
   database.py
   functions.py
   import.py
   books.csv
   querys.sql
   .env
   .gitignore

   - static
      - css
      - fuentes
      - icons
      - vectores
   
   - templates
   ```

- Recuerda realizar las ejecuciones de la consola desde la carpeta en donde se encuentra el application.py.

- La aplicación incluye autenticación de usuarios, por lo que los usuarios deben registrarse e iniciar sesión para acceder y poder postear reseñas.

- La funcionalidad de búsqueda utiliza la API de Google Books para obtener información detallada de los libros.

- La aplicación proporciona estadísticas sobre reseñas de libros y recomendaciones aleatorias para los usuarios.

- Las sugerencias de la barra de búsqueda no son precisas debido a que la API (Google Books) para este apartado no cuenta con un filtro de restricción que permita mostrar únicamente los libros que pertenecen a la base de datos.

- Puede que te encuentres con libros que, al intentar reseñarlos, generen un error 404. Esto se debe a que no forman parte de la base de datos. La razón por la cual aparecen se debe a un simple error en el filtro que no limita los resultados a libros que estén exclusivamente en la base de datos no tiene una precisión del 100%. El problema al diseñar un método con una precisión del 100% es el tiempo de carga, que de por sí ya es lento.

¡Espero que disfrutes utilizando la aplicación de reseñas de libros! Si tienes alguna pregunta o necesitas más información, no dudes en contactarme.

## Obtención de información a través de la API.

`/api/<isbn>`
- Devuelve un archivo JSON el cual contiene el título, autor, fecha de publicación, número ISBN, total de reseñas y su puntuación promedio de Google Books.

### Ejemplo
`GET` request: `api/<isbn>`

Resultado:
```JSON
{
  "author": "Ben Aaronovitch",
  "average_score": "N/A",
  "isbn": "0345524616",
  "review_count": "N/A",
  "tittle": "Whispers Under Ground",
  "year": 2012
}
```

## Hecho por: Carlos Adrián Espinosa Luna.