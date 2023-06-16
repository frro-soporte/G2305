from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class AltaSocio(FlaskForm):
    dni =  IntegerField("Dni:", validators=[DataRequired()])
    nombre = StringField("Nombre:", validators=[DataRequired(), Length(min=4, max = 15)])
    apellido = StringField("Apellido:", validators=[DataRequired(), Length(min = 4, max = 15)])
    submit = SubmitField("Guardar!")

class ModificacionSocio(FlaskForm):
    nombre = StringField("Nombre:", validators=[DataRequired(), Length(min=4, max = 15)])
    apellido = StringField("Apellido:", validators=[DataRequired(), Length(min = 4, max = 15)])
    submit = SubmitField("Guardar!")




