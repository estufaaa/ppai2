from scripts.control.GestorEventoSismico import GestorEventoSismico

from PyQt5.QtWidgets import (
    QWidget, QMainWindow, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QComboBox, QLineEdit, QMessageBox, QDialog, QHeaderView, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from scripts.windows import MainWindowRevision


class PantallaEventoSismico(QWidget):
    def __init__(self, pantallaInicio):  # no llamar directamente
        super().__init__()
        # inicializar variables
        self.grillaEventoSismico = None  # se asigna en habilitarVentana()
        self.pantallaInicio = pantallaInicio
        # llamar metodos
        self.habilitarVentana()
        self.gestor = GestorEventoSismico.nuevoResultadoRevisionManual(self)

    @staticmethod
    def opRegistrarResultadoRevisionManual(inicio):  # este metodo debe usarse como constructor
        return PantallaEventoSismico(inicio)

    def habilitarVentana(self):
        self.show()
        self.setWindowTitle("Revisión Manual - Selección")
        self.resize(800, 500)
        layout = QVBoxLayout()
        self.grillaEventoSismico = QTableWidget()
        self.grillaEventoSismico.setColumnCount(4)
        self.grillaEventoSismico.setHorizontalHeaderLabels(["FechaHora", "Epicentro", "Hipocentro", "Magnitud"])
        self.grillaEventoSismico.cellDoubleClicked.connect(self.tomarSeleccionEventoSismico)
        header = self.grillaEventoSismico.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        layout.addWidget(self.grillaEventoSismico)
        self.setLayout(layout)

    def solicitarSeleccionEventoSismico(self, eventos):
        self.eventosAutoDetectados = eventos
        self.grillaEventoSismico.setRowCount(0)
        for r, evento in enumerate(eventos):
            self.grillaEventoSismico.insertRow(r)
            datos = [
                evento.getFechaHoraOcurrencia().strftime("%d/%m/%Y %H:%M:%S"),
                f"({evento.getLatitudEpicentro():.5f}, {evento.getLongitudEpicentro():.5f})",
                f"({evento.getLatitudHipocentro():.5f}, {evento.getLongitudHipocentro():.5f})",
                f"{evento.getValorMagnitud():.1f}"
            ]
            for col, valor in enumerate(datos):
                item = QTableWidgetItem(valor)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Desactivar edición
                self.grillaEventoSismico.setItem(r, col, item)

    def tomarSeleccionEventoSismico(self, row, col):
        self.gestor.tomarSeleccionEventoSismico(self.eventosAutoDetectados[row])
