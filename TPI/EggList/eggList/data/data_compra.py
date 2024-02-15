from sqlalchemy import and_

from eggList import db
from eggList.models.compra import Compra
from eggList.models.lista_productos import ListaProductos
from sqlalchemy import inspect

def get_compra(id_compra:int):
    return Compra.query.get(id_compra)


def buscar_compra_disponible(lista:ListaProductos) -> Compra:
    compra_disponible:Compra = Compra.query.filter(and_(Compra.id_lista == lista.id, Compra.fecha_compra==None )).first()
    return compra_disponible

def save_compra(compra:Compra, commit:bool = True, flush:bool=False):

    if not compra.id:
        db.session.add(compra)
        if flush:
            db.session.flush(compra)
            db.session.refresh()
    if commit:
        db.session.commit()


def delete_compra(compra:Compra, commit:bool=True):
    db.session.delete(compra)
    if commit:
        db.session.commit()