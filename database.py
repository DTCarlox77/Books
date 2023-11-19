# Database.py es un archivo dedicado al CRUD en la base de datos.
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
import bcrypt
import random

# Carga de las credenciales en la variable de entorno.
load_dotenv()
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("Error de conexión con la URL de la base de datos.")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Cifrador de contraseñas para enviarlas a la base de datos de forma segura.
def hash_password(password): 
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    # Para evitar conflictos con el tipo de dato en PostgreSQL, se realiza una conversión a String.
    hashed_password_str = hashed_password.decode('utf-8')
    return hashed_password_str

# Recibe una contraseña y la compara con la contraseña cifrada en la base de datos, si coincide retorna True.
def unhash_password(password, hashed_password):
    
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password_bytes)

# Para evitar confictos con los nombres de usuario, la función realiza una búsqueda de prevención.
def verificar_usuario_existente(username):
    
    query = text("SELECT COUNT(*) FROM users WHERE username = :username")
    result = db.execute(query, {"username": username}).fetchone()
    return result[0] > 0

# Registro de un usuario a la plataforma. (Si el usuario existe, entonces no crear nueva cuenta) (Devuelve un valor Booleano).
def registrar_usuario(name, lastname, username, password, image):
    
    # Evitar la repetición de nombres de usuario.
    if verificar_usuario_existente(username):
        return False
    
    # Encriptación de la contraseña.
    password_hash = hash_password(password)
    
    # Consulta para el registro de un nuevo usuario.
    query = text("INSERT INTO users (username, name, lastname, password_hash, image) VALUES (:username, :name, :lastname, :password_hash, :image)")
    try:
        db.execute(query, {"username": username, "name": name, "lastname": lastname, "password_hash": password_hash, "image": image})
        db.commit()
        return True
    
    except Exception as e:
        db.rollback()  # En caso de error, deshacer los cambios.
        print("Error al registrar el usuario: " + str(e))
        return False
    
# Opción del usuario para un cambio de contraseña.
def change_password(user_id, old_password, new_password):
    
    query = text("SELECT password_hash FROM users WHERE id = :id")
    result = db.execute(query, {"id": user_id}).fetchone()
    
    # Valida que la antigua contraseña sea válida.
    if unhash_password(old_password, result[0]):
        
        # Cifrar la nueva contraseña.
        new_password = hash_password(new_password)
        
        # Inserta la nueva contraseña.    
        query = text("UPDATE users SET password_hash = :password_hash WHERE id = :id")
        
        try:
            db.execute(query, {"password_hash": new_password, "id": user_id})
            db.commit()
            return True
        
        except Exception as e:
            db.rollback()  # En caso de error, deshacer los cambios.
            print("Error al cambiar la contraseña: " + str(e))
            return False
            
    return False
    
# Validación de credenciales para el inicio de sesión en la plataforma (Devuelve un valor Booleano).
def inicio_de_sesión(username, password):
    
    if verificar_usuario_existente(username):
        
        query = text("SELECT password_hash FROM users WHERE username = :username")
        result = db.execute(query, {"username": username}).fetchone()
        return unhash_password(password, result[0])
    
# Función que obtiene el ID a partir del nombre de usuario ingresado en el inicio de sesión.
def obtener_id(username):
    
    if verificar_usuario_existente(username):
        
        query = text("SELECT id FROM users WHERE username = :username")
        result = db.execute(query, {"username": username}).fetchone()
        return result[0]
    
    else:
        return "El usuario no existe."

# Devuelve una lista con los datos del usuario en la sesión.
def obtener_datos_usuario(id):
    
    if not id:
        return False
    
    query = text("SELECT id, username, name, lastname, password_hash, DATE(created_at), image FROM users WHERE id = :id")
    result = db.execute(query, {"id": id}).fetchone()
    return result

    # Orden: ID, Username, Name, Lastname, Password, Date, Image (Campo nuevo)
    
# Elimina todo de un usuario, su cuenta y sus reseñas.
def eliminar_usuario(user_id):
    query_reviews = text("DELETE FROM reviews WHERE user_id = :user_id")
    query_user = text("DELETE FROM users WHERE id = :user_id")
    
    try:
        db.execute(query_reviews, {"user_id": user_id})  
        db.execute(query_user, {"user_id": user_id})
        db.commit()
        
        return True
    
    except Exception as e:
        db.rollback()  # En caso de error, deshacer los cambios.
        print("Error al eliminar el usuario: " + str(e))
        
        return False
    
