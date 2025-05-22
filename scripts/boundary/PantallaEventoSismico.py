from scripts.control.GestorEventoSismico import GestorEventoSismico

from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QComboBox, QLineEdit, QMessageBox, QDialog, QHeaderView, QScrollArea, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class PantallaEventoSismico(QWidget):
    def __init__(self, pantallaInicio):
        super().__init__()
        self.pantallaInicio = pantallaInicio

    def opRegistrarResultadoRevisionManual(self, eventos, alcances, origenes, sesion, estados):
        self.habilitarVentana()
        self.gestor = GestorEventoSismico(self, eventos, alcances, origenes, sesion, estados)
        self.gestor.nuevoResultadoRevisionManual()

    def habilitarVentana(self):
        self.show()
        self.setWindowTitle("Revisión Manual - Selección")
        # centrar
        self.resize(1000, 700)
        pantalla = QApplication.primaryScreen().geometry()  # Tamaño de la pantalla
        ventana = self.geometry()  # Tamaño de la ventana
        x = (pantalla.width() - ventana.width()) // 2
        y = (pantalla.height() - ventana.height()) // 2
        self.move(x, y)  # Mueve la ventana al centro de la pantalla
        # crear tabla
        self.layout = QVBoxLayout()
        botonAtras = QPushButton("<< Atras")
        botonAtras.clicked.connect(lambda: (self.pantallaInicio.show(), self.close()))
        self.layout.addWidget(botonAtras)
        self.tablaEventosSismicos = QTableWidget()
        self.tablaEventosSismicos.setColumnCount(4)
        self.tablaEventosSismicos.setHorizontalHeaderLabels(["FechaHora", "Epicentro", "Hipocentro", "Magnitud"])
        self.tablaEventosSismicos.cellDoubleClicked.connect(self.tomarSeleccionEventoSismico)
        header = self.tablaEventosSismicos.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        self.layout.addWidget(self.tablaEventosSismicos)
        self.setLayout(self.layout)

    def solicitarSeleccionEventoSismico(self, eventos):
        self.eventosAutoDetectados = eventos
        self.tablaEventosSismicos.setRowCount(0)
        for r, evento in enumerate(eventos):
            self.tablaEventosSismicos.insertRow(r)
            datos = [
                evento.getFechaHoraOcurrencia().strftime("%d/%m/%Y %H:%M:%S"),
                f"({evento.getLatitudEpicentro():.5f}, {evento.getLongitudEpicentro():.5f})",
                f"({evento.getLatitudHipocentro():.5f}, {evento.getLongitudHipocentro():.5f})",
                f"{evento.getValorMagnitud():.1f}"
            ]
            for col, valor in enumerate(datos):
                item = QTableWidgetItem(valor)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Desactivar edición
                self.tablaEventosSismicos.setItem(r, col, item)

    def tomarSeleccionEventoSismico(self, row, col):
        self.gestor.tomarSeleccionEventoSismico(self.eventosAutoDetectados[row])
        #  borrar la tabla
        self.layout.removeWidget(self.tablaEventosSismicos)
        self.tablaEventosSismicos.setParent(None)
        self.tablaEventosSismicos.deleteLater()

    def mostrarDatosEventoSeleccionado(self, valorMagnitud, alcance, clasificacion, origen, sismogramas):
        # ajustar pantalla
        self.setWindowTitle("Revision Manual - Evento Sismico")
        self.resize(1000, 700)

        # Datos del evento
        datosLayout = QHBoxLayout()

        magnitudLayout = QHBoxLayout()
        magnitudLayout.setAlignment(Qt.AlignLeft)
        magnitudLayout.addWidget(QLabel("Magnitud:"))
        self.inputMagnitud = QLineEdit(f"{valorMagnitud:.2}")
        self.inputMagnitud.setEnabled(False)
        self.inputMagnitud.setStyleSheet("color: dimgray;")
        self.inputMagnitud.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        magnitudLayout.addWidget(self.inputMagnitud)

        alcanceLayout = QHBoxLayout()
        alcanceLayout.setAlignment(Qt.AlignCenter)
        alcanceLayout.addWidget(QLabel("Alcance:"))
        self.inputAlcance = QComboBox()
        self.inputAlcance.setEnabled(False)
        self.inputAlcance.setStyleSheet("color: dimgray;")
        self.inputAlcance.addItem(alcance)
        alcanceLayout.addWidget(self.inputAlcance)

        clasificacionLayout = QHBoxLayout()
        clasificacionLayout.setAlignment(Qt.AlignCenter)
        clasificacionLayout.addWidget(QLabel("Clasificacion:"))
        self.inputClasificacion = QComboBox()
        self.inputClasificacion.setEnabled(False)
        self.inputClasificacion.setStyleSheet("color: dimgray;")
        self.inputClasificacion.addItem(clasificacion)
        clasificacionLayout.addWidget(self.inputClasificacion)

        origenLayout = QHBoxLayout()
        origenLayout.setAlignment(Qt.AlignRight)
        origenLayout.addWidget(QLabel("Origen:"))
        self.inputOrigen = QComboBox()
        self.inputOrigen.setEnabled(False)
        self.inputOrigen.setStyleSheet("color: dimgray;")
        self.inputOrigen.addItem(origen)
        origenLayout.addWidget(self.inputOrigen)

        datosLayout.addLayout(magnitudLayout)
        datosLayout.addSpacing(66)
        datosLayout.addLayout(alcanceLayout)
        datosLayout.addSpacing(66)
        datosLayout.addLayout(clasificacionLayout)
        datosLayout.addSpacing(66)
        datosLayout.addLayout(origenLayout)
        self.layout.addLayout(datosLayout)

        # Layout de los sismogramas con scroll
        scroll = QScrollArea()  # el scroll
        container = QWidget()  # el padre del contenido, debe ser un Widget
        scrollLayout = QVBoxLayout(container)  # el layout del contenido, los layout no son Widgets

        # Tabla sismogramas
        self.tablaSismogramas = QTableWidget()
        self.tablaSismogramas.setColumnCount(2)
        self.tablaSismogramas.setHorizontalHeaderLabels(["Estación Sismológica", "Sismograma"])
        ancho = 334
        alto = 248
        for row, sismograma in enumerate(sismogramas):
            pixmap = QPixmap(sismograma[1]).scaled(ancho, alto, Qt.KeepAspectRatio)
            self.tablaSismogramas.insertRow(row)
            item = QTableWidgetItem(sismograma[0])
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.tablaSismogramas.setItem(row, 0, item)
            lbl = QLabel()
            lbl.setPixmap(pixmap)
            lbl.setAlignment(Qt.AlignCenter)
            self.tablaSismogramas.setCellWidget(row, 1, lbl)
            # Ajustá la altura de la fila
            self.tablaSismogramas.setRowHeight(row, alto + 10)  # margen extra opcional
        hdr = self.tablaSismogramas.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.Stretch)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        scrollLayout.addWidget(self.tablaSismogramas)

        scroll.setWidget(container)
        scroll.setObjectName("scroll")
        scroll.setWidgetResizable(True)
        self.layout.addWidget(scroll)

    def habilitarOpVisualizarMapaES(self):
        botonesLayout = QHBoxLayout()
        botonMapa = QPushButton("Mapa")
        botonMapa.clicked.connect(self.tomarOpcionVisualizarMapa)
        botonesLayout.addWidget(botonMapa)
        self.layout.addLayout(botonesLayout)

    def tomarOpcionVisualizarMapa(self):
        self.gestor.tomarOpcionVisualizarMapa()

    def visualizarMapa(self, mapa):
        ventanaMapa = QDialog(self)
        ventanaMapa.setWindowTitle("Mapa")
        ventanaMapa.resize(600, 400)
        mapaLayout = QVBoxLayout(ventanaMapa)
        pix = QPixmap(mapa).scaled(500, 350, Qt.KeepAspectRatio)
        lbl = QLabel()
        lbl.setPixmap(pix)
        mapaLayout.addWidget(lbl)
        ventanaMapa.exec_()

    def solicitarOpModificarDatosES(self, alcances, origenes):
        self.modificoDatos = False
        botonesLayout = self.layout.itemAt(self.layout.count() - 1)  # el ultimo que agregue fueron los botones
        botonModificar = QPushButton("Habilitar Modificacion")
        botonFinalizar = QPushButton("Finalizar Revision")
        botonModificar.clicked.connect(lambda: self.habilitarModificacionDatosES(alcances, origenes, botonModificar))
        botonFinalizar.clicked.connect(lambda: self.tomarModificacionDatosES() if self.modificoDatos
                                                                            else self.tomarRechazoOpModificarDatosES())
        botonesLayout.addWidget(botonModificar)
        botonesLayout.addWidget(botonFinalizar)

    def habilitarModificacionDatosES(self, alcances, origenes, botonModificar):
        botonModificar.setEnabled(False)
        self.modificoDatos = True
        self.inputMagnitud.setEnabled(True)
        self.inputMagnitud.setStyleSheet("")
        self.inputAlcance.setEnabled(True)
        self.inputAlcance.setStyleSheet("")
        for alcance in alcances:
            if not alcance in [self.inputAlcance.itemText(i) for i in range(self.inputAlcance.count())]:
                self.inputAlcance.addItem(alcance)
        self.inputOrigen.setEnabled(True)
        self.inputOrigen.setStyleSheet("")
        for origen in origenes:
            if not origen in [self.inputOrigen.itemText(i) for i in range(self.inputOrigen.count())]:
                self.inputOrigen.addItem(origen)

    def tomarRechazoOpModificarDatosES(self):
        self.gestor.tomarRechazoOpModificarDatosES()

    def tomarModificacionDatosES(self):
        magnitud = self.inputMagnitud.text()
        alcance = self.inputAlcance.currentText()
        origen = self.inputOrigen.currentText()
        self.gestor.tomarModificacionDatosES(magnitud ,alcance, origen)

    def solicitarSeleccionAccion(self):
        ventanaAccion = QDialog()
        ventanaAccion.setWindowTitle("Registrar Resultado")
        ventanaAccion.resize(400, 100)
        layoutAccion = QVBoxLayout()
        ventanaAccion.setLayout(layoutAccion)
        layoutAccion.addWidget(QLabel("Resultado de la revision:"))
        botonConfirmar = QPushButton("Confirmar")
        botonConfirmar.clicked.connect(lambda: self.tomarSeleccionConfirmar(ventanaAccion))
        layoutAccion.addWidget(botonConfirmar)
        botonRechazar = QPushButton("Rechazar")
        botonRechazar.clicked.connect(lambda: self.tomarSeleccionRechazar(ventanaAccion))
        layoutAccion.addWidget(botonRechazar)
        botonDerivar = QPushButton("Derivar")
        botonDerivar.clicked.connect(lambda: self.tomarSeleccionDerivar(ventanaAccion))
        layoutAccion.addWidget(botonDerivar)
        ventanaAccion.exec_()

    def tomarSeleccionConfirmar(self, ventana):
        ventana.close()
        self.gestor.tomarSeleccionConfirmar()

    def tomarSeleccionRechazar(self, ventana):
        ventana.close()
        self.gestor.tomarSeleccionRechazar()

    def tomarSeleccionDerivar(self, ventana):
        ventana.close()
        self.gestor.tomarSeleccionDerivar()

    def solicitarCorreccionDatosES(self, mensaje):
        ventanaError = QDialog()
        ventanaError.setWindowTitle("Erro de Validacion")
        ventanaError.resize(400, 100)
        layoutError = QVBoxLayout()
        ventanaError.setLayout(layoutError)
        layoutError.addWidget(QLabel(mensaje))
        layoutBoton = QHBoxLayout()
        layoutBoton.setAlignment(Qt.AlignCenter)
        botonError = QPushButton("Ok")
        botonError.setFixedWidth(100)
        botonError.clicked.connect(lambda: (ventanaError.close()))
        layoutBoton.addWidget(botonError)
        layoutError.addLayout(layoutBoton)
        ventanaError.exec_()

    def finCU(self):
        ventanaFin = QDialog()
        ventanaFin.setWindowTitle("Revision Registrada con Exito")
        ventanaFin.resize(400, 100)
        layoutFin = QVBoxLayout()
        ventanaFin.setLayout(layoutFin)
        layoutFin.addWidget(QLabel("La revision se registro con exito."))
        layoutBoton = QHBoxLayout()
        layoutBoton.setAlignment(Qt.AlignCenter)
        botonFin = QPushButton("Ok")
        botonFin.setFixedWidth(100)
        botonFin.clicked.connect(lambda: (self.pantallaInicio.show(), ventanaFin.close(), self.close()))
        layoutBoton.addWidget(botonFin)
        layoutFin.addLayout(layoutBoton)
        ventanaFin.exec_()
