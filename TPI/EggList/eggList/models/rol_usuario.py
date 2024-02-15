from eggList import db


class RolUsuario(db.Model):
    """Clase que representa el rol del usuario en el programa(NO EN UNA LISTA)"""
    __tablename__ = "roles"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)

    def es_rol(self, rol: str):
        return self.name == rol

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<RolUsuario {self.name}>"
