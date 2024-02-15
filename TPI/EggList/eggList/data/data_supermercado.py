from eggList.models.supermercado import Supermercado


def get_supermercado(id_supermercado:int):
    return Supermercado.query.get(id_supermercado)

def get_supermercados(cod_postal:int=None):
    supermercados = []
    if cod_postal:
        supermercados = Supermercado.query.filter(Supermercado.cod_postal == cod_postal).all()
    return supermercados
