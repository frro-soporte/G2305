from eggList import db
from eggList.models.producto import Producto


def get_producto(id:int):
    producto = Producto.query.get(id)
    return producto

def save_producto(producto:Producto, commit = True):
    if not producto.id:
        db.session.add(producto)
    if commit:
        db.session.commit()

def delete_producto(producto, commit = True):
    db.session.delete(producto)
    if commit:
        db.session.commit()