from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")

        layout = QVBoxLayout()
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-mail")

        self.senha_input = QLineEdit()
        self.senha_input.setPlaceholderText("Senha")
        self.senha_input.setEchoMode(QLineEdit.EchoMode.Password)

        btn_login = QPushButton("Entrar")
        btn_login.clicked.connect(self.realizar_login)

        layout.addWidget(QLabel("Faça seu login"))
        layout.addWidget(self.email_input)
        layout.addWidget(self.senha_input)
        layout.addWidget(btn_login)

        self.setLayout(layout)

    def realizar_login(self):
        email = self.email_input.text()
        senha = self.senha_input.text()
        print("Tentando login com:", email, senha)
        # Vai vir uma chamada de socket do client para autenticação 