from PyQt6.QtWidgets import QApplication
import sys
from gui import HackUnixApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HackUnixApp()
    window.show()
    sys.exit(app.exec())