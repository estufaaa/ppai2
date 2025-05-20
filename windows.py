# windows.py
import os
import random

from PyQt5.QtWidgets import (
    QWidget, QMainWindow, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QComboBox, QLineEdit, QMessageBox, QDialog, QHeaderView, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from domain import (
    sample_events, analista, alcances, origenes,
    ESTADO_AUTODETECTADO, ESTADO_CONFIRMADO,
    ESTADO_RECHAZADO, ESTADO_REV_EXPERTO, obtener_clasificacion, Empleado
)
from domain import ESTADO_BLOQUEADO, rol_analista

usuarios = [Empleado("Gonzalez", "gonzalez@gmail.com", "Gustavo", "987", rol_analista),
            Empleado("Arevalo", "arevalo@gmail.com", "Celeste", "654", rol_analista),
            Empleado("Masud", "masud@gmail.com", "Juan", "321", rol_analista)]

class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Principal")
        self.resize(600, 300)
        w = QWidget()
        v = QVBoxLayout()
        lbl = QLabel(f"Bienvenido {analista.nombre}")
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
        self.rev = MainWindowRevision(self)
        self.rev.show()
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
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(str(e.id)))
            self.table.setItem(r, 1, QTableWidgetItem(e.fecha_ini.strftime("%d/%m/%Y %H:%M:%S")))
            self.table.setItem(r, 2, QTableWidgetItem(e.fecha_fin.strftime("%d/%m/%Y %H:%M:%S")))
            epic = f"({e.latitud_epi:.2f},{e.longitud_epi:.2f})"
            self.table.setItem(r, 3, QTableWidgetItem(epic))
            hip = f"({e.latitud_hipo:.2f},{e.longitud_hipo:.2f})"
            self.table.setItem(r, 4, QTableWidgetItem(hip))
            self.table.setItem(r, 5, QTableWidgetItem(f"{e.valor_magnitud:.1f}"))
            self.table.setItem(r, 6, QTableWidgetItem(e.clasificacion.nombre))
            self.table.setItem(r, 7, QTableWidgetItem(e.origen.nombre))
            self.table.setItem(r, 8, QTableWidgetItem(e.alcance.nombre))
            self.table.setItem(r, 9, QTableWidgetItem(e.estado.nombre))
            if e.estado in [ESTADO_CONFIRMADO, ESTADO_RECHAZADO, ESTADO_REV_EXPERTO]:
                self.table.setItem(r, 10, QTableWidgetItem(e.analista_revisor.nombre))
                self.table.setItem(r, 11, QTableWidgetItem(
                    e.fecha_revision.strftime("%d/%m/%Y %H:%M:%S") if e.fecha_revision else "-"
                ))
            else:
                self.table.setItem(r, 10, QTableWidgetItem("-"))
                self.table.setItem(r, 11, QTableWidgetItem("-"))

    def go_back(self):
        self.parent.show()
        self.close()


