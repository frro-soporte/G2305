from eggList import db


class Provincia(db.Model):
    __tablename__ = "provincias"

    id = db.Column(db.Integer(),primary_key = True, autoincrement = True)
    nombre = db.Column(db.String(100),nullable = False)
    ciudades = db.relationship("Ciudad",back_populates = "provincia")
