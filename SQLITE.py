import sqlite3

# Crear a conexion ( Es necesario para cualquier accion en la DB)

conn = sqlite3.connect("DatabaseName.db")  # Si no existe la crea en el directorio del programa
conn = sqlite3.connect(":memory:")  # Crea una conexion a una DB en memoria, cuando cierro el programa no guarda nada

# Crear una tabla y añadir data
"""Primero tenemos que crear un cursor, le dice a la db lo que queremos hacer"""

c = conn.cursor()

"""Crear una tabla, execute ejecuta comandos"""

'''
c.execute("""CREATE TABLE customers (
		nombre text , 
		apellido text, 
		email text,
)""")
'''

# Si lo imputamos asi con """, puede ser multilinea (docstrings)
# DATATYPE define el tipo de dato de la columna, SQLite tiene solo 5 tipos de datos (NULL, INTEGER, REAL , TEXT ,BLOB)

""" Hasta aca no se ejecuto, tenemos que commitearlo en la DB"""
conn.commit()

# Cerrar conexion

conn.close()