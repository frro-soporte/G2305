from eggList.data import data_supermercado
from eggList.models.supermercado import Supermercado


class SupermercadoNoEncontradoException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def find_all():
    supermercados = Supermercado.query.all()
    return supermercados

def get_supermercados_by_ciudad(cod_postal:int):
    supermercados = data_supermercado.get_supermercados(cod_postal)
    return supermercados