class TipoDeDato:
    def __init__(self, denominacion, medida, umbral):
        self.denominacion = denominacion,
        self.nombreUnidadMedida = medida,
        self.valorUmbral = umbral

    def getDenominacion(self):
        return self.denominacion

    def esTuDenominacion(self, d):
        return self.denominacion == d
