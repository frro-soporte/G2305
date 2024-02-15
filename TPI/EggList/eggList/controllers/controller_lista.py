from typing import List

from flask import Blueprint, render_template, flash, redirect, url_for, abort, request
from flask_login import login_required, current_user

import eggList.logic.logic_lista
from eggList.forms.lista_forms import CrearListaForm, EnSupermercadoForm
from eggList.models.lista_productos import ListaProductos
from eggList.models.producto import Producto
from eggList.models.supermercado import Supermercado
from eggList.models.ciudad import Ciudad
from eggList.forms.producto_form import AgregarProductoForm, CarritoForm, ModificarProductoForm
from eggList.utils import send_email, generate_map
from eggList.logic.logic_usuario import user_roles_required
from eggList.logic import logic_lista, logic_supermercado
from eggList.logic.logic_lista import (ListaNoEncontradaException, UsuarioNoEnListaException, RolEnListaException
, CarritoSinProductosException, ProductoNoEncontradoException
                                       )
listas = Blueprint('listas', __name__)


@listas.route("/lista/mis-listas")
@login_required
@user_roles_required("Usuario")
def mis_listas():
    listas_por_semana = logic_lista.get_listas_por_semana()
    return render_template("listas/mis_listas.html", listas_por_semana = listas_por_semana)




@listas.route("/lista/crear", methods = ["GET","POST"])
@login_required
@user_roles_required("Usuario")
def crear_lista():
    form = CrearListaForm()
    if form.validate_on_submit():
        usuarios = []
        incluye_grupo_familiar = form.incluye_grupo_familiar.data


        lista = ListaProductos(
            descripcion = form.descripcion.data,
            autor = current_user
        )
        logic_lista.crear_lista(lista,incluye_grupo_familiar)
        send_email(users = lista.usuarios, title = f"Se ha creado la lista {lista.descripcion}",
                   body = f"""Se ha creado la lista {lista.descripcion}             
                   
                   """)
        flash("Su lista se ha agregado correctamente","success")
        return redirect(url_for("listas.mis_listas"))
    return render_template("/listas/crear_lista_form.html", form = form)

@listas.route("/lista/<int:lista_id>")
@login_required
@user_roles_required("Usuario")
def lista(lista_id):

    try:
        (lista, es_comprador) = logic_lista.get_lista_with_role(lista_id)


    except ListaNoEncontradaException:
        flash("La lista ingresada no se encontró","danger")
        abort(404)
    except UsuarioNoEnListaException:
        flash("Usted no es usuario de esta lista","warning")
        abort(403)
    #Compra disponible puede tirar una excepcion de que no se encontra compra disponible
    compra_disponible = logic_lista.buscar_compra_disponible(lista)
    if es_comprador:
        form_carrito = CarritoForm()


        productos_disponibles = list(filter(lambda producto: not producto.id_compra, lista.productos))
        productos_en_carrito = []
        productos_fuera_de_carrito = []
        for producto in productos_disponibles:
            if producto.esta_en_carrito:
                productos_en_carrito.append(producto)
            else:
                productos_fuera_de_carrito.append(producto)
        total = lista.get_total()
        return render_template("listas/lista_comprador.html", lista=lista,
                               productos_en_carrito=productos_en_carrito,
                               productos_fuera_de_carrito=productos_fuera_de_carrito,
                               form_carrito=form_carrito, total=total, compra=compra_disponible)


    else:
        form = EnSupermercadoForm()

        ciudad_user: Ciudad = current_user.ciudad
        supermercados: List[Supermercado] = logic_supermercado.get_supermercados_by_ciudad(cod_postal=ciudad_user.cod_postal)

        """Problema con map script, por ahora no voy a mostrar mapa"""
        (map_header, map_body, map_script) = None, None, None
        #(map_header, map_body, map_script) = generate_map(ciudad= ciudad_user, supermercados= supermercados)
        form.supermercado.choices = [(super.id, super.nombre) for super in supermercados]
        lista.productos.sort(key=lambda producto: bool(producto.id_compra))
        return render_template("listas/lista_armador.html", lista=lista,
                               supermercados=supermercados, form_super=form,
                               ciudad_user=ciudad_user, en_compra=bool(compra_disponible),
                               map_header = map_header, map_body = map_body, map_script = map_script)






@listas.route("/lista/<int:lista_id>/en_supermercado/<int:supermercado_id>", methods = ["POST"])
@login_required
@user_roles_required("Usuario")
def en_supermercado(lista_id, supermercado_id):
    lista = ListaProductos(id = lista_id)
    supermercado = Supermercado(id = supermercado_id)
    logic_lista.en_supermercado(lista, supermercado)
    return redirect(url_for("listas.lista",lista_id = lista.id))


