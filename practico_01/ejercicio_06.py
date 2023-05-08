"""Type, Comprensión de Listas, Sorted y Filter."""

from typing import List, Union


def numeros_al_final_basico(lista: List[Union[float, str]]) -> List[Union[float, str]]:
    """Toma una lista de enteros y strings y devuelve una lista con todos los
    elementos numéricos al final.
    """
    lista_str:[str]=[]
    for elem in lista:
        if type(elem) == str:
            lista_str.append(elem)
    lista_num:[float]=[]
    for elem in lista:
        if type(elem) in (float,int):
            lista_num.append(elem)
    return lista_str + lista_num



# NO MODIFICAR - INICIO
assert numeros_al_final_basico([3, "a", 1, "b", 10, "j"]) == ["a", "b", "j", 3, 1, 10]
# NO MODIFICAR - FIN


###############################################################################


def numeros_al_final_comprension(lista: List[Union[float, str]]) -> List[Union[float, str]]:
    """Re-escribir utilizando comprensión de listas."""
    lista_str = [x for x in lista if isinstance(x, str)]
    lista_num = [x for x in lista if isinstance(x, (int, float))]
    return lista_str + lista_num


# NO MODIFICAR - INICIO
assert numeros_al_final_comprension([3, "a", 1, "b", 10, "j"]) == ["a", "b", "j", 3, 1, 10]
# NO MODIFICAR - FIN


###############################################################################


def numeros_al_final_sorted(lista: List[Union[float, str]]) -> List[Union[float, str]]:
    """Re-escribir utilizando la función sorted con una custom key.
    Referencia: https://docs.python.org/3/library/functions.html#sorted
    """
    return sorted(lista,key=lambda x: isinstance(x,(int,float)))


# NO MODIFICAR - INICIO
assert numeros_al_final_sorted([3, "a", 1, "b", 10, "j"]) == ["a", "b", "j", 3, 1, 10]
# NO MODIFICAR - FIN


###############################################################################


def numeros_al_final_filter(lista: List[Union[float, str]]) -> List[Union[float, str]]:
    """CHALLENGE OPCIONAL - Re-escribir utilizando la función filter.
    Referencia: https://docs.python.org/3/library/functions.html#filter
    """
    listaStr = list(filter(lambda elem: isinstance(elem, str), lista))
    listaNum = list(filter(lambda elem: isinstance(elem, (int, float)), lista))
    return listaStr + listaNum


# NO MODIFICAR - INICIO
if __name__ == "__main__":
    assert numeros_al_final_filter([3, "a", 1, "b", 10, "j"]) == ["a", "b", "j", 3, 1, 10]
# NO MODIFICAR - FIN


###############################################################################


def numeros_al_final_recursivo(lista: List[Union[float, str]]) -> List[Union[float, str]]:
    """CHALLENGE OPCIONAL - Re-escribir de forma recursiva."""

    if(len(lista)==1):
        return lista
    lista_reducida = lista[1:]
    if isinstance(lista[0],(float,int)):
        num = lista[0]
        return numeros_al_final_recursivo(lista_reducida).append(num)
    letra = lista[0]
    return [letra] + numeros_al_final_recursivo(lista_reducida)





# NO MODIFICAR - INICIO
if __name__ == "__main__":
    print(numeros_al_final_recursivo([3, "a", 1, "b", 10, "j"]))
    assert numeros_al_final_recursivo([3, "a", 1, "b", 10, "j"]) == ["a", "b", "j", 3, 1, 10]
# NO MODIFICAR - FIN
