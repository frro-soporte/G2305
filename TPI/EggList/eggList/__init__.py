from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "usuarios.login"
login_manager.login_message_category = "primary"
login_manager.login_message = "Necesitas loguearte para poder acceder a esta página"
mail = Mail()



def create_app(config_file = "config.py"):

    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)
    migrate.init_app(app,db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


    from eggList.models import (ciudad, compra, grupo_familiar, lista_productos, producto,
                                provincia, rol_lista, rol_usuario, supermercado, usuario, usuario_lista, usuarios_roles)


    from eggList.controllers.controller_lista import listas
    from eggList.controllers.controller_usuario import usuarios
    from eggList.controllers.controller_main import main
    from eggList.controllers.controller_grupo_familiar import grupos_familiares
    from eggList.controllers.controller_compra import compras
    from eggList.controllers.controller_provincia import provincias
    from eggList.controllers.error_handler import errores

    app.register_blueprint(listas)
    app.register_blueprint(usuarios)
    app.register_blueprint(main)
    app.register_blueprint(grupos_familiares)
    app.register_blueprint(compras)
    app.register_blueprint(provincias)
    app.register_blueprint(errores)

    return app
