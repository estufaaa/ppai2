from CambioEstado import CambioEstado

class EventoSismico:
    def __init__(self, fecha_ini, fecha_fin, e_longitud, e_latitud, h_longitud, h_latitud, valor_magnitud,
                 alcance, clasificacion, origen, series_temporales, estado):
        self.fechaHoraOcurrencia = fecha_ini
        self.fechaHoraFin = fecha_fin
        # atributos
        self.latitudEpicentro = e_latitud
        self.longitudEpicentro = e_longitud
        self.latitudHipocentro = h_latitud
        self.longitudHipocentro = h_longitud
        self.valorMagnitud = valor_magnitud
        # datos (atributos puntero)
        self.alcanceSismo = alcance
        self.clasificacion = clasificacion
        self.origenGeneracion = origen
        self.seriesTemporales = series_temporales
        # estado
        self.estadoActual = estado
        self.cambiosEstado = [CambioEstado(estado, fecha_ini)]

    def bloquear(self, estadoBloqueado, fechaHora, responsable):
        for cambio in self.cambiosEstado:
            if cambio.sosEstadoActual():
                cambio.setFechaHoraFin(fechaHora)
                break
        cambioBloqueado = CambioEstado(estadoBloqueado, fechaHora, responsable)
        self.estadoActual = estadoBloqueado
        self.cambiosEstado.append(cambioBloqueado)

    def getAlcance(self):
        return self.alcanceSismo.getNombre()

    def getClasificacion(self):
        return self.clasificacion.getNombre()

    def getOrigen(self):
        return self.origenGeneracion.getNombre()

    def getFechaHoraOcurrencia(self):
        return self.fechaHoraOcurrencia

    def getLatitudEpicentro(self):
        return self.latitudEpicentro

    def getLatitudHipocentro(self):
        return self.latitudHipocentro

    def getLongitudEpicentro(self):
        return self.longitudEpicentro

    def getLongitudHipocentro(self):
        return self.longitudHipocentro
