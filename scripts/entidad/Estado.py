class Estado:
    def __init__(self, nombre, ambito):
        self.nombreEstado = nombre
        self.ambito = ambito

    def sosAutoDetectado(self):
        return self.nombreEstado == "AutoDetectado"

    def sosBloqEnRevision(self):
        return self.nombreEstado == "BloqueadoEnRevision"

    def sosRechazado(self):
        return  self.nombreEstado == "Rechazado"

    def sosConfirmado(self):
        return  self.nombreEstado == "Confirmado"

    def sosDerivado(self):
        return  self.nombreEstado == "Derivado"

    def sosAmbitoEventoSismico(self):
        return self.ambito == "Evento Sismico"

    def getNombre(self):
        return self.nombreEstado
