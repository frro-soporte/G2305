from typing import List

from flask_login import current_user

from eggList import db
from eggList.models.lista_productos import ListaProductos
from eggList.models.usuario import Usuario
from eggList.models.usuario_lista import UsuarioLista
from sqlalchemy import inspect, and_

def save_usuario_lista(usuario_lista:UsuarioLista, commit:bool = True):
    insp = inspect(usuario_lista)
    if insp.transient:
        db.session.add(usuario_lista)
    if commit:
        db.session.commit()



def buscar_user_lista(lista:ListaProductos, user:Usuario) -> UsuarioLista:
    user_lista = UsuarioLista.query.filter(and_(UsuarioLista.usuario_id == user.id, UsuarioLista.lista_id == lista.id)).first()
    return user_lista
