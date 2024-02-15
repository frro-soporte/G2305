from flask import url_for

from eggList import db
from eggList.models.usuario import Usuario


class GrupoFamiliar(db.Model):
    """
    Clase que representa un grupo familiar dentro del programa
    Es decir, un conjunto de usuarios. Su mayor utilidad es para compartirse las listas
    """
    __tablename__ = "grupos_familiares"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    nombre_familia = db.Column(db.String(50), nullable=False, unique=True)
    imagen_grupo = db.Column(db.String(25), nullable=  False, default = "default.jpg")

    usuarios = db.relationship('Usuario', back_populates="grupo_familiar", foreign_keys = [Usuario.id_grupo_familiar])


    id_admin = db.Column(db.Integer(),db.ForeignKey('usuarios.id'),nullable = False)

    def get_integrantes(self):
        integrantes  = list(filter(lambda user: user.tiene_grupo_familiar(), self.usuarios))
        return integrantes

    def get_invitados(self):
        invitados  = list(filter(lambda user: not user.tiene_grupo_familiar(), self.usuarios))
        return invitados

    def agregar_usuario(self, nuevo_usuario):
        if not isinstance(nuevo_usuario, Usuario):
            raise ValueError
        self.usuarios.append(nuevo_usuario)
        nuevo_usuario.grupo_familiar_id = self.id

    def eliminar_usuario(self, usuario):
        if not isinstance(usuario, Usuario):
            raise ValueError
        try:
            self.usuarios.remove(usuario)
        except ValueError:
            pass
        usuario.id_grupo_familiar = None
        usuario.fecha_confirmacion_grupo = None

    def set_admin(self,nuevo_admin):
        if nuevo_admin not in self.usuarios:
            raise ValueError("EL usuario ingresado no es integrante del grupo ")
        self.id_admin = nuevo_admin.id
        self.admin = nuevo_admin




    def get_img_url(self):
        return url_for('static',filename = "grupo_familiar_pics/"+self.imagen_grupo)
