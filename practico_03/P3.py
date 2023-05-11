from __future__ import  annotations
from typing import Optional
from dataclasses import dataclass
from typing import List
""" Práctica 3"""

"""Constructor, Variables de instancia y métodos de instacia
   Implementar la clase Rectangulo que contiene una base y una altura, y el
    método area.
    """
""" EJ 1"""

class Rectangulo:
    def __init__(self, base: float=None, altura: float=None) -> None:
        self.base: float = base
        self.altura: float = altura

    def area(self):
        if self.base is None or self.altura is None:
            return 0
        return self.base * self.altura

# Test Constructor
rec = Rectangulo(10, 10)
assert rec.base == 10
assert rec.altura == 10
assert rec.area() == 100

# Test Valores por defecto
rec = Rectangulo()
assert rec.base is None
assert rec.altura is None
assert rec.area() == 0

rec.base = 10
rec.altura = 10
assert rec.base == 10
assert rec.altura == 10
assert rec.area() == 100

# Test Instanciación sin variable
assert Rectangulo(10, 10).area() == 100
assert Rectangulo(10, 0).area() == 0
assert Rectangulo(0, 10).area() == 0
# NO MODIFICAR - FIN

 ################################################################################
""" EJ 2 """

"""Clase con "nombre" como variable de instancia y un id incremental
    generado automáticamente.
    Restricciones:
        - Utilizar sólamente el constructor (__init__) y un método de
          clase (@classmethod) con una variable de clase"""
class Articulo:
    _ult_id: int=0
    def __init__(self,nombre: str="")->None:
        self.nombre: str=nombre
        self.id_: int = self._sig_id()

    @classmethod
    def _sig_id(cls):
        cls._ult_id +=1
        return cls._ult_id

art1 = Articulo("manzana")
art2 = Articulo("pera")
art3 = Articulo()
art3.nombre = "tv"

assert art1.nombre == "manzana"
assert art2.nombre == "pera"
assert art3.nombre == "tv"

assert art1.id_ == 1
assert art2.id_ == 2
assert art3.id_ == 3
assert Articulo._ult_id == 3

#############################################################################
""" EJ 3"""
"""Clase con los siguientes miembros:
Atributos de instancia:
- nombre: str
- edad: int
- sexo (H hombre, M mujer): str
- peso: float
- altura: float
Métodos:
- es_mayor_edad(): indica si es mayor de edad, devuelve un booleano.
"""
"""
class Persona:
    def __init__(self,nombre: str ="",edad: int=None,sexo: str="",peso: float = None,altura: float = None ):
        self.nombre=nombre
        self.edad=edad
        self.sexo=sexo
        self.peso=peso
        self.altura=altura

    def es_mayor_edad(self):
        if self.edad>=18:
            return True
        return False

assert Persona("Juan", 18, "H", 85, 175.9).es_mayor_edad()
assert not Persona("Julia", 16, "M", 65, 162.4).es_mayor_edad()  """

""" HACERLO CON DATACLASS"""
####from dataclasses import dataclass
""" ¿Como pongo val por defecto en dataclass?"""

@dataclass
class Persona:
    nombre: str
    edad: int
    sexo: str
    peso: float
    altura: float

    def es_mayor_edad(self):
        if self.edad >= 18:
            return True
        return False

assert Persona("Juan", 18, "H", 85, 175.9).es_mayor_edad()
assert not Persona("Julia", 16, "M", 65, 162.4).es_mayor_edad()

#####################################################################################################################
""" EJ 4"""
"""Escribir un constructor que añada una variable de instancia llamada raza,
  de tipo string y que tenga como valor por defecto "". Adicionalmente se debe
  sobrecargar el método descripción para que devuelva:
  "Soy un perro y" + método descripción del padre
  """
"""
class Animal:
    def __init__(self, edad: int = 0):
        self.edad = edad

    def descripcion(self) -> str:
        return f"Tengo {self.edad} años"

class Perro(Animal):
    def __init__(self, edad: int= 0, raza: str = ""):
        super().__init__(edad)
        self.raza = raza


    def descripcion(self)->str:
        return "Soy un perro y " + super().descripcion().lower()

terrier = Perro(edad=8, raza="Yorkshire Terrier")
cachorro = Perro(edad=1)
dogo = Perro(raza="Dogo")

assert Animal(10).descripcion() == "Tengo 10 años"
assert terrier.descripcion() == "Soy un perro y tengo 8 años"
assert dogo.descripcion() == "Soy un perro y tengo 0 años"
assert cachorro.descripcion() == "Soy un perro y tengo 1 años"  """




