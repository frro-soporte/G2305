from functools import wraps
from datetime import datetime,timedelta
from typing import Optional
import datetime
from flask import current_app, render_template, url_for
from flask_login import current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.datastructures import FileStorage
from flask_login import login_user
from eggList import db, bcrypt
from eggList.logic.logic_ciudad import CiudadNoEncontradaException
from eggList.logic.logic_supermercado import SupermercadoNoEncontradoException
from eggList.models.ciudad import Ciudad
from eggList.models.supermercado import Supermercado
from eggList.models.usuario import Usuario
from eggList.models.rol_usuario import RolUsuario
from eggList.forms.usuario_forms import UserForm
from eggList.utils import send_email, save_profile_picture
from eggList.data import data_usuario, data_supermercado, data_rol_usuario, data_lista, data_ciudad


class UsuarioNoValidoException(Exception):
    pass
class NotExistingRoleException(Exception):
    def __init__(self,msg):
        super.__init__(msg)

class ValorUnicoRepetidoException(Exception):
    pass

class UsuarioNoEncontradoException(Exception):
    pass

class ContraseniaInvalidaException(Exception):
    pass


def verify_id_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token)['user_id']
        user = data_usuario.get_user(id = user_id)
    except:
        return None
    return user

def add_role(user:Usuario, role:str):
    #Privado
    rol = data_rol_usuario.get_role(role)
    if rol:
        user.add_user_role(rol)
    else:
        raise NotExistingRoleException("El rol ingresado no existe")

def confirm_user(token):
    user:Usuario = verify_id_token(token)
    if not user:
        raise UsuarioNoEncontradoException("El token no es válido")
    user.confirmar()
    add_role(user, "Usuario")
    data_usuario.save_user(user, commit=True)


def user_roles_required(*roles):
    """Valida que el usuario actual tenga los roles necesarios"""
    def decorator_function(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated:
                tiene_rol = False
                for rol in roles:
                    tiene_rol = tiene_rol or current_user.has_user_role(rol)
                if tiene_rol:
                    return func(*args, **kwargs)
            return render_template("errores/error_rol.html")
        return wrapper
    return decorator_function

def crear_usuario(user_ingresado: Usuario):
    user: Usuario = data_usuario.get_user(email = user_ingresado.email)
    if user and user.email_confirmed_at:
        raise ValorUnicoRepetidoException("El mail ya se encuentra registrado")

    password_hash = bcrypt.generate_password_hash(user_ingresado.password).decode('utf-8')

    if not user:

        user = Usuario(
            nombre=user_ingresado.nombre,
            apellido=user_ingresado.apellido,
            email=user_ingresado.email,
            telefono=user_ingresado.telefono,
            password=password_hash
        )
        data_usuario.save_user(user,commit=False, flush=True)


    else:
        user.nombre = user_ingresado.nombre
        user.apellido = user_ingresado.apellido
        user.password = password_hash
        user.telefono = user_ingresado.telefono

    send_email(users=[user], title="Creacion de cuenta en EggList",
               body=f"""Usted ha solicitado crear una cuenta en eggList
    Por favor, dirijase al siguiente link si quiere confirmar la cuenta:
    {url_for('usuarios.confirm_register', confirm_token=user.get_id_token(), _external=True)}

    Si no fue usted, por favor, ignore el mensaje
                               """
               )
    data_usuario.save_user(user)
    return user


def actualizar_ubicacion(cod_postal:int):
    ciudad:Ciudad = data_ciudad.get_ciudad(cod_postal)
    if not ciudad:
        raise CiudadNoEncontradaException
    current_user.cod_postal = cod_postal
    data_usuario.save_user(current_user,commit = True)


def modificar_usuario(user_modificado:Usuario, imagen_perfil: Optional[FileStorage]):

    if current_user.email != user_modificado.email:
        raise ValorUnicoRepetidoException("El mail ingresado ya esta usado")
    current_user.nombre = user_modificado.nombre
    current_user.apellido = user_modificado.apellido
    current_user.email = user_modificado.email
    current_user.telefono = user_modificado.telefono
    if imagen_perfil:
        nombre_imagen = save_profile_picture(imagen_perfil)
        current_user.imagen_perfil = nombre_imagen
    data_usuario.save_user(current_user, commit=True)


def get_compras_paginate(supermercado:Optional[Supermercado] = None,
                                     fecha_desde:Optional[datetime.date] = None,
                                     fecha_hasta: Optional[datetime.date] = None,
                                     user:Usuario = current_user,
                                     page:int = 1):

    if supermercado:
        supermercado_busqueda: Supermercado = data_supermercado.get_supermercado(supermercado.id)
        if not supermercado_busqueda:
            raise SupermercadoNoEncontradoException("El supermercado ingresado no existe")
    if fecha_desde and fecha_hasta and fecha_desde>=fecha_hasta:
        raise ValueError("Las fechas ingresadas son incorrectas")

    compras_paginate = data_usuario.get_compras_user_paginate(
        supermercado = supermercado,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        user=user,
        page = page
    )
    return compras_paginate

def login_usuario(user:Usuario, recordar:bool):
    user_encontrado:Usuario = data_usuario.get_user(email = user.email)

    if not user_encontrado:
        raise UsuarioNoEncontradoException
    if not user_encontrado.esta_confirmado():
        raise UsuarioNoValidoException
    if not bcrypt.check_password_hash(pw_hash=user_encontrado.password, password=user.password):
        raise ContraseniaInvalidaException
    login_user(user_encontrado, remember=recordar, duration=datetime.timedelta(minutes=30))







def get_user_by_email(email:str):
    user = data_usuario.get_user(email = email)
    if not user:
        raise UsuarioNoEncontradoException
    return user

def get_user_by_id(id:int):
    user = data_usuario.get_user(id = id)
    if not user:
        raise UsuarioNoEncontradoException
    return user


def get_listas_semanales():
    return data_lista.get_listas_semanales(user= current_user)

def get_ultimas_n_compras(n:int=3, user:Usuario =current_user):
    return data_usuario.get_ultimas_n_compras(n, user)

def get_supermercados_visitados():
    supermercados_visitados = data_usuario.get_supermercados_visitados()
    return supermercados_visitados




