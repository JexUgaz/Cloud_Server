class Subred:
    def __init__(self, id, dir_red, activo):
        self.id = id
        self.dir_red = dir_red
        self.activo = activo

    def __str__(self):
        return f"Subred(id={self.id}, dir_red='{self.dir_red}', activo={self.activo})"
