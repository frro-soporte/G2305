from sqlalchemy import create_engine, ForeignKey, Column,String , Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import  sessionmaker

"""Sessionmaker crea sesiones para poder utilizar la DB"""

Base = declarative_base()

class  Person(Base):
    __tablename__= "people"       #Nombre de la tabla de SQLite DB

    idP = Column("idP", Integer, primary_key=True)      #Variable dentro de python y digo a que corresponde en la DB y parámetros
    nombre= Column("name",String)
    apellido = Column("apellido", String)
    genero = Column("genero",CHAR)
    edad = Column("edad", Integer)

    def __init__(self,idP,nombre,apellido,genero,edad):
        self.idP = idP
        self.nombre = nombre
        self.apellido = apellido
        self.genero = genero
        self.edad = edad

    def __repr__(self):
        return f"({self.idP}) {self.nombre}  {self.apellido} ({self.genero},{self.edad})"


#Una vez que tenemos las clases tenemos que crear un Engine y especificar la DB

engine = create_engine("sqlite:///mydb.db", echo=True)

"""El parámetro echo en la función create_engine de SQLAlchemy se utiliza para habilitar o deshabilitar la impresión de todas las declaraciones SQL que se ejecutan en la base de datos. 
El valor predeterminado es False, lo que significa que no se imprimirán las declaraciones SQL."""

Base.metadata.create_all(bind=engine)     # Toma todas las clases que extienden Base y las crea en la DB

Session = sessionmaker(bind=engine)      #Clase
session = Session()                      #Instancia

person = Person(12312,"Mike","Smit","m",35)
session.add(person)           #Añade la persona a la DB
session.commit()

p1 = Person(12313,"Anna","Smit","f",40)
p2 = Person(12314,"Bob","Smit","m",55)

session.add(p1)
session.add(p2)

session.commit()

#results = session.query(Person).all()            #Query a la tabla y asigo al resultset
results = session.query(Person).filter(Person.nombre.like("%An%"))
for r in results:
    print(r)