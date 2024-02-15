from typing import List, Tuple

from flask_login import current_user

from eggList import db
from eggList.data import data_compra, data_supermercado, data_ciudad, data_producto
from eggList.logic.logic_supermercado import SupermercadoNoEncontradoException
from eggList.logic.logic_usuario import UsuarioNoValidoException
from eggList.models.lista_productos import ListaProductos
from eggList.models.producto import Producto
from eggList.models.usuario_lista import UsuarioLista
from eggList.models.usuario import Usuario
from eggList.models.rol_lista import RolLista
from eggList.models.compra import Compra
from eggList.models.supermercado import Supermercado
import eggList.data.data_lista as data_lista
from eggList.data import data_usuario_lista
from eggList.utils import send_email


class ListaNoEncontradaException(Exception):
    pass
class RolListaNoEncontrado(Exception):
    pass

class UsuarioNoEnListaException(Exception):
    pass

class CarritoSinProductosException(Exception):
    pass

class RolEnListaException(Exception):
    pass
class ListaEnCompraException(Exception):
    pass

class CompraNoEncontradaException(Exception):
    pass

class CompraNotFoundException(Exception):
    pass

"""FUnciones de roles"""
def buscar_rol_usuario_en_lista(lista: ListaProductos) -> RolLista:
    #Metodo privado
    user_lista = data_usuario_lista.buscar_user_lista(lista)
    return user_lista.role


def user_has_list_role(lista: ListaProductos,  rol_lista_str: str = "Armador",user:Usuario = current_user)-> bool:
    #Metodo privado
    user_lista = data_usuario_lista.buscar_user_lista(lista, user)
    return user_lista.role.name == rol_lista_str


"""querys"""
def get_lista(id:int):
    lista_encontrada = data_lista.get_lista(id)
    if not lista_encontrada:
        raise ListaNoEncontradaException("La lista no se ha encontrado")
    if not lista_encontrada.es_usuario_valido(current_user):
        raise UsuarioNoEnListaException("El usuario no esta en la lista")

    return lista_encontrada


def get_lista_with_role(id:int) -> Tuple[ListaProductos, bool]:
    #Es una extension de get_lista
    lista_encontrada = get_lista(id)
    es_comprador = user_has_list_role(lista_encontrada, "Comprador")
    return (lista_encontrada,es_comprador)




def get_listas_por_semana():
    listas = current_user.listas[::-1]
    listas_por_semana = []
    if listas:
        semana = listas[0].get_semana()
        listas_por_semana = [(semana, [])]
        index = 0
        for lista in listas:
            if lista.get_semana() == semana:
                listas_por_semana[index][1].append(lista)
            else:
                semana = lista.get_semana()
                listas_por_semana.append((semana, [lista]))
                index += 1
    return listas_por_semana
def agregar_producto(lista: ListaProductos, producto: Producto):
    lista_encontrada = data_lista.get_lista(lista.id)
    if not lista_encontrada:
        raise ListaNoEncontradaException

    producto.agregar_a_lista(lista)
    data_producto.save_producto(producto,commit =True)


def crear_lista(lista: ListaProductos, incluye_grupo_familiar:bool):



    #Damos un flush ya que necesitamos el id de la lista para poder
    #Asignarselo al usuario lista
    data_lista.save_lista(lista, commit=False, flush=True)
    rol_armador = data_lista.get_rol_lista("Armador")
    usuarios = []
    if incluye_grupo_familiar and current_user.grupo_familiar:
        usuarios += current_user.grupo_familiar.get_integrantes()
    else:
        usuarios.append(current_user)
    usuarios_lista = []
    for usuario in usuarios:
        usuario_lista = UsuarioLista(usuario_id=usuario.id,
                                    lista_id=lista.id,
                                    role=rol_armador)
        usuarios_lista.append(usuario_lista)


    data_lista.save_lista(lista, usuarios_lista=usuarios_lista, commit=True)
    send_email(users=usuarios, title=f"Se ha creado la lista {lista.descripcion}",
               body=f"""{current_user.nombre + current_user.apellido} ha creado la lista {lista.descripcion}  """)




def actualizar_rol(lista: ListaProductos, rol_lista_str: str ,user:Usuario = current_user):
    #metodo privado
    rol_lista = data_lista.get_rol_lista(rol_lista_str)
    if not rol_lista:
        raise RolListaNoEncontrado

    user_lista = data_usuario_lista.buscar_user_lista(lista,user)
    if not user_lista:
        raise UsuarioNoEnListaException
    if rol_lista and user_lista:
        user_lista.role = rol_lista
        data_usuario_lista.save_usuario_lista(user_lista, commit=False)

