from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from src.server.shop import ShopServer


class ProductDetailsWindow(QWidget):
    def __init__(self, product):
        super().__init__()
        self.setWindowTitle(product["title"])
        self.resize(400, 500)
        self.shop_server = ShopServer()
        layout = QVBoxLayout()

        # Imagem do produto (placeholder)
        image = QLabel()
        pixmap = QPixmap(
            "resources/default_product.jpg"
        )  # Substitua com o caminho da imagem real
        image.setPixmap(pixmap.scaled(300, 200, Qt.AspectRatioMode.KeepAspectRatio))
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Detalhes
        name_label = QLabel(f"<h2>{product['title']}</h2>")
        price_label = QLabel(f"<b>Preço:</b> {product['price']}")
        desc_label = QLabel(f"<b>Descrição:</b> {product['description']}")
        seller_label = QLabel(
            f"<b>Vendedor:</b> {product.get('shop',{}).get("name",'Loja Genérica')}"
        )

        # Botão comprar
        buy_button = QPushButton("Comprar")
        buy_button.clicked.connect(self.buy_product)

        # Adiciona ao layout
        layout.addWidget(image)
        layout.addWidget(name_label)
        layout.addWidget(price_label)
        layout.addWidget(desc_label)
        layout.addWidget(seller_label)
        layout.addWidget(buy_button)

        self.setLayout(layout)

    def buy_product(self):
        QMessageBox.information(self, "Compra", "Produto comprado com sucesso!")
        self.close()
