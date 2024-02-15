from eggList.models.rol_usuario import RolUsuario




def get_role(name:str):
    rol = RolUsuario.query.filter(RolUsuario.name == name).first()

    return rol