# Cambio de URL de imagen de perfil.
def change_image(user_id, image):
    
    query = text("UPDATE users SET image = :image WHERE id = :id")
    
    try:
        db.execute(query, {"image": image, "id": user_id})
        db.commit()
        return True
        
    except Exception as e:
        db.rollback()  # En caso de error, deshacer los cambios.
        print("Error al cambiar la contraseña: " + str(e))
        return False

# Si el libro está en la base de datos, de podrá reseñar.
def verificar_libro_db(isbn):
    
    query = text("SELECT COUNT(*) FROM books WHERE isbn = :isbn")
    result = db.execute(query, {"isbn": isbn}).fetchone()
    
    return result[0] > 0

# Agrega reseñas a la base de datos.
def review(rating, review_text, user_id, book_id):
    
    # Métodos de validación de credenciales antes de insertar la reseña a la base de datos.
    if rating.strip():
        rating = int(rating)
        if rating > 5 or rating < 1:
            print("Algo salió mal.")
            return False
    
    else:
        return False
    
    # Inserción de la reseña a la base de datos.
    query = text("INSERT INTO reviews (user_id, book_id, rating, review_text) VALUES (:user_id, :book_id, :rating, :review_text)")
    try:
        db.execute(query, {"user_id": user_id, "book_id": book_id, "rating": rating, "review_text": review_text})
        db.commit()
        print(query.compile().params)
        return True
    
    except Exception as e:
        db.rollback()  # En caso de error, deshacer los cambios.
        print("Error al insertar la reseña: " + str(e))
        return False
    
# En la tabla de reviews se almacenan las reseñas en función del ID en la base de datos propia, por ende su obtención es necesaria para otras consultas. El "international standard book number" (isbn) será la clave de las búsquedas en la base de datos.
def obtener_id_libro(isbn):
    
    query = text("SELECT id FROM books WHERE isbn = :isbn")
    result = db.execute(query, {"isbn": isbn}).fetchone()
    
    if result:
        return result[0]
    
    return False

# La principal función de esto es la de saber si un X libro posee al menos una reseña.
def cantidad_reviews_libro(isbn):
    
    book_id = obtener_id_libro(isbn)
    
    query = text("SELECT COUNT(*) FROM reviews WHERE book_id = :id")
    result = db.execute(query, {"id": book_id}).fetchone()
    return result[0] > 0

# Devuelve el número de reviews que posee un libro.
def estadisticas_libro(isbn):
    
    book_id = obtener_id_libro(isbn)
    
    query = text("SELECT COUNT(*), AVG(reviews.rating) AS rating_promedio FROM reviews WHERE book_id = :id")
    result = db.execute(query, {"id": book_id}).fetchone()
    
    if result[1]:
        return [result[0], round(float(result[1]), 1)]
    
    return False

# Destinada a mostrar las reviews de otros usuarios en la plataforma.
def reviews_usuarios(isbn):
    
    book_id = obtener_id_libro(isbn)
    
    query = text("""
            SELECT reviews.rating, reviews.review_text, users.username, DATE(reviews.created_at) AS fecha
            FROM reviews
            INNER JOIN users ON reviews.user_id = users.id
            WHERE reviews.book_id = :book_id
            """)

    result = db.execute(query, {"book_id": book_id}).fetchall()
    
    if result:
        return result
    
    return False

# Retorna una lista en orden creciente del total de estrellas que posee un libro.
def cantidad_reviews_estrellas(isbn):
    
    book_id = obtener_id_libro(isbn)
    stars = []
    
    for rating in range(1, 6):
        query = text("SELECT COUNT(*) FROM reviews WHERE rating = :rating AND book_id = :book_id")
        result = db.execute(query, {"rating": rating, "book_id": book_id}).fetchone()
        
        if result:
            stars.append(result[0])
            
    return stars

# Obtiene la review del usuario en la sesión para darle la posibilidad de editarla.
def obtener_review_usuario(user_id, isbn):
    
    book_id = obtener_id_libro(isbn)
    query = text("SELECT rating, review_text FROM reviews WHERE user_id = :user_id AND book_id = :book_id")
    result = db.execute(query, {"user_id": user_id, "book_id": book_id}).fetchone()
    
    if result:
        return result
    
    return False

# Reviews que un usuario ha realizado, esta función las extrae todas para mostrarlas en su perfil.
def obtener_reviews(user_id):
    
    query = text("""
            SELECT reviews.rating, reviews.review_text, books.isbn, DATE(reviews.created_at) AS date, books.title
            FROM reviews
            INNER JOIN books ON reviews.book_id = books.id
            WHERE user_id = :user_id
            """)

    result = db.execute(query, {"user_id": user_id}).fetchall()
    
    if result:
        return result
    
    return False

