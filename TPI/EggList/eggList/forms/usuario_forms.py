from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, RadioField, FileField
from wtforms.validators import Email, DataRequired, Length, ValidationError, EqualTo, Regexp
import re

from eggList.models.usuario import Usuario
from eggList.models.provincia import Provincia
telefono_regexp = "^[0-9]{2,3}\s?[0-9]{7}$"

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators = [DataRequired()])
    remember = BooleanField('Mantener sesion iniciada')
    submit = SubmitField('Ingresar')


class UserForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min = 3, max = 50)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefono = StringField("Telefono", validators = [DataRequired(),
                                                     Length(min=9, max=12),
                                                     Regexp(telefono_regexp, message="Ingrese [Num. de area sin 0] [telefono sin 15]")]
                                                        )
    password = PasswordField('Contraseña', validators = [DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators = [DataRequired(), EqualTo('password', message="Las contraseñas deben coincidir")])

    submit = SubmitField('Registrarse')





class ActualizarPerfilForm(FlaskForm):

    #Datos personales
    nombre = StringField("Nombre", validators = [DataRequired(), Length(min = 3, max = 50)])
    apellido = StringField("Apellido", validators = [DataRequired(), Length(min=3, max=50)])
    imagen_perfil = FileField('Cambiar imagen', validators=[FileAllowed(['jpg', 'png', 'webp'])])

    #Datos de contacto
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefono = StringField("Telefono", validators = [DataRequired(), Length(min=9, max=12),
                                                     Regexp(telefono_regexp, message="Ingrese [Num. de area sin 0] [telefono sin 15]")])

    #Submit
    submit = SubmitField()

    def validate_email(self, email):
        user = Usuario.query.filter_by(email=email.data).first()
        if user and user.email_confirmed_at and user.email != current_user.email:
            raise ValidationError('Ese correo ya está registrado, por favor elija otro')
