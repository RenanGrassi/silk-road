# windows/create_store_window.py
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)
from src.server.shop import ShopServer, ShopModel


class CreateStoreWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Criar Loja")
        self.resize(300, 200)
        self.shop_server = ShopServer()
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nome da Loja")

        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Descrição")

        self.create_button = QPushButton("Criar")
        self.create_button.clicked.connect(self.create_store)

        layout.addWidget(QLabel("Cadastro de Loja"))
        layout.addWidget(self.name_input)
        layout.addWidget(self.description_input)
        layout.addWidget(self.create_button)

        self.setLayout(layout)

    def create_store(self):
        name = self.name_input.text()
        desc = self.description_input.text()

        if name:
            shop_created = self.shop_server.create(ShopModel(name=name))
            if "error" in shop_created.keys():
                QMessageBox.warning(self, "Erro", shop_created["error"])
                return
            QMessageBox.information(
                self, "Sucesso", f"Loja '{name}' criada com sucesso!"
            )
            self.close()
        else:
            QMessageBox.warning(self, "Erro", "O nome da loja é obrigatório.")
