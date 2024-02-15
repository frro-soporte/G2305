from flask import Blueprint, jsonify

from eggList.logic import logic_provincia
from eggList.logic.logic_provincia import ProvinciaNoEncontradaException
from eggList.models.provincia import Provincia

provincias = Blueprint('provincias',__name__)

@provincias.route("/provincia/<int:id_provincia>/ciudades")
def ciudades(id_provincia):
    try:
        provincia = logic_provincia.get_provincia(id_provincia)
    except ProvinciaNoEncontradaException:
        return jsonify({"message":"La provincia ingresada no se encuentra"}),404
    ciudades=[]
    for ciudad in provincia.ciudades:
        ciudad_dicc = {"cod_postal":ciudad.cod_postal, "nombre":ciudad.nombre}
        ciudades.append(ciudad_dicc)
    return jsonify(ciudades)