# Eliminar reseña si el usuario lo desea. Hay que recordar que el USER_ID se obtiene a partir de la sesión y el ISBN a través de la API..
def eliminar_review(user_id, isbn):
    
    book_id = obtener_id_libro(isbn)
    
    query = text("DELETE FROM reviews WHERE user_id = :user_id AND book_id = :book_id")
    try:
        db.execute(query, {"user_id": user_id, "book_id": book_id})
        db.commit()
        return True
    
    except Exception as e:
        db.rollback()  # En caso de error, deshacer los cambios.
        print("Error al eliminar la reseña: " + str(e))
        return False
    
# Actualización de una reseña.
def actualizar_review(user_id, isbn, rating, review_text):
    
    book_id = obtener_id_libro(isbn)
    
    # Métodos de validación de credenciales antes de insertar la reseña a la base de datos.
    if rating.strip():
        rating = int(rating)
        if rating > 5 or rating < 1:
            print("Algo salió mal.")
            return False
    
    try:
        query = text("UPDATE reviews SET rating = :rating, review_text = :review_text WHERE user_id = :user_id AND book_id = :book_id")
        db.execute(query, {"rating": rating, "review_text": review_text, "user_id": user_id, "book_id": book_id})
        db.commit()
        return True
        
    except Exception as e:
        db.rollback()  # En caso de error, deshacer los cambios.
        print("Error al actualizar la reseña: " + str(e))
        return False

# Devuelve un diccionario con la información de un libro perteneciente a la base de datos.
def book_information(isbn):
    
    # Esta función es exclusiva de los libros en la base de datos.
    if not verificar_libro_db(isbn):
        return False
    
    # Un libro sin reseñas deberá contener vacío el apartado de reseñas y cantidad de reseñas totales en el formato JSON, por eso se realiza la siguiente validación.
    if cantidad_reviews_libro(isbn):
        
        query = text("""
            SELECT books.*, AVG(reviews.rating) AS rating_promedio, COUNT(reviews.id)
            FROM books
            LEFT JOIN reviews ON books.id = reviews.book_id
            WHERE books.isbn = :isbn
            GROUP BY books.id
        """)
    else:
        
        query = text("SELECT * FROM books WHERE isbn = :isbn")
    
    # Lista con los resultados de la consulta.
    result = db.execute(query, {"isbn": isbn}).fetchone()
    
    # Creación del diccionario para posteriormente generar un formato JSON.
    if cantidad_reviews_libro(isbn):
        
        objeto = {
            "tittle": result[2],
            "author": result[3],
            "year": result[4],
            "isbn": isbn,
            "review_count": result[6],
            "average_score": round(float(result[5]), 1)
        }
        
    else:
        
        objeto = {
            "tittle": result[2],
            "author": result[3],
            "year": result[4],
            "isbn": isbn,
            "review_count": "N/A",
            "average_score": "N/A"
        }
    
    return objeto

# Función realizar una búsqueda general entre los libros de la base de datos sin importar en sí el parámetro de búsqueda.
def obtener_libros_busqueda(search=""):
    
    # Si no hay actualización de la variable, entonces no tomarla (tomarla vacía).
    year = None
    
    # Solución al bug por búsqueda de ISBN. Ahora se comprueba que la longitud sea de cuatro dígitos si en realidad se desea obtener un libro buscado por año de publicación.
    
    if len(search) == 4:   
        # En caso de ingresar un número, es posible que este sea el año de publicación del libro.
        try:
            year = int(search)
        except ValueError:
            year = None
        
    # La consulta se limita a las 50 primeras coincidencias para evitar altos tiempos de carga.
    query = text("SELECT * FROM books WHERE (LOWER(title) LIKE LOWER(:search) OR LOWER(author) LIKE LOWER(:search) OR LOWER(isbn) LIKE LOWER(:search) OR year = :year) LIMIT 50")
    result = db.execute(query, {"search": f"%{search}%", "year": year}).fetchall()

    # Estructura: ID, ISBN, TITLE, AUTHOR, YEAR.    
    return result

# Realizar una búsqueda aleatória entre diferentes libros para dar "recomendaciones".
def sugerencias():
    
    search = random.choice("abcdefghijklmnopqrstuvwxyz")
    
    # La consulta se limita a las 15 primeras coincidencias para evitar altos tiempos de carga.
    query = text("SELECT * FROM books WHERE (LOWER(title) LIKE LOWER(:search) OR LOWER(author) LIKE LOWER(:search)) LIMIT 14")
    result = db.execute(query, {"search": f"%{search}%"}).fetchall()
    
    return result

# Por: Carlos Adrián Espinosa Luna / Grupo K