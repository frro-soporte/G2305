import datetime
from typing import Optional

from flask import url_for
from flask_login import current_user
from werkzeug.datastructures.file_storage import FileStorage

from eggList import db
from eggList.data import data_grupo_familiar, data_usuario
from eggList.logic import logic_usuario
from eggList.logic.logic_usuario import UsuarioNoEncontradoException, ValorUnicoRepetidoException
from eggList.models.grupo_familiar import GrupoFamiliar
from eggList.models.usuario import Usuario
from eggList.utils import save_family_picture, send_email


class UsuarioEnGrupoException(Exception):
    pass
class GrupoNoEncontradoException(Exception):
    pass


class AdminException(Exception):
    pass

def crear_grupo(grupo:GrupoFamiliar, imagen: FileStorage):
    # Validamos que el nombre no se repita
    grupo_existente = data_grupo_familiar.get_grupo_familiar(nombre = grupo.nombre_familia)
    if grupo_existente:
        raise ValorUnicoRepetidoException


    #Si se ingresó una imagen, se guarda y se le asigna el nombre a la propiedadn imagen_grupo del grupo familiar
    #Caso contrario, se le asigna el default desde la base de datos
    imagen_nombre = None
    if imagen:
        imagen_nombre = save_family_picture(imagen)
        grupo.imagen_grupo = imagen_nombre
    grupo.agregar_usuario(current_user)
    grupo.set_admin(current_user)
    current_user.fecha_confirmacion_grupo = datetime.datetime.now()


    data_grupo_familiar.save_grupo_familiar(grupo)


def get_grupo_by_nombre(nombre: str):
    return data_grupo_familiar.get_grupo_familiar(nombre = nombre)


def invitar_usuario(user:Usuario):
    usuario_a_invitar:Usuario = data_usuario.get_user(email = user.email)
    if not usuario_a_invitar or not usuario_a_invitar.esta_confirmado():
        raise UsuarioNoEncontradoException

    if current_user == usuario_a_invitar:
        raise UsuarioEnGrupoException("Ya te encuentras en el grupo")

    if usuario_a_invitar.tiene_grupo_familiar():
        raise UsuarioEnGrupoException("El usuario ya posee un grupo")
    grupo:GrupoFamiliar = current_user.grupo_familiar
    if grupo.id_admin != current_user.id:
        raise AdminException
    #Lo agregamos a la lista de usuarios, pero no lo confirmamos
    grupo.agregar_usuario(usuario_a_invitar)

    data_grupo_familiar.save_grupo_familiar(grupo, commit=True)

    send_email([usuario_a_invitar],
               title=f"'{current_user.nombre} {current_user.apellido}' te ha invitado de su grupo familiar",
               body=f"""Si desea unirse al grupo familiar '{current_user.grupo_familiar.nombre_familia}', dirijase al siguiente link
        {url_for('grupos_familiares.confirmar_usuario', grupo_familiar=current_user.grupo_familiar.nombre_familia, confirm_token=usuario_a_invitar.get_id_token(), _external=True)}                   

        Si desea rechazar la invitacion, ingrese al siguiente link
        {url_for('grupos_familiares.rechazar_invitacion', grupo_familiar=current_user.grupo_familiar.nombre_familia, confirm_token=usuario_a_invitar.get_id_token(), _external=True)}  
        """)

def agregar_integrante(grupo:GrupoFamiliar, token:str):
    user:Usuario = logic_usuario.verify_id_token(token)
    grupo = data_grupo_familiar.get_grupo_familiar(nombre=grupo.nombre_familia)
    if  not grupo:
        raise GrupoNoEncontradoException("El ingresado no se encontro")
    if not user:
        raise UsuarioNoEncontradoException("El usuario ingresado no se encontro")
    if not user.grupo_familiar:
        raise UsuarioEnGrupoException(f"{user.email} no fue invitado a este grupo o su invitacion fue revocada")

    if user.tiene_grupo_familiar():
        raise UsuarioEnGrupoException(f"{user.email} ya tiene grupo")

    user.fecha_confirmacion_grupo = datetime.datetime.now()
    data_grupo_familiar.save_grupo_familiar(grupo,commit=True)


def modificar_grupo(grupo_modificado:GrupoFamiliar,imagen:Optional[FileStorage]):
    grupo:GrupoFamiliar = current_user.grupo_familiar
    if current_user.id != grupo.id_admin:
        raise AdminException
    grupo_existente:GrupoFamiliar = data_grupo_familiar.get_grupo_familiar(nombre=grupo_modificado.nombre_familia)
    if grupo_existente and grupo_existente.nombre_familia != grupo_modificado.nombre_familia:
        raise ValorUnicoRepetidoException
    grupo.nombre_familia =grupo_modificado.nombre_familia
    if imagen:
        grupo.imagen_grupo = save_family_picture(imagen)

    data_grupo_familiar.save_grupo_familiar(grupo, commit=True)




def rechazar_invitacion(grupo_familiar:GrupoFamiliar,confirm_token:str):
    grupo: GrupoFamiliar = data_grupo_familiar.get_grupo_familiar(nombre=grupo_familiar.nombre_familia)
    if not grupo:
        raise GrupoNoEncontradoException
    usuario_a_eliminar:Usuario = logic_usuario.verify_id_token(confirm_token)


    if not usuario_a_eliminar or not usuario_a_eliminar.esta_confirmado():
        raise UsuarioNoEncontradoException("El usuario no existe")



    grupo_familiar.eliminar_usuario(usuario_a_eliminar)
    data_grupo_familiar.save_grupo_familiar(grupo, commit=True)
def eliminar_usuario(user:Usuario):
    grupo_familiar: GrupoFamiliar = current_user.grupo_familiar
    if not grupo_familiar:
        raise GrupoNoEncontradoException
    if current_user.id != grupo_familiar.id_admin:
        raise AdminException("No sos admin del grupo")
    usuario_a_eliminar:Usuario = data_usuario.get_user(email = user.email)


    if not usuario_a_eliminar or not usuario_a_eliminar.esta_confirmado():
        raise UsuarioNoEncontradoException("El usuario no existe")

    #Si el usuario no se encuentra en el grupo
    if usuario_a_eliminar not in grupo_familiar.usuarios:
        raise UsuarioEnGrupoException("El usuario no se encuentra en el grupo")
    if usuario_a_eliminar.id == grupo_familiar.id_admin:
        raise AdminException("El usuario ingresado es admin")
    grupo_familiar.eliminar_usuario(usuario_a_eliminar)
    data_grupo_familiar.save_grupo_familiar(grupo_familiar, commit=True)

