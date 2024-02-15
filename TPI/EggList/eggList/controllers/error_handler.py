import werkzeug.exceptions
from flask import Blueprint, render_template

errores = Blueprint('errores', __name__)

@errores.app_errorhandler(403)
def error_403(error):
    return render_template('errores/403.html'),403

@errores.app_errorhandler(404)
def error_404(error):
    return render_template('errores/404.html'),404


@errores.app_errorhandler(500)
def internal_server_error(error):

    return render_template("errores/500.html"), 500



