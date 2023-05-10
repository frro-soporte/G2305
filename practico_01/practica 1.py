from typing import Iterable
from typing import List, Union
from typing import Any


# EJERCICIO 1
"""Toma dos números y devuelve el mayor.
    Restricción: No utilizar la función max """


def maximo_basico(a: float, b: float):
  if a>=b:
    return a
  else:
     return b

assert maximo_basico(9, 18) == 18
assert maximo_basico(10, 5) == 10

################################################################

"""Re-escribir utilizando el built-in max.
   Referencia: https://docs.python.org/3/library/functions.html#max """


def maximo_libreria(a: float, b: float):
    return (max(a,b))

# NO MODIFICAR - INICIO
assert maximo_libreria(10, 5) == 10
assert maximo_libreria(9, 18) == 18
# NO MODIFICAR - FIN

#######################################################################

"""Re-escribir utilizando el operador ternario.
   Referencia: https://docs.python.org/3/reference/expressions.html#conditional-expressions
   
   "condition_if_true if condition else condition_if_false"
   """

def maximo_ternario(a: float, b: float):
    return a if  a>=b else b


assert maximo_ternario(10, 5) == 10
assert maximo_ternario(9, 18) == 18

#########################################################################

"""EJERCICIO 2"""

"""Comparaciones Encadenadas, Cantidad Arbitraria de Parámetros, Recursividad."""

"""Toma 3 números y devuelve el máximo.
   Restricción: Utilizar UNICAMENTE tres IFs y comparaciones encadenadas.
   Referencia: https://docs.python.org/3/reference/expressions.html#comparisons
   """

def maximo_encadenado(a: float, b: float, c: float):
    if a>=b and a>=c:
        return a

    if c>=a and c>=b:
        return c
    if b>=a and b>=c:
        return b

assert maximo_encadenado(1, 10, 5) == 10
assert maximo_encadenado(4, 9, 18) == 18
assert maximo_encadenado(24, 9, 18) == 24

#############################################################################
"""Re-escribir para que tome 4 parámetros, utilizar la función max.
  Referencia: https://docs.python.org/3/library/functions.html#max"""

def maximo_cuadruple(a: float, b: float, c: float, d: float):
   return (max(a,b,c,d))

assert maximo_cuadruple(1, 10, 5, -5) == 10
assert maximo_cuadruple(4, 9, 18, 6) == 18
assert maximo_cuadruple(24, 9, 18, 20) == 24
assert maximo_cuadruple(24, 9, 18, 30) == 30

###################################################################################

"""Re-escribir para que tome una cantidad arbitraria de parámetros.
    Referencia: https://docs.python.org/3/tutorial/controlflow.html#arbitrary-argument-lists
    """
def maximo_arbitrario(*args):
    return max(*args)

assert maximo_arbitrario(1, 10, 5, -5,10) == 10
assert maximo_arbitrario(4, 9, 18, 6) == 18
assert maximo_arbitrario(24, 9, 18, 20) == 24
assert maximo_arbitrario(24, 9, 18, 30) == 30

#########################################################################################

"""Re-Escribir de forma recursiva."""



#########################################################################################
"""Toma dos números (a, b) y un booleano (multiplicar):
     - Si multiplicar es True: devuelve la multiplicación entre a y b.
     - Si multiplicar es False: devuelve la division entre a y b.
     - Si multiplicar es False y b es cero: devuelve "Operación no válida".
 Restricciones:
     - Utilizar un único return.
     - No utilizar AND ni OR.
 """

def operacion_basica(a: float, b: float, multiplicar: bool):

    if multiplicar:
        x = a*b
    elif b != 0:
        x = a/b

    if multiplicar==False and b == 0:
        x = "Operación no válida"

    return x

print (operacion_basica(0, 5, True))
"""
assert operacion_basica(1, 1, True) == 1
assert operacion_basica(1, 1, False) == 1
assert operacion_basica(25, 5, True) == 125
assert operacion_basica(25, 5, False) == 5
assert operacion_basica(0, 5, True) == 0
assert operacion_basica(0, 5, False) == 0
assert operacion_basica(1, 0, True) == 0
assert operacion_basica(1, 0, False) == "Operación no válida" 
"""



###########################################################################
"""Re-Escribir utilizando tres returns."""

def operacion_multiple (a: float, b: float, multiplicar: bool):
    x =0
    if (multiplicar==True):
        return a*b
    elif b != 0:
        return a/b

    if (x==0):
        return "Operación no válida"

