from scripts.control.GestorEventoSismico import GestorEventoSismico

from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QComboBox, QLineEdit, QMessageBox, QDialog, QHeaderView, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from scripts import Generador

class PantallaEventoSismico(QWidget):
    def __init__(self, pantallaInicio):
        super().__init__()
        self.pantallaInicio = pantallaInicio

    def opRegistrarResultadoRevisionManual(self):
        self.habilitarVentana()
        self.gestor = GestorEventoSismico(self, Generador.eventos, Generador.sesion, Generador.estados)
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

    def mostrarDatosEventoSeleccionado(self, alcance, clasificacion, origen, sismogramas):
        # ajustar pantalla
        self.setWindowTitle("Revision Manual - Evento Sismico")
        self.resize(1000, 700)

        # Layout principal con scroll
        scroll = QScrollArea()  # el scroll
        container = QWidget()  # el padre del contenido, debe ser un Widget
        scrollLayout = QVBoxLayout(container)  # el layout del contenido, los layout no son Widgets

        # Datos del evento
        datosLayout = QHBoxLayout()

        alcanceLayout = QHBoxLayout()
        alcanceLayout.addWidget(QLabel("Alcance:"))
        self.inputAlcance = QComboBox()
        self.inputAlcance.addItem(alcance)
        alcanceLayout.addWidget(self.inputAlcance)

        clasificacionLayout = QHBoxLayout()
        clasificacionLayout.addWidget(QLabel("Clasificacion:"))
        self.inputClasificacion = QComboBox()
        self.inputClasificacion.addItem(clasificacion)
        clasificacionLayout.addWidget(self.inputClasificacion)

        origenLayout = QHBoxLayout()
        origenLayout.addWidget(QLabel("Origen:"))
        self.inputOrigen = QComboBox()
        self.inputOrigen.addItem(origen)
        origenLayout.addWidget(self.inputOrigen)

        datosLayout.addLayout(alcanceLayout)
        datosLayout.addSpacing(150)
        datosLayout.addLayout(clasificacionLayout)
        datosLayout.addSpacing(150)
        datosLayout.addLayout(origenLayout)
        scrollLayout.addLayout(datosLayout)

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
        """
        # Botones Modificar + Confirmar acción + Mapa
        botonesLayout = QHBoxLayout()
        modificar = QPushButton("Modificar")
        modificar.clicked.connect()  # hacer cosas
        self.inputAccion = QComboBox()
        self.inputAccion.addItems(["Confirmar evento", "Rechazar evento", "Solicitar revisión a experto"])
        self.confirmar = QPushButton("Confirmar Acción")
        self.confirmar.clicked.connect(self.confirm_action)
        btn_map = QPushButton("Mapa")
        btn_map.clicked.connect(self.show_map)
        botonesLayout.addWidget(modificar)
        botonesLayout.addWidget(self.inputAccion)
        botonesLayout.addWidget(self.confirmar)
        botonesLayout.addWidget(btn_map)
        v.addLayout(botonesLayout)
        """

        scroll.setWidget(container)
        scroll.setWidgetResizable(True)
        self.layout.addWidget(scroll)
