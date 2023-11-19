# Creado por: Carlos Adrián Espinosa Luna / Grupo K.
from flask import Flask, session, render_template, redirect, request, session, url_for, jsonify, abort
from flask_session import Session
import requests

# Funciones que operan la base de datos y otorgan mejoras a la aplicación. (Módulo personalizado)
from database import *
from functions import *

# Inicialización del servidor de Flask.
app = Flask(__name__, static_url_path='/static')

# El login será permanente a menos que se cierre sesión.
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Decorador de función para verificar que un usuario esté logueado.
def inicio_requerido(ruta):
    @wraps(ruta)
    
    def verificacion_autenticacion(*args, **kwargs):
        
        if not esta_autenticado():
            return redirect(url_for('login'))
        
        return ruta(*args, **kwargs)
    
    return verificacion_autenticacion

@app.route("/")
def main():
    
    try:
        datos_usuario = obtener_datos_usuario(session["id"])
        return render_template("main.html", datos_usuario = datos_usuario)
    
    except:
        return render_template("main.html")
    # Esta es una página estática.

# Ruta que muestra las credenciales del usuario en la sesión y sus reseñas. Permite el cambio de contraseña y eliminación de cuenta.
@app.route("/profile")
@inicio_requerido
def profile():
    
    datos_usuario = obtener_datos_usuario(session["id"])
    reviews = obtener_reviews(session["id"])
    
    return render_template("contact.html", datos_usuario = datos_usuario, reviews = reviews, menu = 1)

# Información y agradecimiento del desarrollador.
@app.route("/contact")
def contact():
    
    try:
        datos_usuario = obtener_datos_usuario(session["id"])
        return render_template("contact.html", datos_usuario = datos_usuario)
    
    except:
        return render_template("contact.html", menu = 2)
    # Esta es una página estática.

# Si me da tiempo agregaré que sea necesario el ingreso de una contraseña antes de hacer esto.
@app.route("/delete_account", methods = ["GET", "POST"])
@inicio_requerido
def delete_account():
    
    datos_usuario = obtener_datos_usuario(session["id"])
    username = datos_usuario[1]
    
    if request.method == "POST":
        
        password = request.form["password"]
        
        # Validación de la contraseña ingresada por el usuario.
        if not inicio_de_sesión(username, password):
                
            mensaje = "La contraseña ingresada es incorrecta."
            return render_template("tools.html", mensaje = mensaje, menu = 1, datos_usuario = datos_usuario)
        
        else:
            
            if eliminar_usuario(session["id"]):
                
                # Cierra la sesión al momento de eliminar todo acerca del usuario.
                return redirect("/close")
            
            mensaje = "Algo salió mal, intenta más tarde."
            return render_template("tools.html", mensaje = mensaje, menu = 1, datos_usuario = datos_usuario)
        
    return render_template("tools.html", datos_usuario = datos_usuario)

# Permitir el cambio de imagen de perfil a un usuario.
@app.route("/profile_image", methods = ["GET", "POST"])
@inicio_requerido
def profile_image():
    
    datos_usuario = obtener_datos_usuario(session["id"])
    
    if request.method == "POST":
        
        image = request.form["image"]
        
        if change_image(session["id"], image):
            
            return redirect("/profile")
        
        mensaje = "Algo salió mal, intenta más tarde."
        return render_template("tools.html", mensaje = mensaje, menu = 2, datos_usuario = datos_usuario)
    
    return render_template("tools.html", menu = 2, datos_usuario = datos_usuario)

# Permitir el cambio de contraseña al usuario.
@app.route("/change_password", methods = ["GET", "POST"])
@inicio_requerido
def change_pass():
    
    datos_usuario = obtener_datos_usuario(session["id"])
    username = datos_usuario[1]
    
    if request.method == "POST":
        
        old_password = request.form["old_password"]
        new_password = request.form["new_password"]
        
        # La contraseña no debería ser tan corta.
        if len(new_password) < 5:
            
            mensaje = "Tu nueva contraseña es demasiado corta."
            return render_template("tools.html", mensaje = mensaje, menu = 3, datos_usuario = datos_usuario)
        
        # Validación de la contraseña ingresada por el usuario.
        if not inicio_de_sesión(username, old_password):
                
            mensaje = "La contraseña ingresada es incorrecta."
            return render_template("tools.html", mensaje = mensaje, menu = 3, datos_usuario = datos_usuario)
        
        else:
            
            if change_password(session["id"], old_password, new_password):
                
                # Cierra la sesión al momento de eliminar todo acerca del usuario.
                return redirect("/profile")
            
            mensaje = "Error, no se pudo cambiar la contraseña."
            return render_template("tools.html", mensaje = mensaje, menu = 3, datos_usuario = datos_usuario)
        
    return render_template("tools.html", menu = 3, datos_usuario = datos_usuario)

