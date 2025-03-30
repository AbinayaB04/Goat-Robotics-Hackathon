from gui.fleet_gui import FleetGUI
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FleetGUI('data/nav_graph_3.json')
    window.show()
    sys.exit(app.exec_())
