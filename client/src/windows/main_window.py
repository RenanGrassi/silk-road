import os

from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget,
    QGridLayout, QScrollArea, QGroupBox, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from src.windows.create_store_window import CreateStoreWindow
from src.windows.product_details_window import ProductDetailsWindow
from src.windows.manage_products_window import ManageProductsWindow
from src.windows.reports_window import ReportsWindow
from src.windows.transaction_history_window import TransactionHistoryWindow
from src.windows.register_products import RegisterProductWindow
from src.windows.purchase_window import PurchaseWindow

from src.server.user import UserServer
from src.server.products import ProductServer


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rota da Seda - Marketplace Distribuído")
        self.resize(1000, 600)

        # Servidores
        self.user_server = UserServer()
        self.products_server = ProductServer()

        # Layout principal
        main_layout = QHBoxLayout(self)
        self.setLayout(main_layout)

        # Lateral: menu
        self.category_list = QListWidget()
        self.category_list.addItems([
            "Autenticação",
            "Criar Loja",
            "Cadastrar Produtos",
            "Gerenciar Produtos",
            "Relatórios",
            "Histórico de Transações",
        ])
        self.category_list.setMaximumWidth(200)
        self.category_list.itemClicked.connect(self.handle_menu_click)
        main_layout.addWidget(self.category_list)

        # Conteúdo principal
        content_layout = QVBoxLayout()

        # Cabeçalho: logo + user info + sair
        header_widget = self.build_header()
        content_layout.addWidget(header_widget)

        # Campo de busca
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar produtos...")
        self.search_input.textChanged.connect(self.filter_products)
        content_layout.addWidget(self.search_input)

        # Galeria de produtos
        self.product_area = QScrollArea()
        self.product_area.setWidgetResizable(True)

        product_grid = QGridLayout()
        product_grid.setSpacing(15)
        self.product_cards = []

        products = self.products_server.list()
        for idx, product in enumerate(products):
            card = self.create_product_card(product)
            self.product_cards.append((card, product.get("name", "").lower()))
            row = idx // 3
            col = idx % 3
            product_grid.addWidget(card, row, col)

        wrapper = QWidget()
        wrapper.setLayout(product_grid)
        self.product_area.setWidget(wrapper)
        content_layout.addWidget(self.product_area)

        main_layout.addLayout(content_layout)

        # Estilo
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: Arial;
                font-size: 14px;
            }
            QListWidget {
                background-color: #ffffff;
                border: 1px solid #ccc;
            }
            QLabel {
                color: #222;
            }
            QPushButton {
                background-color: #e6e6e6;
                border: 1px solid #ccc;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #d4d4d4;
            }
        """)

    def build_header(self):
        header_layout = QHBoxLayout()

        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("src/resources/logo.png")
        logo_label.setPixmap(
            logo_pixmap.scaled(216, 72, Qt.AspectRatioMode.KeepAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)
        )
        logo_label.setFixedSize(240, 72)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # User info
        user = self.user_server.get()
        self.user_info = QLabel(f"Usuário: {user.get('name')} | Saldo: ฿{user.get('balance', 0):.2f}")
        self.user_info.setStyleSheet("color: green; font-weight: bold;")
        self.user_info.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        # Sair
        logout_button = QPushButton("Sair")
        logout_button.setStyleSheet("background-color: #ffcccc; font-weight: bold;")
        logout_button.clicked.connect(self.logout)

        right_header = QHBoxLayout()
        right_header.addWidget(self.user_info)
        right_header.addWidget(logout_button)

        right_widget = QWidget()
        right_widget.setLayout(right_header)

        header_layout.addWidget(logo_label)
        header_layout.addStretch()
        header_layout.addWidget(right_widget)

        header_widget = QWidget()
        header_widget.setLayout(header_layout)

        return header_widget

    def handle_menu_click(self, item):
        text = item.text()
        if text == "Criar Loja":
            self.create_store_window = CreateStoreWindow()
            self.create_store_window.show()
        elif text == "Gerenciar Produtos":
            self.manage_products_window = ManageProductsWindow()
            self.manage_products_window.show()
        elif text == "Relatórios":
            self.reports_window = ReportsWindow()
            self.reports_window.show()
        elif text == "Histórico de Transações":
            self.history_window = TransactionHistoryWindow()
            self.history_window.show()
        elif text == "Cadastrar Produtos":
            loja_id = 1  # Poderia ser dinâmico com base no usuário logado
            self.register_product_window = RegisterProductWindow(loja_id)
            self.register_product_window.show()

    def create_product_card(self, product: dict):
        box = QGroupBox(product.get("name", "Produto"))
        layout = QVBoxLayout()

        # Imagem
        image_path = f"client/resources/products/{product.get('images', '')}"
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(160, 120, Qt.AspectRatioMode.KeepAspectRatio)
            img_label = QLabel()
            img_label.setPixmap(pixmap)
            img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(img_label)
        else:
            layout.addWidget(QLabel("📷 Imagem não encontrada"))

        layout.addWidget(QLabel(product.get("description", "Sem descrição")))
        layout.addWidget(QLabel(f"<b>Preço: ฿{product.get('price', 0):.2f}</b>"))

        buy_button = QPushButton("Comprar")
        buy_button.clicked.connect(lambda: self.open_purchase_window(product))
        layout.addWidget(buy_button)

        box.setLayout(layout)
        return box

    def open_purchase_window(self, product):
        self.purchase_window = PurchaseWindow(product)
        self.purchase_window.finished.connect(self.atualizar_saldo)
        self.purchase_window.show()

    def atualizar_saldo(self):
        user = self.user_server.get()
        self.user_info.setText(f"Usuário: {user.get('name')} | Saldo: ฿{user.get('balance', 0):.2f}")

    def filter_products(self, text):
        text = text.lower()
        for card, name in self.product_cards:
            card.setVisible(text in name)

    def logout(self):
        from windows.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
