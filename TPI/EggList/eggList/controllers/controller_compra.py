import datetime
from typing import List

from flask import Blueprint, render_template, request, flash, abort, redirect, url_for
from flask_login import login_required, current_user

import eggList.logic.logic_lista
from eggList.forms.compra_forms import CompraBusquedaForm
from eggList.logic import logic_usuario
from eggList.logic.logic_lista import CompraNoEncontradaException
from eggList.logic.logic_supermercado import SupermercadoNoEncontradoException
from eggList.models.compra import Compra
from eggList.models.supermercado import Supermercado
from eggList.logic.logic_usuario import user_roles_required, UsuarioNoValidoException

compras = Blueprint('compras', __name__)

@compras.route("/compras/mis-compras")
@login_required
@user_roles_required("Usuario")
def mis_compras():
    page = request.args.get('page', 1, type=int)
    form = CompraBusquedaForm()
    fecha_desde_str = request.args.get('fecha_desde', type=str)
    fecha_hasta_str = request.args.get('fecha_hasta', type=str)
    supermercado_id = request.args.get('supermercado', type=int)

    supermercados = logic_usuario.get_supermercados_visitados()
    form.supermercado.choices = [(0, "Cualquiera")]
    form.supermercado.choices += [(super.id, str(super)) for super in supermercados]
    compras:List[Compra]

    supermercado = None
    fecha_desde = None
    fecha_hasta = None

    if supermercado_id:
        supermercado = Supermercado(id = supermercado_id)
    if fecha_desde_str:
          fecha_desde = datetime.datetime.strptime(fecha_desde_str,'%Y-%m-%d')
    if fecha_hasta_str:
        fecha_hasta = datetime.datetime.strptime(fecha_hasta_str,'%Y-%m-%d') + datetime.timedelta(days = 1)

    try:
        compras = logic_usuario.get_compras_paginate(fecha_desde=fecha_desde, fecha_hasta=fecha_hasta,
                                                                   page=page, supermercado = supermercado)
    except SupermercadoNoEncontradoException:
        flash("El supermercado ingresado no existe","danger")
        return render_template("compras/mis-compras.html",compras = None,  form = form)
    except ValueError:
        flash("La fecha de inicio es mayor a la fecha de fin","danger")
        return render_template("compras/mis-compras.html", compras = None,  form=form)

    return render_template("compras/mis-compras.html", compras = compras, form = form)



@compras.route("/compras/compra/<int:id_compra>")
@login_required
@user_roles_required("Usuario")
def compra(id_compra:int):
    compra = None

    try:
        compra = eggList.logic.logic_lista.get_compra(id_compra)
    except CompraNoEncontradaException:
        flash("La compra ingresada no existe","warning")
        abort(404)
    except UsuarioNoValidoException:
        flash("No tiene permisos para acceder a esta compra","warning")
        abort(403)


    return render_template("/compras/compra.html", compra = compra)