def actualizar_roles(lista: ListaProductos, rol_lista_str: str, usuarios:List[Usuario]):
    #metodo privado
    rol_lista = data_lista.get_rol_lista(rol_lista_str)
    if not rol_lista:
        raise RolListaNoEncontrado
    for user in usuarios:
        user_lista = data_usuario_lista.buscar_user_lista(lista,user)
        if not user_lista:
            raise UsuarioNoEnListaException
        user_lista.role = rol_lista
        data_usuario_lista.save_usuario_lista(user_lista, commit=False)

def en_supermercado(lista:ListaProductos, supermercado:Supermercado):
    lista_obj = data_lista.get_lista(lista.id)
    if not lista_obj:
        raise ListaNoEncontradaException("La lista ingresada no se encontró")
    supermercado_obj = data_supermercado.get_supermercado(supermercado.id)
    if not supermercado_obj:
        raise SupermercadoNoEncontradoException("EL supermercado ingresado no se encontró")
    hay_compradores = any([user_has_list_role(lista,"Comprador",user=usr) for usr in lista.usuarios])
    if hay_compradores:
        raise ListaEnCompraException("La lista ya se encuentra el compra")
    compra = data_compra.buscar_compra_disponible(lista)

    actualizar_rol(lista_obj, "Comprador")

    if not compra:
        compra = Compra(id_lista = lista.id, id_supermercado = supermercado.id)
    data_compra.save_compra(compra, commit=True)


def buscar_compra_disponible(lista:ListaProductos):
    compra = data_compra.buscar_compra_disponible(lista)

    return compra

def salir_del_super(lista_id:int):
    lista_encontrada = data_lista.get_lista(id=lista_id)



    actualizar_rol(lista_encontrada, "Armador")



    #Si el ultimo comprador sale de la lista, borra la compra
    if (not any([user_has_list_role(lista=lista_encontrada, rol_lista_str="Comprador", user=user)
                 and user != current_user for user in lista_encontrada.usuarios])):
        compra_disponible = data_compra.buscar_compra_disponible(lista_encontrada)
        data_compra.delete_compra(compra_disponible,commit=False)
    lista_encontrada.sacar_productos_de_carrito()
    data_lista.save_lista(lista_encontrada, commit=True)
    return lista_encontrada





def comprar(lista:ListaProductos):
    lista_encontrada = data_lista.get_lista(lista.id)
    if not lista_encontrada:
        raise ListaNoEncontradaException
    compra_disponible = data_compra.buscar_compra_disponible(lista_encontrada)
    if not compra_disponible:
        raise CompraNoEncontradaException
    if not user_has_list_role(lista_encontrada, "Comprador"):
        raise RolEnListaException

    productos_en_carrito = list(
        filter(lambda producto: producto.en_carrito(), lista_encontrada.productos))
    compra_disponible.comprar(productos_en_carrito)
    actualizar_roles(lista_encontrada, "Armador",lista_encontrada.usuarios)

    data_compra.save_compra(compra_disponible, commit = True)



def get_compra(id_compra:int):
    compra = data_compra.get_compra(id_compra)
    if not compra:
        raise CompraNotFoundException("No se encontro la compra ingresada")
    if not compra.es_usuario_valido(current_user):
        raise UsuarioNoValidoException("El usuario ingresado no puede acceder a la lista")
    return compra


class ProductoNoEncontradoException(Exception):
    pass


def get_producto(id:int):
    prod = data_producto.get_producto(id)
    if not prod:
        raise ProductoNoEncontradoException
    return prod


def poner_en_carrito(producto:Producto):
    producto_encontrado:Producto = data_producto.get_producto(producto.id)
    if not producto_encontrado:
        raise ProductoNoEncontradoException
    producto_encontrado.cantidad = producto.cantidad
    producto_encontrado.precio = producto.precio
    lista = ListaProductos(id = producto_encontrado.id_lista)
    if not user_has_list_role(lista, "Comprador"):
        raise RolEnListaException
    producto_encontrado.poner_en_carrito()
    data_producto.save_producto(producto,commit=True)
    return producto_encontrado


def sacar_de_carrito(producto:Producto):
    producto_encontrado = data_producto.get_producto(producto.id)
    if not producto_encontrado:
        raise ProductoNoEncontradoException
    lista = ListaProductos(id=producto_encontrado.id_lista)
    if not user_has_list_role(lista, "Comprador"):
        raise RolEnListaException
    producto_encontrado.sacar_del_carrito()
    data_producto.save_producto(producto, commit=True)
    return producto_encontrado


def modificar_producto(producto:Producto):
    #No hay ninguna validacion para realizar(por ahora)
    data_producto.save_producto(producto, commit=True)


def borrar_producto(producto):
    producto_encontrado = data_producto.get_producto(producto.id)
    if not producto_encontrado:
        raise ProductoNoEncontradoException
    data_producto.delete_producto(producto_encontrado, commit=True)
    return producto_encontrado
