import os
from datetime import datetime

class GestorEventoSismico:
    def __init__(self, pantalla, eventos, sesion, estados):  # no llamar
        # inicializar valores
        self.pantalla = pantalla
        self.sesionActual = sesion
        self.estados = estados
        self.eventosSismicos = eventos
        self.eventoSeleccionado = None  # se asigna al tomar evento

    def nuevoResultadoRevisionManual(self):
        autoDetectados = self.buscarEventosSismicosAutoDetectados()
        ordenados = self.ordenarPorFechaHoraOcurrencia(autoDetectados)
        self.pantalla.solicitarSeleccionEventoSismico(ordenados)

    def buscarEventosSismicosAutoDetectados(self):
        autoDetectados = []
        for evento in self.eventosSismicos:
            if evento.sosAutoDetectado():
                autoDetectados.append(evento)
        return autoDetectados

    def ordenarPorFechaHoraOcurrencia(self, eventos):
        eventos.sort(key=lambda e: e.fechaHoraOcurrencia)
        return eventos

    def tomarSeleccionEventoSismico(self, evento):
        self.eventoSeleccionado = evento
        self.bloquearEventoSismico()
        alcance = self.obtenerAlcance()
        clasificacion = self.obtenerClasificacion()
        origen = self.obtenerOrigenDeGeneracion()
        datos = self.obtenerDatosSismicos()  # [estacion, [fecha, [valores]]]
        sismogramas = self.llamarCUGenerarSismograma(datos)  # estacion, ruta
        self.pantalla.mostrarDatosEventoSeleccionado(alcance, clasificacion, origen, sismogramas)
        self.habilitarOpcionVisualizarMapaES()

    def bloquearEventoSismico(self):
        fechaHora = datetime.now()
        estadoBloqueado = self.buscarBloqEnRevision()
        self.eventoSeleccionado.bloquear(estadoBloqueado, fechaHora)

    def buscarBloqEnRevision(self):
        for estado in self.estados:
            if estado.sosAmbitoEventoSismico() and estado.sosBloqEnRevision():
                return estado
        return None

    def obtenerAlcance(self):
        return self.eventoSeleccionado.getAlcance()

    def obtenerClasificacion(self):
        return self.eventoSeleccionado.getClasificacion()

    def obtenerOrigenDeGeneracion(self):
        return self.eventoSeleccionado.getOrigen()

    def obtenerDatosSismicos(self):
        return self.eventoSeleccionado.getDatosSismicos()

    def llamarCUGenerarSismograma(self, datos):  # estacion, ruta
        ruta = os.path.join(os.path.dirname(__file__), '../..', 'img', 'sismograma.png')
        return [(datos[i][0], ruta) for i in range(len(datos))]

    def habilitarOpcionVisualizarMapaES(self):
        pass