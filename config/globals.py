class RolesGlobal:
    usuario=2
    administrador=1
    @staticmethod
    def getNameRol(id:int):
        if id==RolesGlobal.usuario:
            return "Usuario"
        elif id==RolesGlobal.administrador:
            return "Administrador"
        else:
            return None
