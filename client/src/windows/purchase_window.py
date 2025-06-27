from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
from PyQt6.QtCore import Qt

from src.server.transactions import TransactionServer
from src.server.models.products import ProductIdModel


class PurchaseWindow(QWidget):
    def __init__(self, product: dict):
        super().__init__()
        self.setWindowTitle("Confirmar Compra")
        self.resize(320, 200)

        self.product = product
        self.transaction_server = TransactionServer()

        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"<b>Produto:</b> {product['name']}"))
        layout.addWidget(QLabel(f"<b>Preço:</b> ฿{product['price']:.2f}"))
        layout.addWidget(
            QLabel(f"<b>Loja:</b> {product.get('seller', 'Desconhecida')}")
        )

        confirm_button = QPushButton("Confirmar Compra")
        confirm_button.clicked.connect(self.buy_product)
        layout.addWidget(confirm_button)

        self.setLayout(layout)

    def buy_product(self):
        try:
            config = ProductIdModel(product_id=self.product["id"])
            result = self.transaction_server.buy(config)

            if "error" not in result.keys():
                QMessageBox.information(
                    self, "Sucesso", "Compra realizada com sucesso!"
                )
                self.close()
            else:
                msg = result.get("error", "Erro ao realizar compra.")
                QMessageBox.warning(self, "Erro", msg)

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha na transação: {e}")
