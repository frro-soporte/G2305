import datetime

from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired


class CompraBusquedaForm(FlaskForm):
    fecha_desde = DateField("Fecha Desde", format='%Y-%m-%d')
    fecha_hasta = DateField("Fecha Hasta", format='%Y-%m-%d', validators=[])
    supermercado = SelectField("Supermercado")
    submit = SubmitField("Buscar")



    def validate_fecha_hasta(self, fecha_hasta):
        if fecha_hasta.data :
            try:
                fecha_desde_datetime = datetime.datetime.strptime(self.fecha_hasta.data,"%Y-%m-%d")
                fecha_hasta_datetime = datetime.datetime.strptime(fecha_hasta.data,"%Y-%m-%d")
                if fecha_hasta_datetime < fecha_desde_datetime:
                    raise ValidationError("No ingresó una Fecha hasta valida")
            except Exception:
                pass


