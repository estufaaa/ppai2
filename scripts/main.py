import sys
from PyQt5.QtWidgets import QApplication
from VentanaInicio import MenuWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MenuWindow()
    win.show()
    sys.exit(app.exec_())
