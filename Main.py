import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from view.MainView import MainView


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    main = MainView()
    main.show()
    sys.exit(app.exec_())
