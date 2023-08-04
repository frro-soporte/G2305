"""Base de Datos SQL - Alta"""

import datetime
from G2305.practico_04.ejercicio_01 import reset_tabla
import sqlite3

def agregar_persona(nombre, nacimiento, dni, altura):
    """Implementar la funcion agregar_persona, que inserte un registro en la
    tabla Persona y devuelva los datos ingresados el id del nuevo registro."""
    conn = sqlite3.connect("Ejercicio1.db")
    c = conn.cursor()
    sql = "INSERT INTO Persona (nombre, FechaNacimiento, dni, altura) VALUES (?, ?, ?,?)"
    valores= (nombre,nacimiento,dni,altura)
    c.execute(sql,valores)
    id= c.lastrowid       #Obtengo ID
    conn.commit()
    c.close()
    return id

# NO MODIFICAR - INICIO
@reset_tabla
def pruebas():
    id_juan = agregar_persona('juan perez', datetime.datetime(1988, 5, 15), 32165498, 180)
    id_marcela = agregar_persona('marcela gonzalez', datetime.datetime(1980, 1, 25), 12164492, 195)
    assert id_juan > 0
    assert id_marcela > id_juan

if __name__ == '__main__':
    pruebas()
# NO MODIFICAR - FIN

