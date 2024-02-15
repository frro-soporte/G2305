from datetime import datetime, timedelta
from typing import Optional, List

from eggList import db
from eggList.models.lista_productos import ListaProductos
from eggList.models.rol_lista import RolLista
from eggList.models.usuario import Usuario
from sqlalchemy import inspect

from eggList.models.usuario_lista import UsuarioLista


def save_lista(lista:ListaProductos,usuarios_lista:List[UsuarioLista]=None,commit:bool = True, flush:bool=False ):

    if not lista.id:
        db.session.add(lista)
    if usuarios_lista:
        db.session.add_all(usuarios_lista)
    if commit:
        db.session.commit()
    if flush:
        db.session.flush()
        db.session.refresh(lista)
        return lista


def get_lista(id:int):
    return ListaProductos.query.get(id)

def get_rol_lista(rol_lista:str):
    return RolLista.query.filter(RolLista.name == rol_lista).first()
def get_listas_semanales(user:Optional[Usuario] = None,
                         semanas_de_antelacion:int = 1):
    """Retorna todas las listas que se crearon esta semana"""
    este_lunes = datetime.utcnow() - timedelta(days=semanas_de_antelacion*datetime.utcnow().weekday(),
                                               hours=datetime.utcnow().hour,
                                               minutes=datetime.utcnow().minute,
                                               seconds=datetime.utcnow().second)
    listas_semanales = ListaProductos.query \
        .filter(ListaProductos.fecha_creacion > este_lunes) \
        .order_by(ListaProductos.fecha_creacion.desc()).all()
    if user:
        listas_semanales = list(filter(lambda lista: lista.es_usuario_valido(user),listas_semanales))

    return listas_semanales