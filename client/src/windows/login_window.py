from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)

from windows.main_window import MainWindow
from windows.register_window import RegisterWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Rota da Seda")
        self.resize(300, 200)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuário")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Entrar")
        self.login_button.clicked.connect(self.login)

        self.register_button = QPushButton("Cadastrar-se")
        self.register_button.clicked.connect(self.register)

        layout.addWidget(QLabel("Bem-vindo ao Rota da Seda"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def login(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()
    def register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
