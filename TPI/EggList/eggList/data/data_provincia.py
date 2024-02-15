from eggList.models.provincia import Provincia


def get_provincia(id:int):
    prov = Provincia.query.get(id)
    return prov