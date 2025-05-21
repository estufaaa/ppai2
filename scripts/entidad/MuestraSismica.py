from DetalleMuestraSismica import DetalleMuestraSismica

class MuestraSismica:
    def __init__(self, fecha_hora, detalles):
        self.fechaHoraMuestra = fecha_hora
        self.detallesMuestraSismica = detalles

    def crearDetalleMuestra(self, valor, tipo):
        self.detallesMuestraSismica.append(DetalleMuestraSismica(valor, tipo))

    def getDatos(self):  # fecha, [valor]
        detalles = []
        for detalle in self.detallesMuestraSismica:
            detalles.append(detalle.getDatos()[0])  # deberia clasificar segun denominacion [1]
        return self.fechaHoraMuestra, detalles
