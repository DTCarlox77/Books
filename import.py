# Script para subir los libros del archivo csv a la base de datos remota PostgreSQL.
import csv
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

# Carga de las variables de entorno.
load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Obtención y envío de la información de libros.
def main():
    
    f = open("books.csv")
    reader = csv.reader(f)
    
    # Saltar encabezados.
    next(reader)
    insertado = 1
    
    # Inserciones a la base de datos.
    for isbn, title, author, year in reader:

        query = text("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)")
        db.execute(query, {"isbn": isbn, "title": title, "author": author, "year": int(year)})
        
        # Mensaje de envío.
        print(f"El libro: {insertado}, con título '{title}' se ha insertado correctamente.")
        insertado += 1
        
    db.commit()

if __name__ == "__main__":
    main()
    
# Este código es un chiste a comparación de los otros {Emoji de calavera}.