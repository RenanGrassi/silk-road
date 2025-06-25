# windows/create_store_window.py
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class CreateStoreWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Criar Loja")
        self.resize(300, 200)

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
            # Aqui no futuro vai a chamada Pyro
            QMessageBox.information(self, "Sucesso", f"Loja '{name}' criada com sucesso!")
            self.close()
        else:
            QMessageBox.warning(self, "Erro", "O nome da loja é obrigatório.")
