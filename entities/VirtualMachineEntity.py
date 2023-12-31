class VirtualMachine:
    def __init__(self, id, nombre, sizeRam, fechaCreacion, dirMac, portVNC, zonaID, imagen):
        self.id = id
        self.nombre = nombre
        self.sizeRam = sizeRam
        self.fechaCreacion = fechaCreacion
        self.dirMac = dirMac
        self.portVNC = portVNC
        self.zonaID = zonaID
        self.imagen = imagen

    def __str__(self):
        return f"VirtualMachine(id={self.id}, nombre='{self.nombre}', sizeRam={self.sizeRam}, fechaCreacion='{self.fechaCreacion}', dirMac='{self.dirMac}', portVNC={self.portVNC}, zonaID={self.zonaID}, imagenID={self.imagen})"

class VirtualMachine_op:
    def __init__(self, id, nombre, sizeRam, flavor, fechaCreacion, dirMac, portVNC, zonaID, imagen):
            self.id = id
            self.nombre = nombre
            self.sizeRam = sizeRam
            self.flavor = flavor
            self.fechaCreacion = fechaCreacion
            self.dirMac = dirMac
            self.portVNC = portVNC
            self.zonaID = zonaID
           # self.internet = internet
            self.imagen = imagen

    def __str__(self):
        return f"VirtualMachine(id={self.id}, nombre='{self.nombre}', sizeRam={self.sizeRam}, flavor={self.flavor},fechaCreacion='{self.fechaCreacion}', dirMac='{self.dirMac}', portVNC={self.portVNC}, zonaID={self.zonaID}, imagenID={self.imagen})"

