from datetime import datetime, timedelta
from typing import List

from eggList import db
from eggList.models.producto import Producto


class ListaProductos(db.Model):
    """
    Clase que representa un lista de supermercado que contiene productos
    """
    __tablename__ = "listas"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(100), nullable=False)
    fecha_creacion = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())
    id_autor = db.Column(db.Integer(), db.ForeignKey('usuarios.id'), nullable=False)
    autor = db.relationship('Usuario')
    usuarios = db.relationship('Usuario', secondary="usuarios_listas", back_populates="listas")
    productos = db.relationship('Producto')

    def __str__(self):
        return f"ListaProductos<fecha_creacion: {self.fecha_creacion} -- autor: {self.autor.nombre} {self.autor.apellido}>"

    def sacar_productos_de_carrito(self):
        for prod in self.productos:
            if not prod.id_compra:
                prod.sacar_del_carrito()
    def agregar_producto(self, producto: Producto):
        self.productos.append(producto)

    def agregar_usuarios(self, usuarios_nuevos:List):
        self.usuarios = self.usuarios+ usuarios_nuevos

    def get_total(self):
        total = 0
        for producto in self.productos:
            if producto.esta_en_carrito and producto.precio and not producto.id_compra:
                total += producto.get_total()
        return total

    def get_semana(self):
        return self.fecha_creacion.date() - timedelta(days=self.fecha_creacion.weekday())

    def es_usuario_valido(self, user):
        es_usuario = user in self.usuarios
        return es_usuario

    def faltan_productos(self):
        return any([bool(prod.id_compra) and not prod.esta_en_carrito for prod in self.productos])


