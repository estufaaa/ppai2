from scripts.entidad.CambioEstado import CambioEstado

class EventoSismico:
    def __init__(self, fecha_ini, fecha_fin, e_latitud, e_longitud, h_latitud, h_longitud, valor_magnitud,
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
        self.cambioBloqueado = None  # esto esta para guardarlo durante el caso de uso

    def bloquear(self, estadoBloqueado, fechaHora, responsable=None):  # en el diagrama de secuencia no busca el responsable
        for cambio in self.cambiosEstado:
            if cambio.sosEstadoActual():
                cambio.setFechaHoraFin(fechaHora)
                break
        self.cambioBloqueado = CambioEstado(estadoBloqueado, fechaHora, responsable)
        self.estadoActual = estadoBloqueado
        self.cambiosEstado.append(self.cambioBloqueado)

    def rechazar(self, estado, fechaHora, responsable):  # esto se puede combinar con los otros, cambiando d. secuencia
        self.cambioBloqueado.setFechaHoraFin(fechaHora)
        cambio = CambioEstado(estado, fechaHora, responsable)
        self.estadoActual = estado
        self.cambiosEstado.append(cambio)

    def confirmar(self, estado, fechaHora, responsable):
        self.cambioBloqueado.setFechaHoraFin(fechaHora)
        cambio = CambioEstado(estado, fechaHora, responsable)
        self.estadoActual = estado
        self.cambiosEstado.append(cambio)

    def derivar(self, estado, fechaHora, responsable):
        self.cambioBloqueado.setFechaHoraFin(fechaHora)
        cambio = CambioEstado(estado, fechaHora, responsable)
        self.estadoActual = estado
        self.cambiosEstado.append(cambio)

    def getDatosSismicos(self):  # [estacion, [fecha, [valor]]]
        estaciones = []
        datosPorEstacion = []
        for serie in self.seriesTemporales:
            datos = serie.getDatos()  # [fecha, [valor]]
            estacion = serie.getNombreEstacionSismologica()
            if not estacion in estaciones:
                estaciones.append(estacion)
                datosPorEstacion.append((estacion, datos))
            else:
                datosPorEstacion[estaciones.index(estacion)][1].extend(datos)
        return datosPorEstacion

    def sosAutoDetectado(self):
        return self.estadoActual.sosAutoDetectado()

    def sosAutoConfirmado(self):
        return self.estadoActual.sosAutoConfirmado()

    def tenesAlcance(self):
        return not self.alcanceSismo is None

    def tenesMagnitud(self):
        return isinstance(self.valorMagnitud, (int, float)) and self.valorMagnitud > 0  # esto deberia usar la clase magnitud

    def tenesOrigen(self):
        return not self.origenGeneracion is None

    def getEstadoActual(self):
        return self.estadoActual.getNombre()

    def getAlcance(self):
        if self.alcanceSismo is None:
            return ""
        return self.alcanceSismo.getNombre()

    def setAlcance(self, alcance):
        self.alcanceSismo = alcance

    def getClasificacion(self):
        if self.clasificacion is None:
            return ""
        return self.clasificacion.getNombre()

    def getOrigen(self):
        if self.origenGeneracion is None:
            return ""
        return self.origenGeneracion.getNombre()

    def setOrigen(self, origen):
        self.origenGeneracion = origen

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

    def getValorMagnitud(self):
        return self.valorMagnitud

    def setValorMagnitud(self, magnitud):
        self.valorMagnitud = magnitud

    def getResponsable(self):
        for cambio in self.cambiosEstado:
            if cambio.sosEstadoActual():
                return cambio.getResponsable()
        return None
