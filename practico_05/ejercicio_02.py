"""Base de Datos - ORM"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ejercicio_01 import Base, Socio

from typing import List, Optional

class DatosSocio():

    def __init__(self):
        self.__engine = create_engine("sqlite:///practica5.db")
        self.__Session = sessionmaker(bind=self.__engine)
        Base.metadata.create_all(bind=self.__engine)


    def buscar(self, id_socio: int) -> Optional[Socio]:
        """Devuelve la instancia del socio, dado su id. Devuelve None si no 
        encuentra nada.
        """
        session = self.__Session()
        socio = session.query(Socio).filter(Socio.id == id_socio).first()
        session.close()
        return socio

    def buscar_dni(self, dni_socio: int) -> Optional[Socio]:
        """Devuelve la instancia del socio, dado su dni. Devuelve None si no 
        encuentra nada.
        """
        session = self.__Session()
        socio = session.query(Socio).filter(Socio.dni == dni_socio).first()
        session.close()
        return socio
        
    def todos(self) -> List[Socio]:
        """Devuelve listado de todos los socios en la base de datos."""
        session = self.__Session()
        socios = session.query(Socio).All()
        session.close()
        return socios

    def borrar_todos(self) -> bool:
        """Borra todos los socios de la base de datos. Devuelve True si el 
        borrado fue exitoso.
        """
        session = self.__Session()

        try:
            session.query(Socio).delete()
            session.commit()
            return True
        except:
            session.rollback()
            return False
        finally:
            session.close()


    def alta(self, socio: Socio) -> Socio:
        """Agrega un nuevo socio a la tabla y lo devuelve"""
        sesion = self.__Session(expire_on_commit=False)
        sesion.add(socio)
        sesion.commit()
        sesion.expunge(socio)
        sesion.close()

        return socio


def baja(self, id_socio: int) -> bool:
        """Borra el socio especificado por el id. Devuelve True si el borrado 
        fue exitoso.
        """
        session = self.__Session()
        socio = session.query(Socio).filter(Socio.id == id_socio).first()
        if socio:
            session.delete(socio)
            session.commit()
            return True
        else:
            return True
        session.close()

    def modificacion(self, socio: Socio) -> Socio:
        """Guarda un socio con sus datos modificados. Devuelve el Socio 
        modificado.
        """
        session = self.__Session()
        soc_viejo = session.query(Socio).filter(Socio.id == socio.id).first()
        if soc_viejo:
            soc_viejo.modificar(socio)
            session.commit()
        else:

        session.close()
        return socio
    
    def contarSocios(self) -> int:
        """Devuelve el total de socios que existen en la tabla"""
        session = self.__Session()
        cant = session.query(Socio).count()
        session.close()
        return cant



# NO MODIFICAR - INICIO

# Test Creación
datos = DatosSocio()

# Test Alta
socio = datos.alta(Socio(dni=12345678, nombre='Juan', apellido='Perez'))
assert socio.id > 0

# Test Baja
assert datos.baja(socio.id) == True

# Test Consulta
socio_2 = datos.alta(Socio(dni=12345679, nombre='Carlos', apellido='Perez'))
assert datos.buscar(socio_2.id) == socio_2

# Test Buscar DNI
socio_2 = datos.alta(Socio(dni=12345670, nombre='Carlos', apellido='Perez'))
assert datos.buscar_dni(socio_2.dni) == socio_2

# Test Modificación
socio_3 = datos.alta(Socio(dni=12345680, nombre='Susana', apellido='Gimenez'))
socio_3.nombre = 'Moria'
socio_3.apellido = 'Casan'
socio_3.dni = 13264587
datos.modificacion(socio_3)
socio_3_modificado = datos.buscar(socio_3.id)
assert socio_3_modificado.id == socio_3.id
assert socio_3_modificado.nombre == 'Moria'
assert socio_3_modificado.apellido == 'Casan'
assert socio_3_modificado.dni == 13264587

# Test Conteo
assert len(datos.todos()) == 3

# Test Delete
datos.borrar_todos()
assert len(datos.todos()) == 0

# NO MODIFICAR - FIN