from scripts import Generador

class GestorEventoSismico:
    def __init__(self, pantalla, eventos, sesion, estados):  # no llamar
        # inicializar valores
        self.pantalla = pantalla
        self.sesionActual = sesion
        self.estados = estados
        self.eventoSeleccionado = None  # se asigna al tomar evento
        # llamadas a metodos
        autoDetectados = self.buscarEventosSismicosAutoDetectados(eventos)
        ordenados = self.ordenarPorFechaHoraOcurrencia(autoDetectados)
        self.pantalla.solicitarSeleccionEventoSismico(ordenados)

    @staticmethod
    def nuevoResultadoRevisionManual(pantalla):  # constructor
        return GestorEventoSismico(pantalla, Generador.eventos, Generador.sesion, Generador.estados)

    def buscarEventosSismicosAutoDetectados(self, eventos):
        autoDetectados = []
        for evento in eventos:
            if evento.sosAutoDetectado():
                autoDetectados.append(evento)
        return autoDetectados

    def ordenarPorFechaHoraOcurrencia(self, eventos):
        eventos.sort(key=lambda e: e.fechaHoraOcurrencia)
        return eventos

    def tomarSeleccionEventoSismico(self, evento):
        self.eventoSeleccionado = evento