# Interfaz principal de la aplicación, permite la búsqueda de libros.
@app.route("/dashboard", methods = ["GET", "POST"])
@inicio_requerido
def dashboard():
    
    datos_usuario = obtener_datos_usuario(session["id"])

    if request.method == "POST":
        
        # La solicitud es capaz de buscar libros que coincidan con la búsqueda del usuario.
        datos_libro = request.form["nombre"]
        
        # Validación que evita las búsquedas vacías.
        if datos_libro == " " or datos_libro == "":
            mensaje = "Recuerda ingresar información para buscar algún libro."
            return render_template("dashboard.html", mensaje = mensaje, datos_usuario = datos_usuario)
        
        # La lista almacenará los libros encontrados en la base de datos.
        libros_encontrados = obtener_libros_busqueda(datos_libro)
        
        # La lista almacenará la información de los libros obtenidos por la API.
        libros = []
        
        # El bucle se encarga de tomar el isbn de los libros encontrados y buscar la información adicional de estos con la ayuda de la API.
        for libro in libros_encontrados:

            # Los libros estarán en la lista con un formato JSON.
            try:
                
                consulta = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{libro[1]}&key={api_key}")
                respuesta = consulta.json()
                
                libros.append(respuesta)
                
            # En caso de obtener un error en la búsqueda, se generará una excepción.
            except Exception as e:
                
                print(f"Algo salió mal: {e}")
                
        # Mejora del formato en el cual se enviarán los libros a la página.
        libros = formatear(libros)
        
        # Verificar si se encontraron resultados.
        if len(libros) < 1:
            mensaje = "No se encontraron coincidencias."
            return render_template("dashboard.html", mensaje = mensaje, datos_usuario = datos_usuario)
        
        # Envio de la información a la página.
        mensaje = "Resultados de búsqueda:"
        return render_template("dashboard.html", libros = libros, mensaje = mensaje, datos_usuario = datos_usuario)
    
    # Generación de recomendaciones de libros para el usuario.
    libros_encontrados = sugerencias()
    libros = []
    mensaje = "Sugerencias"
    
    for libro in libros_encontrados:

        consulta = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{libro[1]}&key={api_key}")
        respuesta = consulta.json()
                
        libros.append(respuesta)
    
    libros = formatear(libros)
            
    return render_template("/dashboard.html", libros = libros, mensaje = mensaje, datos_usuario = datos_usuario)

# Página de inicio de sesión: Solicita un usuario y una contraseña.
@app.route("/login", methods = ["GET", "POST"])
def login():
    
    # Un logueado no debería poder estar en esta sección.
    if esta_autenticado():
        return redirect("/dashboard")
    
    # Solicitud de las credenciales.
    if request.method == "POST":
        
        username = request.form["username"]
        password = request.form["password"]
        
        # Ningún campo debe quedar vacío.
        if not username or not password:
            
            mensaje = "Debes completar todos los campos para acceder."
            return render_template("login.html", mensaje = mensaje)

        # Aprobación de las credenciales.
        if not verificar_usuario_existente(username):
            
            mensaje = "El usuario ingresado no existe."
            return render_template("login.html", mensaje = mensaje)
        
        # Conceder o negar acceso.
        else:
            
            # Validación de la contraseña ingresada por el usuario.
            if not inicio_de_sesión(username, password):
                
                mensaje = "La contraseña ingresada es incorrecta."
                return render_template("login.html", mensaje = mensaje)
            
            # Almacenamiento de las credenciales del usuario en la sesión.
            else:
                
                # Al momento de validar el login, el usuario será enviado al dashboard. A su vez, en este apartado se almacena el ID de usuario en la sesión.
                session["id"] = obtener_id(username)
                return redirect("/dashboard")
            
    return render_template("login.html", mensaje = None)

