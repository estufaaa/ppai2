import os
from datetime import datetime

class GestorEventoSismico:
    def __init__(self, pantalla, eventos, alcances, origenes, sesion, estados):  # no llamar
        # inicializar valores
        self.pantalla = pantalla
        self.sesionActual = sesion
        self.estados = estados
        self.eventosSismicos = eventos
        self.alcances = alcances
        self.origenes = origenes
        self.eventoSeleccionado = None  # se asigna al tomar evento

    def nuevoResultadoRevisionManual(self):
        autoDetectados = self.buscarEventosSismicosAutoDetectados()
        ordenados = self.ordenarPorFechaHoraOcurrencia(autoDetectados)
        self.pantalla.solicitarSeleccionEventoSismico(ordenados)

    def buscarEventosSismicosAutoDetectados(self):
        autoDetectados = []
        for evento in self.eventosSismicos:
            if evento.sosAutoDetectado():
                listaDatos = []
                listaDatos.append(evento)
                listaDatos.append(evento.getFechaHoraOcurrencia())
                listaDatos.append(evento.getLatitudEpicentro())
                listaDatos.append(evento.getLongitudEpicentro())
                listaDatos.append(evento.getLatitudHipocentro())
                listaDatos.append(evento.getLongitudHipocentro())
                listaDatos.append(evento.getValorMagnitud())
                autoDetectados.append(listaDatos)

        return autoDetectados

    def ordenarPorFechaHoraOcurrencia(self, eventos):
        eventos.sort(key=lambda e: e[1])
        return eventos

    def tomarSeleccionEventoSismico(self, evento):
        self.eventoSeleccionado = evento
        self.bloquearEventoSismico()
        magnitud = self.eventoSeleccionado.getValorMagnitud()
        alcance = self.obtenerAlcance()
        clasificacion = self.obtenerClasificacion()
        origen = self.obtenerOrigenDeGeneracion()
        datos = self.obtenerDatosSismicos()  # [estacion, [fecha, [valores]]]
        sismogramas = self.llamarCUGenerarSismograma(datos)  # estacion, ruta
        self.pantalla.mostrarDatosEventoSeleccionado(magnitud, alcance, clasificacion, origen, sismogramas)
        self.habilitarOpcionVisualizarMapaES()
        self.habilitarOpModificacionDatosES()

    def bloquearEventoSismico(self):
        fechaHora = self.obtenerFechaHoraActual()
        estadoBloqueado = self.buscarBloqEnRevision()
        self.eventoSeleccionado.bloquear(estadoBloqueado, fechaHora)

    def obtenerFechaHoraActual(self):
        return datetime.now()

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
        self.pantalla.habilitarOpVisualizarMapaES()

    def tomarOpcionVisualizarMapa(self):
        mapa = os.path.join(os.path.dirname(__file__), '../..', 'img', 'mapa.png')
        self.pantalla.visualizarMapa(mapa)

    def habilitarOpModificacionDatosES(self):
        self.pantalla.solicitarOpModificarDatosES([a.getNombre() for a in self.alcances],
                                                  [o.getNombre() for o in self.origenes])

    def tomarRechazoOpModificarDatosES(self):
        self.solicitarSeleccionAccion()

    def tomarModificacionDatosES(self, magnitud, alcance, origen):
        try:
            self.eventoSeleccionado.setValorMagnitud(float(magnitud))
        except ValueError:
            self.eventoSeleccionado.setValorMagnitud(None)
        self.eventoSeleccionado.setAlcance(None)  # si no lo encuentro queda None para que salte la validacion
        for a in self.alcances:
            if alcance == a.getNombre():
                self.eventoSeleccionado.setAlcance(a)
                break
        self.eventoSeleccionado.setOrigen(None)
        for o in self.origenes:
            if origen == o.getNombre():
                self.eventoSeleccionado.setOrigen(o)
                break
        self.solicitarSeleccionAccion()

    def solicitarSeleccionAccion(self):
        self.pantalla.solicitarSeleccionAccion()

    def tomarSeleccionConfirmar(self):
        validacion = self.validarExistenciaDatosES()
        if validacion != 0:
            self.solicitarCorreccionDatosES(validacion)
            return
        self.confirmarEventoSismico()
        self.finCU()

    def tomarSeleccionRechazar(self):
        validacion = self.validarExistenciaDatosES()
        if validacion != 0:
            self.solicitarCorreccionDatosES(validacion)
            return
        self.rechazarEventoSismico()
        self.finCU()

    def tomarSeleccionDerivar(self):
        validacion = self.validarExistenciaDatosES()
        if validacion != 0:
            self.solicitarCorreccionDatosES(validacion)
            return
        self.derivarEventoSismico()
        self.finCU()

    def validarExistenciaDatosES(self):  # cualquier cosa que no sea 0 es un codigo de error
        if not self.eventoSeleccionado.tenesMagnitud():
            return 1
        if not self.eventoSeleccionado.tenesAlcance():
            return 2
        if not self.eventoSeleccionado.tenesOrigen():
            return 3
        return 0

    def solicitarCorreccionDatosES(self, codigo):
        if codigo == 1:
            self.pantalla.solicitarCorreccionDatosES("La magnitud ingresada es invalida.")
        elif codigo == 2:
            self.pantalla.solicitarCorreccionDatosES("El alcance seleccionado es invalido.")
        elif codigo == 3:
            self.pantalla.solicitarCorreccionDatosES("El origen seleccionado es invalido.")
        else:
            self.pantalla.solicitarCorreccionDatosES("Los datos ingresados son invalidos.")

    def confirmarEventoSismico(self):
        fechaHora = self.obtenerFechaHoraActual()
        estado = self.buscarEstadoConfirmado()
        analista = self.obtenerASLogueado()
        self.eventoSeleccionado.confirmar(estado, fechaHora, analista)

    def rechazarEventoSismico(self):
        fechaHora = self.obtenerFechaHoraActual()
        estado = self.buscarEstadoRechazado()
        analista = self.obtenerASLogueado()
        self.eventoSeleccionado.rechazar(estado, fechaHora, analista)

    def derivarEventoSismico(self):
        fechaHora = self.obtenerFechaHoraActual()
        estado = self.buscarEstadoDerivado()
        analista = self.obtenerASLogueado()
        self.eventoSeleccionado.rechazar(estado, fechaHora, analista)

    def buscarEstadoConfirmado(self):
        for estado in self.estados:
            if estado.sosAmbitoEventoSismico() and estado.sosConfirmado():
                return estado

    def buscarEstadoRechazado(self):
        for estado in self.estados:
            if estado.sosAmbitoEventoSismico() and estado.sosRechazado():
                return estado

    def buscarEstadoDerivado(self):
        for estado in self.estados:
            if estado.sosAmbitoEventoSismico() and estado.sosDerivado():
                return estado

    def obtenerASLogueado(self):
        return self.sesionActual.obtenerEmpleado()

    def finCU(self):
        self.pantalla.finCU()
