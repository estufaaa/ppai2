class Sismografo:
    def __init__(self, id, adq, serie, estacion):
        self.identificadorSismografo = id
        self.fechaAdquisision = adq
        self.nroSerie = serie
        self.estacionSismologica = estacion

    def getNombreEstacion(self):
        return self.estacionSismologica.getNombre()
