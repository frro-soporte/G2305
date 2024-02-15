from operator import and_
from typing import List
from datetime import datetime
from flask_login import current_user

from eggList import db
from eggList.models.lista_productos import ListaProductos
from eggList.models.usuario import Usuario
from eggList.models.compra import Compra
from eggList.models.supermercado import Supermercado

from eggList.data import data_lista as data_listas
from sqlalchemy import inspect

def get_user(id:int = None, email:str = None):
    """Funcion para buscar un usuario por uno de los parametros ingresados"""
    if id != None and email != None:
        raise ValueError("Solo se puede realizar la busqueda de una sola forma")

    if id != None:
        return Usuario.query.get(id)
    if email != None:
        return Usuario.query.filter(Usuario.email == email).first()







def get_compras_user(user:Usuario = current_user) -> List[Compra]:
    compras = Compra.query.filter(Compra.id_comprador == user.id).all()
    return compras



def get_compras_user_paginate(supermercado: Supermercado = None,
                              fecha_desde: datetime.date = None,
                              fecha_hasta: datetime.date = None,
                            user:Usuario=current_user,
                              page:int = 1) :
    filtros = (Compra.id_comprador == user.id)



    if supermercado:
        filtros = filtros & (Compra.id_supermercado == supermercado.id)
    if fecha_desde:
        filtros = filtros & (Compra.fecha_compra >= fecha_desde)
    if fecha_hasta:
        filtros = filtros & (Compra.fecha_compra <= fecha_hasta)
    compras = Compra.query.filter(filtros).order_by(Compra.fecha_compra.desc()).paginate(per_page = 5, page = page)

    return compras


def get_ultima_compra(user:Usuario = current_user) -> Compra:
   compras = get_compras_user(user)
   ultima_fecha = max([compra.fecha_compra for compra in compras])
   ultima_compra:Compra = None
   for compra in compras:
       if compra.fecha_compra == ultima_fecha:
           ultima_compra = compra
   return ultima_compra



def get_ultimas_n_compras(n:int, user:Usuario) -> List[Compra]:
    compras= Compra.query.filter(Compra.id_comprador == user.id).order_by(Compra.fecha_compra.desc()).limit(n).all()
    return compras


def get_supermercados_visitados(user:Usuario = current_user) -> List[Supermercado]:
    supermercados_id = db.session.query(Compra.id_supermercado).filter(Compra.id_comprador == user.id).distinct().all()
    supermercados_id = [sup_id[0] for sup_id in supermercados_id]
    supermercados = Supermercado.query.filter(Supermercado.id.in_(supermercados_id)).all()
    return supermercados



def save_user(user:Usuario, commit:bool= True, flush:bool =False) :
    if not user.id:
        db.session.add(user)
        if flush:
            db.session.flush()
            db.session.refresh(user)
    if commit:
        db.session.commit()

