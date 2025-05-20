class EstacionSismologica:
    def __init__(self, codigo, nombre):
        self.codigoEstacion = codigo
        self.nombre = nombre

    def getNombre(self):
        return self.nombre