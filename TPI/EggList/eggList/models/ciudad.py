from eggList import db


class Ciudad(db.Model):
    __tablename__ = "ciudades"

    cod_postal = db.Column(db.Integer(), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    id_provincia = db.Column(db.Integer(),db.ForeignKey("provincias.id",
                                                        ondelete="CASCADE",
                                                        onupdate = "CASCADE"),nullable = False)
    position_x = db.Column(db.Double(), nullable = False)
    position_y = db.Column(db.Double(), nullable=False)
    min_zoom = db.Column(db.Integer(),nullable = False)


    provincia = db.relationship("Provincia", back_populates="ciudades", )


    def get_coordinates(self):
        return (self.position_x, self.position_y)