assert operacion_multiple(1, 1, True) == 1
assert operacion_multiple(1, 1, False) == 1
assert operacion_multiple(25, 5, True) == 125
assert operacion_multiple(25, 5, False) == 5
assert operacion_multiple(0, 5, True) == 0
assert operacion_multiple(0, 5, False) == 0
assert operacion_multiple(1, 0, True) == 0
assert operacion_multiple(1, 0, False) == "Operación no válida"

#####################################################################################3
""" EJ 4
Toma un string y devuelve un booleano en base a si letra es una vocal o
    no"""

def es_vocal_if(letra: str):

    if str.lower(letra)=="a":
        return True
    if str.lower(letra) == "e":
        return True
    if str.lower(letra) == "i":
        return True
    if str.lower(letra) == "o":
        return True
    if str.lower(letra) == "u":
        return True

    assert es_vocal_if("a")
    assert not es_vocal_if("b")
    assert es_vocal_if("A")

"""Re-escribir utilizando un sólo IF y el operador IN."""

def es_vocal_if_in(letra: str):
    if str.lower(letra) in "aeiouáéíóú":
        return True

assert es_vocal_if_in("a")
assert not es_vocal_if_in("b")
assert es_vocal_if_in("A")

"""Re-escribir utilizando el operador IN pero sin utilizar IF."""

def es_vocal_in(letra: str):
    return str.lower(letra) in "aeiouáéíóú"

assert es_vocal_in("a")
assert not es_vocal_in("b")
assert es_vocal_in("A")

#################################################################################
""" EJ 5
Toma un lista de números y devuelve el producto todos los númreos. Si
    la lista está vacia debe devolver 0.
    """



def multiplicar_basico(numeros: Iterable[float]):
    acm=1
    if not numeros:
        return 0
    else:
        for num in numeros:
            acm *= num
        return acm


assert multiplicar_basico([1, 2, 3, 4]) == 24
assert multiplicar_basico([2, 5]) == 10
assert multiplicar_basico([]) == 0
assert multiplicar_basico([1, 2, 3, 0, 4, 5]) == 0
assert multiplicar_basico(range(1, 20)) == 121_645_100_408_832_000

#################################################################################################
""" EJ 6
Toma una lista de enteros y strings y devuelve una lista con todos los
    elementos numéricos al final.  """

def numeros_al_final_basico(lista: List[Union[float, str]]) -> List[Union[float, str]]:
    return sorted(lista, key=lambda x: isinstance(x, (int, float)))

assert numeros_al_final_basico([3, "a", 1, "b", 10, "j"]) == ["a", "b", "j", 3, 1, 10]

"""Hacerlo con reduce"""

##############################################################################################
"""EJ 7"""
"""Toma un string y devuelve un booleano en base a si se lee igual al
  derecho y al revés.
  Restricción: No utilizar bucles - Usar Slices de listas.
  Referencia: https://docs.python.org/3/tutorial/introduction.html#lists
  """
def es_palindromo(palabra: str ) ->bool:
    if palabra == palabra[::-1]:  #[start:stop:step]
        return True
    else:
        return False

assert not es_palindromo("amor")
assert es_palindromo("radar")
assert es_palindromo("")

"""Toma un string y devuelve la mitad. Si la longitud es impar, redondear
    hacia arriba"""

def mitad(palabra: str) -> str:
    l = len(palabra)
    m = l // 2
    if l % 2 == 1:
        m += 1
    return palabra[:m]


assert mitad("hello") == "hel"
assert mitad("Moon") == "Mo"
assert mitad("") == ""

####################################################
"""Toma dos listas y devuelve un booleano en base a si tienen al menos 1
    elemento en común.
    Restricción: Utilizar bucles anidados.
    """

def superposicion_basico(lista_1: Iterable[Any], lista_2: Iterable[Any]) -> bool:
    cont= 0
    for l in lista_1:
        for l2 in lista_2:
            if l == l2:
                cont +=1
    if cont > 0:
        return True

test_list = [1, "hello", 35.20]
assert superposicion_basico(test_list, (2, "world", 35.20))
assert not superposicion_basico(test_list, (2, "world", 30.85))

""" Re-Escribir utilizando un sólo bucle y el operador IN """
def superposicion_in(lista_1: Iterable[Any], lista_2: Iterable[Any]) -> bool:
    for l in lista_1:
        if l in lista_2:
            return True

test_list = [1, "hello", 35.20]
assert superposicion_in(test_list, (2, "world", 35.20))
assert not superposicion_in(test_list, (2, "world", 30.85))

