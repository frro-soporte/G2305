from datetime import datetime

from flask import url_for, current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from eggList import login_manager, db, bcrypt
from eggList.models.rol_usuario import RolUsuario

class Usuario(db.Model, UserMixin):
    """Clase que representa la entidad usuario en el modelo"""
    __tablename__ = "usuarios"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime(), nullable=True)
    telefono = db.Column(db.String(12), nullable = False)
    imagen_perfil = db.Column(db.String(25), nullable=False, default="default.webp")
    password = db.Column(db.String(60), nullable=False)
    fecha_creacion = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())

    roles = db.relationship('RolUsuario', secondary='usuarios_roles')

    id_grupo_familiar = db.Column(db.Integer(), db.ForeignKey('grupos_familiares.id', ondelete = "SET NULL"), nullable=True)
    grupo_familiar = db.relationship('GrupoFamiliar',back_populates="usuarios", foreign_keys = [id_grupo_familiar])
    fecha_confirmacion_grupo = db.Column(db.DateTime(), nullable = True)

    cod_postal =db.Column(db.Integer(),db.ForeignKey("ciudades.cod_postal"), nullable=True)
    ciudad = db.relationship('Ciudad')

    # Posible mapeo a borrar
    listas = db.relationship('ListaProductos', secondary="usuarios_listas", back_populates="usuarios")

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def get_img_url(self):
        return url_for('static',filename = f'profile_pics/{self.imagen_perfil}')

    def has_user_role(self, rol_str: str) -> bool:
        return any([rol_str == rol.name for rol in self.roles])

    def get_id_token(self, expires_sec: int = 1800):
        if not self.id:
            raise AttributeError("Falta el id del usuario")
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def add_user_role(self, role: RolUsuario):
        self.roles.append(role)

    def es_familiar_de(self, user):
        if self.grupo_familiar:
            return user in self.grupo_familiar.usuarios
        return False

    def esta_confirmado(self):
        return bool(self.email_confirmed_at)

    def tiene_grupo_familiar(self):
        return self.id_grupo_familiar and self.fecha_confirmacion_grupo

    def confirmar(self):
        self.email_confirmed_at = datetime.utcnow()

    def check_password(self, password:str):
        return bcrypt.check_password_hash(self.password, password)



@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


