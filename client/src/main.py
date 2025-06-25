import sys
from PyQt6.QtWidgets import QApplication
from src.windows.login_window import LoginWindow

app = QApplication(sys.argv)


def show_login():
    global login_window
    login_window = LoginWindow()
    login_window.show()


show_login()

sys.exit(app.exec())
