from eggList.data import data_provincia
from eggList.models.provincia import Provincia
from eggList.models.ciudad import Ciudad

class ProvinciaNoEncontradaException:
    pass

def find_all():
    provincias = Provincia.query.order_by(Provincia.nombre.asc()).all()
    return provincias

def get_provincia(id:int):
    prov = data_provincia.get_provincia(id)
    if not prov:
        raise ProvinciaNoEncontradaException
    return prov


def get_ciudades(prov_id:int):
    ciudades = Ciudad.query.filter(Ciudad.id_provincia == prov_id).order_by(Ciudad.nombre.asc()).all()
    return ciudades