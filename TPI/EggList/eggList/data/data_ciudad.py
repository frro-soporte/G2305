from eggList.models.ciudad import Ciudad


def get_ciudad(cod_postal:int):
    return Ciudad.query.get(cod_postal)