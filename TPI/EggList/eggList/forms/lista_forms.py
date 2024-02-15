from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length

from eggList.models.provincia import Provincia


class CrearListaForm(FlaskForm):
    descripcion = StringField('Descripcion', validators = [DataRequired(),Length(min = 3, max = 100)])
    incluye_grupo_familiar = BooleanField('Incluye grupo familiar')
    submit = SubmitField('Crear Lista')



class EnSupermercadoForm(FlaskForm):

    supermercado = SelectField("Supermercado", validate_choice = True)
    submit = SubmitField("En Supermercado")