"""Re-Escribir utilizando sin bucles, el operador in y la funcion any. """

def superposicion_any(lista_1: Iterable[Any], lista_2: Iterable[Any]) -> bool:
    if any(x in lista_2 for x in lista_1):
        return True
    else:
        return False

test_list = [1, "hello", 35.20]
assert superposicion_any(test_list, (2, "world", 35.20))
assert not superposicion_any(test_list, (2, "world", 30.85))

"""Re-Escribir utilizando conjuntos (sets)"""

def superposicion_set(lista_1: Iterable[Any], lista_2: Iterable[Any]) -> bool:
    lista_1 = set(lista_1)
    lista_2 = set(lista_2)
    return not(lista_1.isdisjoint(lista_2))  #Si no tiene elementos en comun isdisjoint return TRUE

test_list = [1, "hello", 35.20]
assert superposicion_set(test_list, (2, "world", 35.20))
assert not superposicion_set(test_list, (2, "world", 30.85))

###########################################################################
""" EJ 9 
Devuelve la suma de los números de 1 a N.
Restricción: Utilizar un bucle for. """

def sumatoria_basico(n: int) -> int:   #range(start, stop, step) RANGE NO CUENTA EL STOP VALUE
    suma = 0
    for i in range(1, n+1):
        suma += i
    return suma

assert sumatoria_basico(1) == 1
assert sumatoria_basico(100) == 5050

"""Re-Escribir utilizando la función sum y sin usar bucles """

"""!!!!!!!! FALTA TERMINAR !!!!!!!!!"""

#################################################################################################3
""" EJ 10"""
"""Toma una lista y devuelve un booleano en función si tiene al menos un
    número par."""

def tiene_pares_basico(numeros: Iterable[int]) -> bool:

    return any(num % 2 == 0 for num in numeros)

assert tiene_pares_basico([1, 3, 5]) is False
assert tiene_pares_basico([1, 3, 5, 6]) is True
assert tiene_pares_basico([1, 3, 5, 600]) is True

"""Re-Escribir utilizando for-else con dos return y un break."""
def tiene_pares_for_else(numeros: Iterable[int]) -> bool:
    for n in numeros:
        if n % 2 == 0:
            return True
            break
    else:
        return False


assert tiene_pares_for_else([1, 3, 5]) is False
assert tiene_pares_for_else([1, 3, 5, 6]) is True
assert tiene_pares_for_else([1, 3, 5, 600]) is True

#################################################################
""" Re-Escribir utilizando la función any, sin utilizar bucles."""

def tiene_pares_any(numeros: Iterable[int]) -> bool:
    return any(n % 2 ==0 for n in numeros);


assert tiene_pares_any([1, 3, 5]) is False
assert tiene_pares_any([1, 3, 5, 6]) is True
assert tiene_pares_any([1, 3, 5, 600]) is True

###################################################################################################
""" EJ 11"""
""" Toma una lista de números, los eleva al cubo, y devuelve la suma de
    los elementos pares.

    Restricción: Utilizar dos bucles for, uno para elevar al cubo y otro para
    separar los pares. """

def suma_cubo_pares_for(numeros: Iterable[int]) -> int:
    sum = 0
    for n in numeros:
       print(n**3)                                   #Lo eleva al numero que le ponga "**n"
    for n in numeros:
        if n % 2 == 0:
            sum += n**3
    return sum

assert suma_cubo_pares_for([1, 2, 3, 4, 5, 6]) == 288

"""Re-Escribir utilizando comprension de listas (debe resolverse en 1 línea)
y la función built-in sum.

Referencia: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
Referencia: https://docs.python.org/3/library/functions.html#sum
"""
def suma_cubo_pares_sum_list(numeros: Iterable[int]) -> int:
    return sum(x**3 for x in numeros if x % 2 == 0)

assert suma_cubo_pares_sum_list([1, 2, 3, 4, 5, 6]) == 288

""" Re-Escribir utilizando expresiones generadoras (debe resolverse en 1 línea)
  y la función sum.
  Referencia: https://docs.python.org/3/reference/expressions.html#generator-expressions
  """
def suma_cubo_pares_sum_gen(numeros: Iterable[int]) -> int:
    return sum((x**3 for x in numeros if x%2 == 0))

assert suma_cubo_pares_sum_gen([1, 2, 3, 4, 5, 6]) == 288

""" FUNCIONES LAMBDA"""
numeros = [1, 2, 3, 4, 5, 6]

numeros_al_cubo= (x=x**3)