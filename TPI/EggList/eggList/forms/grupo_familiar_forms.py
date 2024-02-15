from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, ValidationError, Email

from eggList.models.grupo_familiar import GrupoFamiliar
from eggList.models.usuario import Usuario


class GrupoFamiliarForm(FlaskForm):
    familia = StringField('Nombre', validators=[DataRequired(), Length(min=3, max=50)])
    imagen = FileField('Imagen', validators=[FileAllowed(['jpg','jpeg','png', 'webp'])])
    submit = SubmitField('Enviar')




class AgregarUsuarioForm(FlaskForm):
    email_usuario = StringField('Mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Agregar')


