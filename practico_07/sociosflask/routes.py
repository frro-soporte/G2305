from practico_07.sociosflask import app
from flask import render_template, url_for, request, redirect, flash
from practico_07.sociosflask.forms import AltaSocio, ModificacionSocio
from practico_05.ejercicio_01 import Socio
from practico_06.capa_negocio import NegocioSocio, DniRepetido, LongitudInvalida, MaximoAlcanzado

negocioSocio = NegocioSocio()


@app.route("/")
def home():
    socios = negocioSocio.todos()
    return render_template('home.html',socios = socios)

@app.route("/baja/<id_socio>")
def baja(id_socio):
    negocioSocio.baja(int(id_socio))
    return redirect(url_for('home'))

@app.route("/modificacion/<id_socio>", methods = ["GET", "POST"])
def modificacion(id_socio):
    form = ModificacionSocio()
    socio = negocioSocio.buscar(int(id_socio))
    if request.method == "GET":
        form.nombre.data = socio.nombre
        form.apellido.data = socio.apellido
        return render_template('modificacionSocio.html', form = form, socio = socio)
    if request.method == "POST":
        socio_modificado = Socio(
            id = socio.id,
            dni = socio.dni,
            nombre = form.nombre.data,
            apellido = form.apellido.data
        )
        try:
            negocioSocio.modificacion(socio_modificado)
            return redirect(url_for('home'))
        except LongitudInvalida:
            flash(f"""No se cumple con la longitud requerida del nombre y/o apellido. 
                        Minima:{NegocioSocio.MAX_CARACTERES}. 
                        Maxima:{NegocioSocio.MIN_CARACTERES}""", "danger")
            return redirect(url_for('modificacion',id_socio = id_socio))


@app.route("/alta", methods = ["GET", "POST"])
def alta():
    form = AltaSocio()

    if request.method == "GET":
        return render_template('altaSocio.html',form = form)
    if request.method == "POST":
        if form.validate_on_submit():

            socio_nuevo = Socio(dni = form.dni.data,
                                nombre = form.nombre.data,
                                apellido = form.apellido.data
                                )
            try:
                negocioSocio.alta(socio_nuevo)
                return redirect(url_for('home'))

            except DniRepetido:
                flash(f"El dni: '{form.dni.data}' ya está registrado. Por favor ingrese otro", "danger")
                return redirect(url_for('alta'))

            except LongitudInvalida:
                flash(f"""No se cumple con la longitud requerida del nombre y/o apellido. 
                            Minima:{NegocioSocio.MAX_CARACTERES}. 
                            Maxima:{NegocioSocio.MIN_CARACTERES}""", "danger")
                return redirect(url_for('alta'))

            except MaximoAlcanzado:
                flash(f"Se cumplió el cupo de {NegocioSocio.MAX_SOCIOS}. No se pueden inscribir mas socios", "danger")
                return redirect(url_for('home'))





        else:
            return redirect(url_for('alta'))