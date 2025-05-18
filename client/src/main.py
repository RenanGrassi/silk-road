# src/main.py
from PySide6.QtWidgets import QApplication
from src.gui.main import ClientGUI
import sys
import os

os.environ["DISPLAY"] = ":1"
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = ClientGUI()
    gui.show()
    sys.exit(app.exec())
