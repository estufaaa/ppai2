import random

from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QPushButton,
    QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView
)
from PyQt5.QtCore import Qt

import Generador
from boundary.PantallaEventoSismico import PantallaEventoSismico


class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Principal")
        self.resize(600, 300)
        pantalla = QApplication.primaryScreen().geometry()  # Tamaño de la pantalla
        ventana = self.geometry()  # Tamaño de la ventana
        x = (pantalla.width() - ventana.width()) // 2
        y = (pantalla.height() - ventana.height()) // 2
        self.move(x, y)  # Mueve la ventana al centro de la pantalla
        w = QWidget()
        v = QVBoxLayout()
        lbl = QLabel(f"Bienvenido {Generador.sesion.obtenerEmpleado().getNombre()}")
        lbl.setAlignment(Qt.AlignCenter)
        v.addWidget(lbl)
        btn1 = QPushButton("Ver Eventos Sísmicos")
        btn2 = QPushButton("Registrar Resultado de Revision Manual")
        btn1.clicked.connect(self.open_all_events)
        btn2.clicked.connect(self.open_revision)
        v.addWidget(btn1)
        v.addWidget(btn2)
        w.setLayout(v)
        self.setCentralWidget(w)

    def open_all_events(self):
        self.all_ev = AllEventsWindow(self)
        self.all_ev.show()
        self.close()

    def open_revision(self):
        self.pantallaRevision = PantallaEventoSismico(self)
        self.pantallaRevision.opRegistrarResultadoRevisionManual(Generador.eventos, Generador.alcances,
                                                                Generador.origenes, Generador.sesion, Generador.estados)
        self.close()

class AllEventsWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Todos los Eventos Sísmicos")
        self.resize(1200, 500)
        pantalla = QApplication.primaryScreen().geometry()  # Tamaño de la pantalla
        ventana = self.geometry()  # Tamaño de la ventana
        x = (pantalla.width() - ventana.width()) // 2
        y = (pantalla.height() - ventana.height()) // 2
        self.move(x, y)  # Mueve la ventana al centro de la pantalla
        v = QVBoxLayout()
        btn_back = QPushButton("« Volver al Menú")
        btn_back.clicked.connect(self.go_back)
        v.addWidget(btn_back)
        self.tablaEventosSismicos = QTableWidget()
        headers = [
            "Fecha Inicio","Fecha Fin","Epicentro","Hipocentro",
            "Magnitud","Clasificación","Origen","Alcance","Estado", "Revisado por"
        ]
        self.tablaEventosSismicos.setColumnCount(len(headers))
        self.tablaEventosSismicos.setHorizontalHeaderLabels(headers)
        self.load_data()
        header = self.tablaEventosSismicos.horizontalHeader()
        for i in range(len(headers)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        v.addWidget(self.tablaEventosSismicos)
        self.setLayout(v)

    def load_data(self):
        for r, e in enumerate(Generador.eventos):
            self.tablaEventosSismicos.insertRow(r)
            self.tablaEventosSismicos.setItem(r, 0, QTableWidgetItem(e.fechaHoraOcurrencia.strftime("%d/%m/%Y %H:%M:%S")))
            if e.fechaHoraFin is not None:
                self.tablaEventosSismicos.setItem(r, 1, QTableWidgetItem(e.fechaHoraFin.strftime("%d/%m/%Y %H:%M:%S")))
            else:
                self.tablaEventosSismicos.setItem(r, 1, QTableWidgetItem("-"))
            epic = f"({e.getLatitudEpicentro():.2f},{e.getLongitudEpicentro():.2f})"
            self.tablaEventosSismicos.setItem(r, 2, QTableWidgetItem(epic))
            hip = f"({e.getLatitudHipocentro():.2f},{e.getLongitudHipocentro():.2f})"
            self.tablaEventosSismicos.setItem(r, 3, QTableWidgetItem(hip))
            self.tablaEventosSismicos.setItem(r, 4, QTableWidgetItem(f"{e.getValorMagnitud():.1f}"))
            self.tablaEventosSismicos.setItem(r, 5, QTableWidgetItem(e.getClasificacion()))
            self.tablaEventosSismicos.setItem(r, 6, QTableWidgetItem(e.getOrigen()))
            self.tablaEventosSismicos.setItem(r, 7, QTableWidgetItem(e.getAlcance()))
            self.tablaEventosSismicos.setItem(r, 8, QTableWidgetItem(e.estadoActual.getNombre()))
            if e.getResponsable() is not None:
                self.tablaEventosSismicos.setItem(r, 9, QTableWidgetItem(e.getResponsable().getNombre()))
            else:
                self.tablaEventosSismicos.setItem(r, 9, QTableWidgetItem("-"))

    def go_back(self):
        self.parent.show()
        self.close()
