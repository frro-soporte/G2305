"""Base de Datos SQL - Búsqueda"""

import datetime
import sqlite3

from ejercicio_02 import agregar_persona
from ejercicio_06 import reset_tabla

def borrar_tabla():
    conn = sqlite3.connect("Ejercicio1.db")
    c = conn.cursor()
    c.execute("DELETE FROM Persona")
    c.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='Persona'")
    conn.commit()
    conn.close()

def buscar_persona(id_persona):
    """Implementar la funcion buscar_persona, que devuelve el registro de una 
    persona basado en su id. El return es una tupla que contiene sus campos: 
    id, nombre, nacimiento, dni y altura. Si no encuentra ningun registro, 
    devuelve False."""
    conn = sqlite3.connect("Ejercicio1.db")
    c = conn.cursor()
    c.execute("SELECT * FROM Persona WHERE IdPersona=(?)",(id_persona,))
    persona = c.fetchone()
    if persona:

        personaList = list(persona)
        personaList[2] = datetime.datetime.strptime(persona[2], "%Y-%m-%d %H:%M:%S")
        persona = tuple(personaList)
        return persona
    else:
        return False



# NO MODIFICAR - INICIO
@reset_tabla
def pruebas():
    juan = buscar_persona(agregar_persona('juan perez', datetime.datetime(1988, 5, 15), 32165498, 180))
    assert juan == (1, 'juan perez', datetime.datetime(1988, 5, 15), 32165498, 180)
    assert buscar_persona(12345) is False

if __name__ == '__main__':
    pruebas()
# NO MODIFICAR - FIN
