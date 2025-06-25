from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt
from src.server.user import UserServer, LoginModel
from windows.main_window import MainWindow
from windows.register_window import RegisterWindow
from Pyro5.errors import NamingError
import time
from src.singletons.token import GlobalToken


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Rota da Seda")
        self.resize(300, 200)
        try:
            self.user_server = UserServer()
        except NamingError:
            time.sleep(2)
            self.user_server = UserServer()
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
        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(QLabel("Bem-vindo ao Rota da Seda"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        layout.addWidget(self.message_label)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if not username or not password:
            self.username_input.setPlaceholderText("Preencha todos os campos")
            self.password_input.setPlaceholderText("Preencha todos os campos")
            return
        user = self.user_server.login(
            LoginModel(**{"email": username, "password": password})
        )
        if "error" in user.keys():
            self.message_label.setText(user["error"])
            self.message_label.setStyleSheet("color: red;")
            return
        if "access_token" in user.keys():
            GlobalToken.set_token(user["access_token"])
            self.main_window = MainWindow()
            self.main_window.show()
        else:
            self.message_label.setText("Login falhou. Verifique suas credenciais.")
            self.message_label.setStyleSheet("color: red;")
            return
        self.close()

    def register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()
