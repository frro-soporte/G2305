import datetime
import sqlite3
from ejercicio_02 import agregar_persona
from ejercicio_04 import buscar_persona
from ejercicio_06 import reset_tabla
def crear_tabla_peso():
    """Implementar la funcion crear_tabla_peso, que cree una tabla PersonaPeso con:
        - IdPersona: Int() (Clave Foranea Persona)
        - Fecha: Date()
        - Peso: Int()
    """
    conn= sqlite3.connect("Ejercicio1.db")
    c=conn.cursor()
    c.execute(""" CREATE TABLE IF NOT EXISTS PersonaPeso(
    IdPersona integer,
    Fecha Date,
    Peso integer,
    CONSTRAINT fk_persona FOREIGN KEY (IdPersona) REFERENCES Persona(IdPersona)
    )""")
    conn.commit()
    conn.close()
def agregar_peso(id_persona, fecha, peso):
    """Implementar la funcion agregar_peso, que inserte un registro en la tabla
    PersonaPeso.

    Debe validar:
    - Que el ID de la persona ingresada existe (reutilizando las funciones ya
        implementadas).
    - Que no existe de esa persona un registro de fecha posterior al que
        queremos ingresar.

    Debe devolver:
    - ID del peso registrado.
    - False en caso de no cumplir con alguna validacion."""
    persona = buscar_persona(id_persona)
    if persona is False:  # Verificar si persona es False
        return False
    if isinstance(persona, tuple) and fecha <= persona[2]:                          #Verifico si es instancia de una tupla
        return False
    conn = sqlite3.connect("Ejercicio1.db")
    c = conn.cursor()
    c.execute(""" INSERT INTO PersonaPeso (IdPersona, Fecha, Peso) VALUES (?, ?, ?) """,(id_persona,fecha,peso))
    id_peso = c.lastrowid
    conn.commit()
    conn.close()
    return id_peso


# NO MODIFICAR - INICIO
@reset_tabla
def pruebas():
    id_juan = agregar_persona('juan perez', datetime.datetime(1988, 5, 15), 32165498, 180)
    assert agregar_peso(id_juan, datetime.datetime(2018, 5, 26), 80) > 0
    # Test Id incorrecto
    assert agregar_peso(200, datetime.datetime(1988, 5, 15), 80) == False
    # Test Registro previo al 2018-05-26
    assert agregar_peso(id_juan, datetime.datetime(2018, 5, 16), 80) == False



if __name__ == '__main__':
    crear_tabla_peso()
    pruebas()
# NO MODIFICAR - FIN

