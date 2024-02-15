from eggList import db


class Producto(db.Model):
    """
    Clase que representa un producto a comprar en un supermercado
    """
    __tablename__ = "productos"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=True)
    cantidad = db.Column(db.Integer())
    esta_en_carrito = db.Column(db.Boolean(), default=False)
    id_lista = db.Column(db.Integer(), db.ForeignKey('listas.id', ondelete ="CASCADE"))
    id_compra = db.Column(db.Integer(), db.ForeignKey('compras.id'))
    id_autor = db.Column(db.Integer(), db.ForeignKey('usuarios.id'), nullable=False)
    autor = db.Relationship('Usuario')

    def get_total(self):
        if self.precio:
            return self.precio * self.cantidad
        return self.cantidad

    def en_carrito(self):
        return self.esta_en_carrito and not self.id_compra


    def poner_en_carrito(self):
        self.esta_en_carrito = True
    def sacar_del_carrito(self):
        self.esta_en_carrito = False
    def agregar_a_lista(self, lista):
        self.id_lista = lista.id

