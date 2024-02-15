from eggList import db


class RolLista(db.Model):
    """Clase que representa el rol de un usuario dentro de una lista"""
    __tablename__ = "roles_en_lista"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<RolLista {self.name}>"

    def __eq__(self, other):
        return self.name == other.name

    def es_rol(self, rol: str):
        return self.name == rol
