class CambioEstado:
    def __init__(self, estado, inicio, responsable=None):
        self.estado = estado
        self.fechaHoraInicio = inicio
        self.fechaHoraFin = None
        self.responsable = responsable

    def sosEstadoActual(self):
        return self.fechaHoraFin is None

    def setFechaHoraFin(self, fin):
        self.fechaHoraFin = fin

    def getResponsable(self):
        return self.responsable
