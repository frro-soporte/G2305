
from flask import Blueprint, flash, render_template, redirect, url_for, abort, request
from flask_login import login_required,  current_user, logout_user


from eggList.logic.logic_ciudad import CiudadNoEncontradaException
from eggList.logic.logic_usuario import ValorUnicoRepetidoException, UsuarioNoEncontradoException, \
    ContraseniaInvalidaException, UsuarioNoValidoException
from eggList.forms.usuario_forms import LoginForm, UserForm, ActualizarPerfilForm
from eggList.logic import logic_usuario
from eggList.models.usuario import Usuario

usuarios = Blueprint('usuarios', __name__)


@usuarios.route("/login",methods = ["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user:Usuario = Usuario(email = form.email.data,
                               password = form.password.data
                               )
        try:
            logic_usuario.login_usuario(user=user, recordar= form.remember.data)
        except UsuarioNoEncontradoException:
            flash("El mail ingresado es incorrecto","danger")
            return redirect(url_for('usuarios.login'))
        except UsuarioNoValidoException:
            flash("No verificó el email, por favor intente registrarse denuevo", "danger")
            return redirect(url_for('usuarios.register'))
        except ContraseniaInvalidaException:
            flash("La contraseña ingresada es incorrecta","danger")
            return redirect(url_for('usuarios.login'))

        flash("Se ha logueado correctamente","success")
        return redirect(url_for('main.home'))
    return render_template("usuarios/login.html", form = form)


@usuarios.route("/register",methods = ["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = UserForm()

    if form.validate_on_submit():
        user = Usuario(
            nombre= form.nombre.data,
            apellido = form.apellido.data,
            email = form.email.data,
            telefono = form.telefono.data,
            password = form.password.data,
        )
        try:
            user= logic_usuario.crear_usuario(user)
        except ValorUnicoRepetidoException:
            flash("El mail ya se encuentra registrado","danger")
            return render_template("usuarios/register.html",form = form)
        flash(f"Se ha enviado un correo de verificación a '{user.email}'", "primary")
        return redirect(url_for('main.home'))
    return render_template("/usuarios/register.html", form = form)

@usuarios.route("/confirm_register/<confirm_token>")
def confirm_register(confirm_token):
    try:
        logic_usuario.confirm_user(confirm_token)
    except UsuarioNoEncontradoException:
        flash("Su intento de registro venció, por favor intente de nuevo", "danger")
        return redirect(url_for("usuarios.register"))
    flash("Su usuario se ha registrado correctamente", "success")
    return (redirect(url_for("main.home")))




@usuarios.route("/perfil/<string:usuario_email>")
@login_required
@logic_usuario.user_roles_required("Usuario")
def perfil(usuario_email):
    usuario= logic_usuario.get_user_by_email(usuario_email)
    if not usuario:
        abort(404)

    return render_template("usuarios/perfil.html", usuario = usuario)


@usuarios.route("/perfil/actualizar/<string:usuario_email>", methods=["GET", "POST"])
@login_required
@logic_usuario.user_roles_required("Usuario")
def actualizar(usuario_email):
    form = ActualizarPerfilForm()




    if form.validate_on_submit():
        usuario = Usuario(email = form.email.data,
                          nombre = form.nombre.data,
                          apellido = form.apellido.data,
                          telefono = int(form.telefono.data))
        imagen_perfil = form.imagen_perfil.data
        try:
            logic_usuario.modificar_usuario(usuario, imagen_perfil)
        except UsuarioNoEncontradoException:
            flash("El usuario no se ha encontrado", "danger")
            abort(404)

        flash("Se ha actualizado tu usuario correctamente", "success")
        return redirect(url_for("usuarios.perfil",usuario_email = usuario.email))
    #Si el form no es valido, que muestre la pagina de actualizar perfil tal y como lo venia haciendo
    usuario = logic_usuario.get_user_by_email(usuario_email)
    if not usuario:
        abort(404)
    if usuario != current_user:
        abort(403)

    form.nombre.data = current_user.nombre
    form.apellido.data = current_user.apellido
    form.email.data = current_user.email
    form.telefono.data = current_user.telefono
    return render_template("usuarios/actualizar_perfil.html", usuario=usuario, form=form)


@usuarios.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('main.home'))


@usuarios.route("/set_location/<int:cod_postal>", methods=["POST"])
@login_required
@logic_usuario.user_roles_required("Usuario")
def set_location(cod_postal):
    try:
        logic_usuario.actualizar_ubicacion(cod_postal)
    except CiudadNoEncontradaException:
        flash("La ciudad ingresada no existe", "danger")
        abort(404)
    return redirect(url_for("main.home"))