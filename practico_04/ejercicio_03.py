"""Base de Datos SQL - Baja"""

import datetime
import sqlite3

from ejercicio_01 import reset_tabla
from ejercicio_02 import agregar_persona



def borrar_persona(id_persona):
    """Implementar la funcion borrar_persona, que elimina un registro en la 
    tabla Persona. Devuelve un booleano en base a si encontro el registro y lo 
    borro o no."""
    conn: sqlite3.Connection = sqlite3.connect("data.db")
    curs: sqlite3.Cursor = conn.cursor()
    curs.execute("DELETE FROM Persona WHERE idPersona = (?)",(id_persona, ))
    cantidad_cambios = conn.total_changes
    conn.commit()
    conn.close()
    return bool(cantidad_cambios)
# NO MODIFICAR - INICIO
@reset_tabla
def pruebas():
    assert borrar_persona(agregar_persona('juan perez', datetime.datetime(1988, 5, 15), 32165498, 180))
    assert borrar_persona(12345) is False

if __name__ == '__main__':
    pruebas()
# NO MODIFICAR - FIN
