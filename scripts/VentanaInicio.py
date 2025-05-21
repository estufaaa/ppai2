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
        lbl = QLabel(f"Bienvenido {Generador.sesion.obtenerUsuarioLogueado().getNombreApellido()}")
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
        self.pantallaRevision.opRegistrarResultadoRevisionManual()
        self.close()

class AllEventsWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Todos los Eventos Sísmicos")
        self.resize(1200, 500)
        v = QVBoxLayout()
        btn_back = QPushButton("« Volver al Menú")
        btn_back.clicked.connect(self.go_back)
        v.addWidget(btn_back)
        self.table = QTableWidget()
        headers = [
            "ID","Fecha Inicio","Fecha Fin","Epicentro","Hipocentro",
            "Magnitud","Clasificación","Origen","Alcance","Estado", "Revisado por", "Fecha de Revision"
        ]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.load_data()
        header = self.table.horizontalHeader()
        for i in range(len(headers)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        v.addWidget(self.table)
        self.setLayout(v)

    def load_data(self):
        return
        for e in sample_events:
            if e.estado in [ESTADO_CONFIRMADO, ESTADO_RECHAZADO, ESTADO_REV_EXPERTO]:
                if e.analista_revisor is None:
                    e.analista_revisor = random.choice(usuarios)
                if e.fecha_revision is None:
                    e.fecha_revision = e.fecha_fin
            else:
                e.analista_revisor = None
                e.fecha_revision = None

        for r, e in enumerate(sample_events):
            self.tablaEventosSismicos.insertRow(r)
            self.tablaEventosSismicos.setItem(r, 0, QTableWidgetItem(str(e.id)))
            self.tablaEventosSismicos.setItem(r, 1, QTableWidgetItem(e.fecha_ini.strftime("%d/%m/%Y %H:%M:%S")))
            self.tablaEventosSismicos.setItem(r, 2, QTableWidgetItem(e.fecha_fin.strftime("%d/%m/%Y %H:%M:%S")))
            epic = f"({e.latitud_epi:.2f},{e.longitud_epi:.2f})"
            self.tablaEventosSismicos.setItem(r, 3, QTableWidgetItem(epic))
            hip = f"({e.latitud_hipo:.2f},{e.longitud_hipo:.2f})"
            self.tablaEventosSismicos.setItem(r, 4, QTableWidgetItem(hip))
            self.tablaEventosSismicos.setItem(r, 5, QTableWidgetItem(f"{e.valor_magnitud:.1f}"))
            self.tablaEventosSismicos.setItem(r, 6, QTableWidgetItem(e.clasificacion.nombre))
            self.tablaEventosSismicos.setItem(r, 7, QTableWidgetItem(e.origen.nombre))
            self.tablaEventosSismicos.setItem(r, 8, QTableWidgetItem(e.alcance.nombre))
            self.tablaEventosSismicos.setItem(r, 9, QTableWidgetItem(e.estado.nombre))
            if e.estado in [ESTADO_CONFIRMADO, ESTADO_RECHAZADO, ESTADO_REV_EXPERTO]:
                self.tablaEventosSismicos.setItem(r, 10, QTableWidgetItem(e.analista_revisor.nombre))
                self.tablaEventosSismicos.setItem(r, 11, QTableWidgetItem(
                    e.fecha_revision.strftime("%d/%m/%Y %H:%M:%S") if e.fecha_revision else "-"
                ))
            else:
                self.tablaEventosSismicos.setItem(r, 10, QTableWidgetItem("-"))
                self.tablaEventosSismicos.setItem(r, 11, QTableWidgetItem("-"))

    def go_back(self):
        self.parent.show()
        self.close()