@listas.route("/lista/<int:lista_id>/agregar", methods = ["GET","POST"])
@login_required
@user_roles_required("Usuario")
def agregar_producto(lista_id):
    form = AgregarProductoForm()
    if request.method == "GET":
        lista = None
        try:
            lista = logic_lista.get_lista(lista_id)
        except ListaNoEncontradaException:
            flash("La lista no existe")
            abort(404)
        except UsuarioNoEnListaException:
            flash("No podes acceder a esta lista")
            abort(403)
        return render_template('productos/agregar_producto_form.html', form=form, lista_id=lista.id)
    if form.validate_on_submit():
        lista = ListaProductos(id = lista_id)
        producto = Producto(descripcion=form.descripcion.data,
                            cantidad=form.cantidad.data if form.cantidad.data != 0 else None,
                            autor = current_user)
        logic_lista.agregar_producto(lista, producto)
        flash(f'Se agregó correctamente el producto {producto.descripcion} a tu lista!', "success")
        return redirect(url_for('listas.lista', lista_id = lista.id))




@listas.route("/lista/<int:lista_id>/comprar")
@login_required
@user_roles_required("Usuario")
def comprar(lista_id):
        lista = ListaProductos(id = lista_id)
        try:
            eggList.logic.logic_lista.comprar(lista)
        except logic_lista.ListaNoEncontradaException:
            flash("La lista no se ha encontrado", "danger")
            return abort(404)

        except RolEnListaException:
            flash("No es comprador de esta lista","danger")
            return redirect(url_for("listas.lista", lista_id=lista.id))

        return redirect(url_for("listas.lista", lista_id = lista.id))

@listas.route("/listas/<int:lista_id>/salir_del_super")
@login_required
@user_roles_required("Usuario")
def salir_del_super(lista_id):
    lista = logic_lista.salir_del_super(lista_id = lista_id )
    return redirect(url_for("listas.lista",lista_id = lista_id))




#Endpoints de productos
@listas.route("/producto/<int:producto_id>/borrar", methods = ["POST"])
@login_required
@user_roles_required("Usuario")
def borrar_producto(producto_id):
    producto = Producto(id = producto_id)
    try:
        producto_borrado = eggList.logic.logic_lista.borrar_producto(producto)
    except ProductoNoEncontradoException:
        flash("El producto ingresado no existe")
        abort(404)
    flash(f"Su producto '{producto_borrado.descripcion}' ha borrado satisfactoriamente", "primary")
    return redirect(url_for('listas.lista',lista_id = producto_borrado.id_lista))


@listas.route("/producto/<int:producto_id>/modificar",methods = ["GET","POST"])
@login_required
@user_roles_required("Usuario")
def modificar_producto(producto_id):

    form = ModificarProductoForm()
    if request.method == "GET":
        producto = eggList.logic.logic_lista.get_producto(producto_id)
        form.descripcion.data = producto.descripcion
        form.cantidad.data = producto.cantidad
        form.precio.data = producto.precio
        return render_template("productos/modificar_producto_form.html", form=form, lista_id=producto.id_lista)
    if form.validate_on_submit():
        producto = Producto(id = producto_id,
                            descripcion = form.descripcion.data,
                            cantidad = form.cantidad.data,
                            precio = form.precio.data)
        eggList.logic.logic_lista.modificar_producto(producto)
        flash("Tu producto se ha modificado con exito", "success")
        return redirect(url_for("listas.lista",lista_id = producto.id_lista))


@listas.route("/producto/<int:producto_id>/agregar_carrito",methods=["POST"])
@login_required
@user_roles_required("Usuario")
def confirmar_carrito(producto_id):
    form_carrito = CarritoForm()
    if form_carrito.validate_on_submit():
        producto = Producto(id = producto_id,
                            precio = form_carrito.precio.data,
                            cantidad = form_carrito.cantidad.data)
        try:
            producto_encontrado = eggList.logic.logic_lista.poner_en_carrito(producto)
        except ProductoNoEncontradoException:
            flash("El producto buscado no existe","danger")
            abort(404)
        except RolEnListaException:
            flash("No tenes permisos para realizar este cambio","warning")
            abort(403)

        flash(f"{producto_encontrado.descripcion} esta en carrito ","success")
        return redirect(url_for("listas.lista",lista_id = producto_encontrado.id_lista))


@listas.route("/producto/<int:producto_id>/sacar_de_carrito")
@login_required
@user_roles_required("Usuario")
def sacar_de_carrito(producto_id):
    producto = Producto(id=producto_id)
    try:
       producto_encontrado =  eggList.logic.logic_lista.sacar_de_carrito(producto)
    except ProductoNoEncontradoException:
        flash("El producto buscado no existe", "danger")
        abort(404)
    except RolEnListaException:
        flash("No tenes permisos para realizar este cambio", "warning")
        abort(403)

    flash(f"{producto_encontrado.descripcion} esta fuera carrito ", "info")
    return redirect(url_for("listas.lista", lista_id=producto_encontrado.id_lista))