class MainWindowRevision(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Revisión Manual - Selección")
        self.resize(800, 500)
        v = QVBoxLayout()
        btn_back = QPushButton("« Volver al Menú")
        btn_back.clicked.connect(self.go_back)
        v.addWidget(btn_back)
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["FechaHora","Epicentro","Hipocentro","Magnitud"])
        # self.load_data() # NUEVO
        self.table.cellDoubleClicked.connect(self.select_event)
        header = self.table.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        v.addWidget(self.table)
        self.setLayout(v)

    def load_data(self):
        evs = [e for e in sample_events if e.estado == ESTADO_AUTODETECTADO]
        evs.sort(key=lambda e: e.fecha_ini)
        """ # NUEVO
        self.table.setRowCount(0)
        for r, e in enumerate(evs):
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(e.fecha_ini.strftime("%d/%m/%Y %H:%M:%S")))
            coord = f"({e.latitud:.2f}, {e.longitud:.2f})"
            self.table.setItem(r, 1, QTableWidgetItem(coord))
            self.table.setItem(r, 2, QTableWidgetItem(f"{e.profundidad}"))
            self.table.setItem(r, 3, QTableWidgetItem(f"{e.valor_magnitud:.1f}"))
        """
        self.table.setRowCount(0)
        for r, e in enumerate(evs):
            self.table.insertRow(r)
            # Crear y configurar los items en una sola línea
            for col, valor in enumerate([
                e.fecha_ini.strftime("%d/%m/%Y %H:%M:%S"),
                f"({e.latitud_epi:.2f}, {e.longitud_epi:.2f})",
                f"({e.latitud_hipo:.2f}, {e.longitud_hipo:.2f})",
                f"{e.valor_magnitud:.1f}"
            ]):
                item = QTableWidgetItem(valor)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Desactivar edición
                self.table.setItem(r, col, item)

    def show(self): # NUEVO
        super().show()
        self.load_data()

    def select_event(self, row, col):
        evs = [e for e in sample_events if e.estado == ESTADO_AUTODETECTADO]
        evs.sort(key=lambda e: e.fecha_ini)
        ev = evs[row]
        ev.cambiar_estado(ESTADO_BLOQUEADO) # NUEVO
        # print(evs[row])
        self.detail = DetailWindowRevision(self, ev)
        self.detail.show()
        self.close()

    def go_back(self):
        self.parent.show()
        self.close()


