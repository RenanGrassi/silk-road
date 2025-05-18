from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from src.gui.login_window import LoginWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Silk Road - Menu Principal")

        # Layout central
        central = QWidget()
        layout = QVBoxLayout()

        # Botões de ações
        btn_login = QPushButton("Login")
        btn_anunciar = QPushButton("Anunciar Produto")

        btn_login.clicked.connect(self.abrir_login)
        btn_anunciar.clicked.connect(self.abrir_anuncio)

        layout.addWidget(btn_login)
        layout.addWidget(btn_anunciar)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def abrir_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()

    # def abrir_anuncio(self):
    #     self.anuncio_window = AnuncioWindow()
    #     self.anuncio_window.show()
