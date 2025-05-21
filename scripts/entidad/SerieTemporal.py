class SerieTemporal:
    def __init__(self, fechaHora, inicio, frecuencia, muestras, sismografo):
        self.muestrasSismicas = muestras
        self.fechaHoraInicioRegistroMuestras = inicio
        self.fechaHoraRegistro = fechaHora
        self.frecuenciaMuestreo = frecuencia
        self.sismografo = sismografo
        self.condicionAlarma = False  # esto sale de validar todos los umbrales de los detalles

    def getDatos(self):  # [fecha, [valor]]
        datos = []
        for muestra in self.muestrasSismicas:
            datos.append(muestra.getDatos())
        return datos

    def getNombreEstacionSismologica(self):
        return self.sismografo.getNombreEstacion()
