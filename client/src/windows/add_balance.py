# windows/create_store_window.py
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)
from src.server.user import UserServer, BalanceModel


class AddBalanceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Adicionar Saldo")
        self.resize(300, 200)
        self.user_server = UserServer()
        layout = QVBoxLayout()

        self.balance_input = QLineEdit()
        self.balance_input.setPlaceholderText("Quantidade")

        self.create_button = QPushButton("Adicionar")
        self.create_button.clicked.connect(self.add_balance)

        layout.addWidget(QLabel("Adicionar Saldo"))
        layout.addWidget(self.balance_input)
        layout.addWidget(self.create_button)

        self.setLayout(layout)

    def add_balance(self):
        balance = self.balance_input.text()

        if balance:
            shop_created = self.user_server.add_balance(
                BalanceModel(amount=float(balance))
            )
            if "error" in shop_created.keys():
                QMessageBox.warning(self, "Erro", shop_created["error"])
                return
            QMessageBox.information(
                self,
                "Sucesso",
                "Saldo adicionado com sucesso!",
            )
            self.close()
        else:
            QMessageBox.warning(self, "Erro", "O valor do saldo não pode ser vazio.")
