class ClasificacionSismo:
    def __init__(self, nombre, desde, hasta):
        self.nombre = nombre
        self.kmProfundidadDesde = desde
        self.kmProfundidadHasta = hasta

    def getNombre(self):
        return self.nombre
