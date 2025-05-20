class DetalleMuestraSismica:
    def __init__(self, valor, tipo):
        self.valor = valor
        self.tipoDeDato = tipo

    def getDatos(self):
        self.tipoDeDato.getDenominacion()