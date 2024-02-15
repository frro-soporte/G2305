from typing import List

from flask import Blueprint, render_template, flash, redirect, url_for, abort, request
from flask_login import login_required, current_user
from eggList.forms.grupo_familiar_forms import GrupoFamiliarForm, AgregarUsuarioForm
from eggList.logic.logic_grupo_familiar import UsuarioEnGrupoException, GrupoNoEncontradoException, AdminException
from eggList.models.grupo_familiar import GrupoFamiliar
from eggList.models.usuario import Usuario
from eggList.logic.logic_usuario import user_roles_required, UsuarioNoEncontradoException, ValorUnicoRepetidoException
from eggList.logic import logic_grupo_familiar

grupos_familiares = Blueprint('grupos_familiares',__name__)

@grupos_familiares.route("/grupo_familiar/crear",methods = ["GET","POST"])
@login_required
@user_roles_required("Usuario")
def crear_grupo_familiar():
    form = GrupoFamiliarForm()
    if form.validate_on_submit():
        imagen = form.imagen.data

        grupo = GrupoFamiliar(
            nombre_familia = form.familia.data,
            usuarios = [current_user, ]
        )
        try:
            logic_grupo_familiar.crear_grupo(grupo,imagen)
        except ValorUnicoRepetidoException:
            flash("El nombre ingresado ya se encuentra utilizado","warning")
            return redirect(url_for('crear_grupo_familiar'))
        flash("Su grupo familiar se a creado correctamente", "success")
        return redirect(url_for('grupos_familiares.grupo_familiar'))

    return render_template('grupos_familiares/grupo_familiar_form.html', form=form)

@grupos_familiares.route("/grupo_familiar")
@login_required
@user_roles_required("Usuario")
def grupo_familiar():
    form = AgregarUsuarioForm()
    grupo:GrupoFamiliar = current_user.grupo_familiar
    integrantes = None
    invitados = None
    if grupo:
        integrantes= grupo.get_integrantes()
        invitados = grupo.get_invitados()
    return render_template("grupos_familiares/grupo_familiar.html",form = form, invitados = invitados, integrantes = integrantes)

@grupos_familiares.route("/grupo_familiar/invitar_usuario",methods=["POST"])
@login_required
@user_roles_required("Usuario")
def invitar_usuario():
    form = AgregarUsuarioForm()

    if form.validate_on_submit():
        user = Usuario(email=form.email_usuario.data)
        try:
            logic_grupo_familiar.invitar_usuario(user)


        except UsuarioNoEncontradoException:
            flash("El mail ingresado no existe","danger")
            return redirect(url_for("grupos_familiares.grupo_familiar"))
        except UsuarioEnGrupoException as ex:
            flash(ex.args[0], "info")
            return redirect(url_for("grupos_familiares.grupo_familiar"))
        except AdminException:
            flash("No sos el admin de este grupo","danger")
            abort(403)
        flash(f"Se ha enviado la invitacion a '{user.email}'","primary")
    return redirect(url_for('grupos_familiares.grupo_familiar'))


@grupos_familiares.route("/grupo_familiar/<string:grupo_familiar>/confirmar_usuario/<confirm_token>")
def confirmar_usuario(grupo_familiar, confirm_token):
    grupo = GrupoFamiliar(nombre_familia = grupo_familiar)
    try:
        logic_grupo_familiar.agregar_integrante(grupo,confirm_token)
    except UsuarioNoEncontradoException:
        flash("El usuario ingresado no se encontro", "danger")
        abort(404)
    except GrupoNoEncontradoException:
        flash("El grupo buscado no existe","danger")
        abort(404)
    except UsuarioEnGrupoException as ex:
        flash(ex.args[0], "warning")
        return redirect(url_for("grupos_familiares.grupo_familiar"))
    flash(f"Te has unido satisfactoriamente al grupo familiar '{grupo.nombre_familia}'", "success")
    return redirect(url_for('usuarios.login'))


@grupos_familiares.route("/grupo_familiar/<string:grupo_familiar>/rechazar_invitacion/<string:confirm_token>")
def rechazar_invitacion(grupo_familiar, confirm_token):
    grupo = GrupoFamiliar(nombre_familia = grupo_familiar)
    try:
        logic_grupo_familiar.rechazar_invitacion(grupo,confirm_token)
    except UsuarioNoEncontradoException:
        flash("El usuario ingresado no se encontro", "danger")
        abort(404)
    except GrupoNoEncontradoException:
        flash("El grupo buscado no existe","danger")
        abort(404)
    except UsuarioEnGrupoException as ex:
        flash(ex.args[0], "warning")
        return redirect(url_for("grupos_familiares.grupo_familiar"))
    flash(f"Has rechazado la invitacion del grupo familiar '{grupo.nombre_familia}'", "warning")
    return redirect(url_for('usuarios.login'))

@grupos_familiares.route("/grupo_familiar/eliminar-usuario/<string:email>", methods = ["POST"])
@login_required
@user_roles_required("Usuario")
def eliminar_usuario_grupo(email:str):
    usuario  = Usuario(email = email)
    try:
        logic_grupo_familiar.eliminar_usuario(usuario)
    except GrupoNoEncontradoException:
        flash("No tenes grupo familiar","warning")
        abort(404)
    except AdminException as ex:
        flash(ex.args[0], "warning")
        return redirect(url_for("grupos_familiares.grupo_familiar"))
    except UsuarioNoEncontradoException:
        flash("El usuario ingresado no esta registrado","warning")
        return redirect(url_for("grupos_familiares.grupo_familiar"))
    except UsuarioEnGrupoException:
        flash("El usuario a eliminar no se encuentra en tu grupo","warning")
        return redirect(url_for("grupos_familiares.grupo_familiar"))
    flash(f"Se ha eliminado al usuario {usuario.email}","primary")
    return redirect(url_for("grupos_familiares.grupo_familiar"))


@grupos_familiares.route("/grupo_familiar/editar", methods=["GET","POST"])
@login_required
@user_roles_required("Usuario")
def editar_grupo_familiar():

    form = GrupoFamiliarForm()
    if form.validate_on_submit():
        grupo_modificado = GrupoFamiliar(nombre_familia = form.familia.data)
        imagen = form.imagen.data
        try:
            logic_grupo_familiar.modificar_grupo(grupo_modificado,imagen)
        except AdminException:
            flash("No sos admin de este grupo", "warning")
            abort(403)
        except ValorUnicoRepetidoException:
            flash("El nombre ingresado esta ocupado","warning")
            return redirect(url_for("grupos_familiares.editar_grupo_familiar"))
        flash("El grupo se ha modificado con exito","success")
        return redirect(url_for("grupos_familiares.grupo_familiar"))



    form.familia.data = current_user.grupo_familiar.nombre_familia
    return render_template("/grupos_familiares/grupo_familiar_form.html", form=form,titulo = "Editar grupo familiar")


