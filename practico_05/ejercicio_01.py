"""Base de Datos - Creación de Clase en ORM"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Socio(Base):
    """Implementar un modelo Socio a traves de Alchemy que cuente con los siguientes campos:
        - id_socio: entero (clave primaria, auto-incremental, unico)
        - dni: entero (unico)
        - nombre: string (longitud 250)
        - apellido: string (longitud 250)
    """
    __tablename__ = "socios"

    id = Column("id_socio", Integer(), primary_key=True, autoincrement=True)
    dni = Column("dni", Integer(), unique=True)
    nombre = Column("nombre", String(250))
    apellido = Column("apellido", String(250))

    def asignar(self, otro):
        if isinstance(otro, Socio):
            atributos = list(self.__dict__.keys())
            atributos.remove('_sa_instance_state')
            for attr in atributos:
                setattr(self,attr,getattr(otro,attr))

        else:
            raise ValueError("Debe ser un objeto tipo Socio")



    def __repr__(self):
        return f"Socio(dni={self.dni}, nombre={self.nombre}, apellido= {self.apellido})"

    def __str__(self):
        return f"Socio nombre:{self.nombre}, apellido:{self.apellido}, dni:{self.dni}, id:{self.id}"

    def __eq__(self, other):
        return self.id == other.id





    # Completar