class DetailWindowRevision(QWidget):
    def __init__(self, parent, evento):
        super().__init__()
        self.parent = parent
        self.evento = evento
        self.setWindowTitle(f"Detalle Evento {evento.id}")
        self.resize(1000, 700)
        self.accion_confirmada = False

        # Layout principal con scroll
        scroll = QScrollArea()
        container = QWidget()
        v = QVBoxLayout(container)

        # Botón volver
        btn_back = QPushButton("« Volver a Selección")
        btn_back.clicked.connect(self.go_back)
        v.addWidget(btn_back)

        # Edición básica
        hl = QHBoxLayout()
        self.magn_edit = QLineEdit(f"{evento.valor_magnitud:.1f}")
        self.alc_cb = QComboBox()
        for a in alcances: self.alc_cb.addItem(a.nombre)
        self.or_cb = QComboBox()
        for o in origenes: self.or_cb.addItem(o.nombre)
        hl.addWidget(QLabel("Magnitud:")); hl.addWidget(self.magn_edit)
        hl.addWidget(QLabel("Alcance:"));   hl.addWidget(self.alc_cb)
        hl.addWidget(QLabel("Origen:"));    hl.addWidget(self.or_cb)
        v.addLayout(hl)

        # Tabla muestras
        """ # NUEVO
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Estación","FechaHora","Tipo de Dato","Valor"])
        self.load_samples()
        hdr = self.table.horizontalHeader()
        for i in range(4):
            hdr.setSectionResizeMode(i, QHeaderView.Stretch)
        v.addWidget(self.table)
        """

        # Tabla sismogramas (group by estación)
        self.table2 = QTableWidget()
        self.table2.setColumnCount(2)
        self.table2.setHorizontalHeaderLabels(["Estación Sismológica", "Sismograma"])
        self.load_sismogramas()
        hdr2 = self.table2.horizontalHeader()
        hdr2.setSectionResizeMode(0, QHeaderView.Stretch)
        hdr2.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        v.addWidget(self.table2)

        # Botones Modificar + Confirmar acción + Mapa
        h2 = QHBoxLayout()
        btn_mod = QPushButton("Modificar")
        btn_mod.clicked.connect(self.apply_modifications)
        self.action_cb = QComboBox()
        self.action_cb.addItems(["Confirmar evento","Rechazar evento","Solicitar revisión a experto"])
        self.confirm_btn = QPushButton("Confirmar Acción")
        self.confirm_btn.clicked.connect(self.confirm_action)
        btn_map = QPushButton("Mapa")
        btn_map.clicked.connect(self.show_map)
        h2.addWidget(btn_mod)
        h2.addWidget(self.action_cb)
        h2.addWidget(self.confirm_btn)
        h2.addWidget(btn_map)
        v.addLayout(h2)

        scroll.setWidget(container)
        scroll.setWidgetResizable(True)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        self.setLayout(layout)

    def load_samples(self):
        rows = []
        for st in sorted(self.evento.series_temporales, key=lambda s: s.estacion.codigo):
            for m in st.muestras:
                rows.append((st.estacion.codigo, m))
        self.table.setRowCount(0)
        for r, (cod, m) in enumerate(rows):
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(str(cod)))
            self.table.setItem(r, 1, QTableWidgetItem(m.fecha_hora.strftime("%d/%m/%Y %H:%M:%S")))
            self.table.setItem(r, 2, QTableWidgetItem(m.tipo_de_dato.nombre))
            self.table.setItem(r, 3, QTableWidgetItem(str(m.valor)))

    def load_sismogramas(self):
        # Agrupo por estación
        estaciones = sorted({st.estacion.codigo for st in self.evento.series_temporales})
        self.table2.setRowCount(0)
        img_path = os.path.join(os.path.dirname(__file__), '..', 'img', 'sismograma.png')

        # Ajustá el tamaño de la imagen
        imagen_ancho = 334
        imagen_alto = 248
        pixmap = QPixmap(img_path).scaled(imagen_ancho, imagen_alto, Qt.KeepAspectRatio)

        for r, cod in enumerate(estaciones):
            self.table2.insertRow(r)
            item = QTableWidgetItem(str(cod)) # NUEVO
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.table2.setItem(r, 0, item)
            lbl = QLabel()
            lbl.setPixmap(pixmap)
            lbl.setAlignment(Qt.AlignCenter)
            self.table2.setCellWidget(r, 1, lbl)

            # 🔥 Ajustá la altura de la fila
            self.table2.setRowHeight(r, imagen_alto + 10)  # margen extra opcional

    def apply_modifications(self):
        texto = self.magn_edit.text().strip()

        if not texto:
            QMessageBox.warning(self, "Error", "La magnitud no puede estar vacía.")
            return False

        try:
            valor = float(texto)
            if valor <= 0:
                QMessageBox.warning(self, "Error", "La magnitud debe ser un número positivo.")
                return False
        except ValueError:
            QMessageBox.warning(self, "Error", "La magnitud debe ser un número válido.")
            return False

        # Verificamos si la clasificación debería cambiar
        nueva_clasificacion = obtener_clasificacion(valor)
        if self.evento.clasificacion.nombre != nueva_clasificacion.nombre:
            self.evento.clasificacion = nueva_clasificacion

        # Aplicamos el resto de los cambios
        self.evento.valor_magnitud = valor
        self.evento.alcance = alcances[self.alc_cb.currentIndex()]
        self.evento.origen = origenes[self.or_cb.currentIndex()]

        QMessageBox.information(self, "Éxito", "Atributos modificados correctamente.")
        return True # NUEVO

    def confirm_action(self):
        if not self.apply_modifications(): # NUEVO
            return
        sel = self.action_cb.currentText()
        if sel == "Confirmar evento":
            nuevo = ESTADO_CONFIRMADO
        elif sel == "Rechazar evento":
            nuevo = ESTADO_RECHAZADO
        else:
            nuevo = ESTADO_REV_EXPERTO
        self.evento.cambiar_estado(nuevo, analista)
        self.accion_confirmada = True
        QMessageBox.information(self, "Éxito", f"Evento marcado como «{nuevo.nombre}».")

        # Ir al menú principal después de confirmar
        self.menu = MenuWindow()
        self.menu.show()
        self.close()


    def show_map(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Mapa")
        dlg.resize(600, 400)
        v = QVBoxLayout(dlg)
        img_path = os.path.join(os.path.dirname(__file__), '..', 'img', 'mapa.png')
        pix = QPixmap(img_path).scaled(500, 350, Qt.KeepAspectRatio)
        lbl = QLabel()
        lbl.setPixmap(pix)
        v.addWidget(lbl)
        dlg.exec_()

    def go_back(self):
        # if not self.accion_confirmada: # NUEVO
            # self.evento.cambiar_estado(ESTADO_AUTODETECTADO) # NUEVO
        self.parent.show()
        self.close()

