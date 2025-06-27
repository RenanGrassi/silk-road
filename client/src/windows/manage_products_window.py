from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHBoxLayout,
)
from src.server.products import ProductServer, ProductIdModel


class ManageProductsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciar Produtos")
        self.resize(900, 500)
        self.product_server = ProductServer()
        layout = QVBoxLayout()

        label = QLabel("<h2>Seus Produtos</h2>")
        layout.addWidget(label)

        # Tabela com 5 colunas: Nome, Preço, Quantidade, Status, Ações
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Produto", "Preço", "Status", "Ações"])
        self.table.verticalHeader().setDefaultSectionSize(50)

        self.table.setColumnWidth(0, 250)  # Produto
        self.table.setColumnWidth(1, 100)  # Preço
        self.table.setColumnWidth(2, 100)  # Quantidade
        self.table.setColumnWidth(3, 200)  # Status

        self.refresh_table()

        layout.addWidget(self.table)
        self.setLayout(layout)

    def toggle_set_status(self, product):
        if product.get("is_active"):
            self.product_server.deactivate_announcement(
                ProductIdModel(**{"product_id": product["id"]})
            )
        else:
            self.product_server.activate_announcement(
                ProductIdModel(**{"product_id": product["id"]})
            )
        self.refresh_table()

    def toggle_delete_product(self, product):
        self.product_server.delete(ProductIdModel(**{"product_id": product["id"]}))
        self.refresh_table()

    def refresh_table(self):
        products = self.product_server.get_by_shop()
        self.table.setRowCount(len(products))

        for row, prod in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(prod["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(f"${prod.get('price')}"))
            self.table.setItem(
                row,
                2,
                QTableWidgetItem("Ativo" if prod.get("is_active", True) else "Pausado"),
            )

            # Atualiza os botões de ação
            btn_pause = QPushButton("⏸" if prod.get("is_active") else "▶️")
            btn_delete = QPushButton("❌")

            btn_pause.clicked.connect(lambda _, p=prod: self.toggle_set_status(p))
            btn_delete.clicked.connect(lambda _, p=prod: self.toggle_delete_product(p))

            action_layout = QHBoxLayout()
            action_layout.addWidget(btn_pause)
            action_layout.addWidget(btn_delete)

            action_cell = QWidget()
            action_cell.setLayout(action_layout)
            self.table.setCellWidget(row, 3, action_cell)
