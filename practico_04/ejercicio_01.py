import sqlite3
import datetime

def crear_tabla():
    conn = sqlite3.connect("Ejercicio1.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS Persona (
            IdPersona INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre CHAR(30),
            FechaNacimiento DATE,
            DNI INTEGER,
            Altura INTEGER
    )""")
    conn.commit()

    # Cerrar la conexión con la base de datos
    conn.close()


# Llamar a la función para crear la tabla
crear_tabla()

"""Implementar la funcion borrar_tabla, que borra la tabla creada 
   anteriormente."""
def borrar_tabla():
   conn= sqlite3.connect("Ejercicio1.db")
   c= conn.cursor()

   c.execute("""
   DROP TABLE IF EXISTS Persona
   """)

   conn.commit()
   conn.close()

def reset_tabla(func):
    def func_wrapper():
        crear_tabla()
        func()
        borrar_tabla()
    return func_wrapper