# Página de registro: Cualquier usuario es libre de registrarse, los nombres de usuario son únicos.
@app.route("/sign_in", methods = ["GET", "POST"])
def sign_in():
    
    # Un logueado no debería poder estar en esta sección.
    if esta_autenticado():
        return redirect("/dashboard")
    
    # Solicitud de las credenciales.
    if request.method == "POST":
        
        username = request.form["username"]
        name = request.form["name"]
        lastname = request.form["lastname"]
        password = request.form["password"]
        image = request.form["image"]
        
        # Ningún campo debe quedar vacío.
        if not username or not password or not lastname or not name:
            
            mensaje = "Debes completar todos los campos para completar el registro."
            return render_template("sign_in.html", mensaje = mensaje)
    
        # El nombre de usuario no puede contener espacios.
        if username.count(" ") > 0:
            
            mensaje = "El nombre de usuario no puede contener espacios."
            return render_template("sign_in.html", mensaje = mensaje)
        
        # El nombre de usuario sólo debe aceptar carácteres alfanuméricos.
        if not username.isalnum():
            
            mensaje = "El nombre de usuario sólo puede contener carácteres alfanuméricos."
            return render_template("sign_in.html", mensaje = mensaje)
        
        # La contraseña no debería ser tan corta.
        if len(password) < 5:
            
            mensaje = "Tu contraseña es demasiado corta."
            return render_template("sign_in.html", mensaje = mensaje)
        
        # Aprobación de las credenciales con la base de datos.
        if verificar_usuario_existente(username):
            
            mensaje = "El nombre de usuario ingresado no está disponible."
            return render_template("sign_in.html", mensaje = mensaje)
    
        # Insertar a la base de datos al nuevo usuario.
        else:
            # Si el registro se completa exitosamente, el usuario será enviado a la ruta de inicio de sesión.
            registrar_usuario(name, lastname, username, password, image)
            return redirect("/login")
        
    return render_template("sign_in.html", mensaje = None)
    
# Libro: Ruta dinámica que mostrará la página personalizada para cada libro y permite el posting de reseñas.
@app.route("/dashboard/<isbn>", methods = ["GET", "POST"])
@inicio_requerido
def books(isbn):
    datos_usuario = obtener_datos_usuario(session["id"])

    # Si el ISBN no está en la base de datos entonces retornar un error 404.
    if not verificar_libro_db(isbn):
        abort(404)

    consulta = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={api_key}")
    data = consulta.json()

    libro = data['items'][0]['volumeInfo']

    mensaje = None  # Inicializar el mensaje como None

    if request.method == "POST":
        book_review = request.form["book_review"]
        rating = request.form["rating"]
        user_review = obtener_review_usuario(session["id"], isbn)
        
        if not user_review:
            if not review(rating, book_review, session["id"], obtener_id_libro(isbn)):
                mensaje = "Ingresa una calificación válida."
            else:
                # Recupera la reseña actualizada y otros datos relevantes.
                user_review = obtener_review_usuario(session["id"], isbn)

        else:
            if not actualizar_review(session["id"], isbn, rating, book_review):
                mensaje = "Ingresa una calificación válida."

    # Obtiene los datos actualizados después de realizar las actualizaciones.
    estadisticas = estadisticas_libro(isbn)  # Número
    opiniones = reviews_usuarios(isbn)  # [estrellas, texto, usuario, fecha]
    estrellas = cantidad_reviews_estrellas(isbn)  # [0, 0, 0, 0, 0]
    user_review = obtener_review_usuario(session["id"], isbn)  # (estrellas, texto)

    return render_template("book.html", datos_usuario=datos_usuario, libro=libro, estadisticas=estadisticas, estrellas=estrellas, opiniones=opiniones, isbn=isbn, user_review=user_review, mensaje=mensaje)

@app.route("/delete/<isbn>", methods = ["GET", "POST"])
@inicio_requerido
def eliminar_review_page(isbn):
    
    # Si el ISBN no está en la base de datos entonces retornar un error 404. 
    if not verificar_libro_db(isbn):
        abort(404)
        
    user_review = obtener_review_usuario(session["id"], isbn) # (estrellas, texto)
    if user_review:
        eliminar_review(session["id"], isbn)
        return redirect(f"/dashboard/{isbn}")
    
    return redirect(f"/dashboard/{isbn}")

# Ruta API: Si un usuario desea consultar información de los libros de está página, podrá lograrlo con una API.
@app.route("/api/<isbn>")
def api(isbn):
    
    # Si el ISBN no está en la base de datos entonces retornar un error 404. 
    if not verificar_libro_db(isbn):
        abort(404)
    
    # Esto retorna un objeto en una estructura de diccionario.
    libro = book_information(isbn)
    return jsonify(libro)

# Ruta del cierre de sesión de la página.
@app.route("/close", methods = ["GET", "POST"])
@inicio_requerido
def close():
    
    # Comprueba si en las cookies existe una sesión.
    if "id" in session:
        session.pop('id', None)
        
    # En caso de cerrar la sesión, se mandará a la pestaña de inicio de sesión.
    return redirect("/login")

if __name__ == '__main__':

    app.run(debug=True)
    
# Proyecto Web Finalizado :)