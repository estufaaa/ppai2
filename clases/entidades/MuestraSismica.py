from DetalleMuestraSismica import DetalleMuestraSismica

class MuestraSismica:
    def __init__(self, fecha_hora, detalles):
        self.fechaHoraMuestra = fecha_hora
        self.detallesMuestraSismica = detalles

    def crearDetalleMuestra(self, valor, tipo):
        self.detallesMuestraSismica.append(DetalleMuestraSismica(valor, tipo))

    def getDatos(self):
        for detalle in self.detallesMuestraSismica:
            detalle.getDatos()