"""Re-Escribir utilizando DataClasses"""

@dataclass
class Animal:
    edad: int = 0

    def descripcion(self) -> str:
        return f"Tengo {self.edad} años"

@dataclass
class Perro(Animal):
    raza: str = ""

    def descripcion(self) -> str:
        return "Soy un perro y " + super().descripcion().lower()

terrier = Perro(edad=8, raza="Yorkshire Terrier")
cachorro = Perro(edad=1)
dogo = Perro(raza="Dogo")

assert Animal(10).descripcion() == "Tengo 10 años"
assert terrier.descripcion() == "Soy un perro y tengo 8 años"
assert dogo.descripcion() == "Soy un perro y tengo 0 años"
assert cachorro.descripcion() == "Soy un perro y tengo 1 años"

################################################################################
""" EJ 5"""
"""La clase auto tiene dos propiedades, precio y marca. La marca se define
  obligatoriamente al construir la clase y siempre que se devuelve, se 
  devuelve con la primer letra en mayúscula y no se puede modificar. El precio
  puede modificarse pero cuando se muestra, se redondea a 2 decimales"""


class Auto:
    def __init__(self, marca: str, precio: float):
        self._marca = marca
        self._precio = precio

    @property
    def marca(self):
        return self._marca
    @property
    def precio(self):
        return round(self._precio,2)
    @precio.setter
    def precio(self,valor: float):
        self._precio = valor

auto = Auto("Ford", 12_875.456)

assert auto.marca == "Ford"
assert auto.precio == 12_875.46
auto.precio = 13_874.349
assert auto.precio == 13_874.35

try:
    auto.marca = "Chevrolet"
    assert False
except AttributeError:
     assert True

##################################################################
""" Reescribir con dataclasses"""

@dataclass
class Auto:
    _nombre: str
    _precio: float

    def __post_init__(self):
        self._nombre = self._nombre.capitalize()

    @property
    def nombre(self):
        return self._nombre

    @property
    def precio(self):
        return round(self._precio, 2)

    @precio.setter
    def precio(self, valor: float):
        self._precio = valor

auto = Auto("Ford", 12_875.456)

assert auto.nombre == "Ford"
assert auto.precio == 12_875.46
auto.precio = 13_874.349
assert auto.precio == 13_874.35

try:
    auto.nombre = "Chevrolet"
    assert False
except AttributeError:
    assert True

####################################################################

""" EJ 6"""
"""Agregar los métodos que sean necesarios para que los test funcionen.
    Hint: los métodos necesarios son todos magic methods
    Referencia: https://docs.python.org/3/reference/datamodel.html#basic-customization"""

#from __future__ import annotations
#from typing import List
class Article:
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name
    def __repr__(self):
        return f"Article('{self.name}')"

class ShoppingCart:

    def __init__(self, articles: List[Article] = None) -> None:
        if articles is None:
            self.articles = []
        else:
            self.articles = articles

    def add(self, article: Article) -> ShoppingCart:
        self.articles.append(article)
        return self

    def remove(self, remove_article: Article) -> ShoppingCart:
        new_articles = []

        for article in self.articles:
            if article != remove_article:
                new_articles.append(article)

        self.articles = new_articles

        return self

    def __str__(self):
        return str([str(article) for article in self.articles])

    def __repr__(self):
        return f"ShoppingCart({self.articles})"

    def __eq__(self, other):
        return set(self.articles) == set(other.articles)


manzana = Article("Manzana")
pera = Article("Pera")
tv = Article("Television")

# Test de conversión a String
assert str(ShoppingCart().add(manzana).add(pera)) == "['Manzana', 'Pera']"

# Test de reproducibilidad
carrito = ShoppingCart().add(manzana).add(pera)
assert carrito == eval(repr(carrito))

# Test de igualdad
assert ShoppingCart().add(manzana) == ShoppingCart().add(manzana)

# Test de remover objeto
assert ShoppingCart().add(tv).add(pera).remove(tv) == ShoppingCart().add(pera)

# Test de igualdad con distinto orden
assert ShoppingCart().add(tv).add(pera) == ShoppingCart().add(pera).add(tv)

# Test de suma
combinado = ShoppingCart().add(manzana) + ShoppingCart().add(pera)
assert combinado == ShoppingCart().add(manzana).add(pera)