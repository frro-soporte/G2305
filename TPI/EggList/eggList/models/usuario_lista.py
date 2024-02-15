from eggList import db


class UsuarioLista(db.Model):
    """Clase que representa la tabla intermedia entre un usuario y su listas"""
    __tablename__ = 'usuarios_listas'
    usuario_id = db.Column(db.Integer(), db.ForeignKey('usuarios.id', ondelete="CASCADE"), primary_key=True)
    lista_id = db.Column(db.Integer(), db.ForeignKey('listas.id', ondelete="CASCADE"), primary_key=True)
    role_id = db.Column(db.Integer(), db.ForeignKey('roles_en_lista.id'), nullable=False)
    role = db.relationship("RolLista")
