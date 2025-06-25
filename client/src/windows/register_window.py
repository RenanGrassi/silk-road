from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from src.server.user import UserServer


class RegisterWindow(QWidget):
    def __init__(self):
        self.user_server = UserServer()
        super().__init__()
        self.setWindowTitle("Cadastro de Usuário")
        self.resize(400, 450)

        layout = QVBoxLayout()

        logo_label = QLabel()
        logo_pixmap = QPixmap("resources/logo.png")
        logo_label.setPixmap(
            logo_pixmap.scaled(
                220,
                80,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        # 🧾 Campos do formulário
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nome de usuário")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirmar senha")
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Feedback
        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Botão de cadastro
        register_button = QPushButton("Cadastrar")
        register_button.clicked.connect(self.register_user)

        layout.addWidget(QLabel("<h3>Crie sua conta</h3>"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_input)
        layout.addWidget(register_button)
        layout.addWidget(self.message_label)

        self.setLayout(layout)

    def register_user(self):
        from windows.login_window import LoginWindow

        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()

        if not username or not email or not password or not confirm:
            self.message_label.setText("Todos os campos são obrigatórios.")
            self.message_label.setStyleSheet("color: red;")
            return

        if "@" not in email or "." not in email:
            self.message_label.setText("Email inválido.")
            self.message_label.setStyleSheet("color: red;")
            return

        if password != confirm:
            self.message_label.setText("As senhas não coincidem.")
            self.message_label.setStyleSheet("color: red;")
            return

        register_data = self.user_server.register(
            {"name": username, "email": email, "password": password}
        )
        if "error" in register_data.keys():
            self.message_label.setText(register_data["error"])
            self.message_label.setStyleSheet("color: red;")
            return
        self.message_label.setText(f"Usuário '{username}' cadastrado com sucesso!")
        self.message_label.setStyleSheet("color: green;")
        self.username_input.clear()
        self.email_input.clear()
        self.password_input.clear()
        self.confirm_input.clear()
        # TODO - Redirecionar para a tela de login
        self.message_label.setText(f"Usuário '{username}' cadastrado com sucesso!")
        self.message_label.setStyleSheet("color: green;")

        # Redireciona para tela de login
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
