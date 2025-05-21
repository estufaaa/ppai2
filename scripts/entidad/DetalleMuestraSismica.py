class DetalleMuestraSismica:
    def __init__(self, valor, tipo):
        self.valor = valor
        self.tipoDeDato = tipo

    def getDatos(self):  # valor, denominacion
        return self.valor, self.tipoDeDato.getDenominacion()