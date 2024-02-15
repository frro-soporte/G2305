from datetime import datetime
from typing import List

from flask_login import current_user

from eggList import db
from eggList.models.producto import Producto


class Compra(db.Model):
    __tablename__ = "compras"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    fecha_compra = db.Column(db.DateTime(),nullable = True)
    productos = db.relationship("Producto")
    id_comprador = db.Column(db.Integer(), db.ForeignKey("usuarios.id"),nullable = True)
    id_lista = db.Column(db.Integer(), db.ForeignKey("listas.id"), nullable =False)
    id_supermercado = db.Column(db.Integer, db.ForeignKey("supermercados.id"), nullable = False)
    supermercado = db.relationship("Supermercado")


    def comprar(self, productos: List[Producto]):
        self.id_comprador = current_user.id
        self.fecha_compra = datetime.utcnow()
        for producto in productos:
            producto.id_compra = self.id

    def fue_comprado(self):
        return bool(self.fecha_compra)

    def es_usuario_valido(self, user):
        """Funcion que retorna un booleano dependiendo si el usuario puede acceder o no a la compra"""
        #Mas adelante tengo pensado poner que se pueda acceder a una compra desde el grupo familiar
        return self.id_comprador == user.id

    def get_total(self):
        return sum([prod.precio * prod.cantidad for prod in self.productos])
