from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QHBoxLayout
)


class ManageProductsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciar Produtos")
        self.resize(900, 500)

        layout = QVBoxLayout()

        label = QLabel("<h2>Seus Produtos</h2>")
        layout.addWidget(label)

        # Tabela com 5 colunas: Nome, Preço, Quantidade, Status, Ações
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Produto", "Preço", "Qtd", "Status", "Ações"])
        self.table.verticalHeader().setDefaultSectionSize(50)

        self.table.setColumnWidth(0, 250)  # Produto
        self.table.setColumnWidth(1, 100)  # Preço
        self.table.setColumnWidth(2, 80)   # Quantidade
        self.table.setColumnWidth(3, 100)  # Status
        self.table.setColumnWidth(4, 200)  # Ações


        # Simulando produtos cadastrados
        fake_products = [
            {"nome": "Produto A", "preco": "฿2.00", "quantidade": "10", "status": "Ativo"},
            {"nome": "Produto B", "preco": "฿3.50", "quantidade": "0", "status": "Pausado"},
            {"nome": "Produto C", "preco": "฿1.25", "quantidade": "5", "status": "Ativo"},
        ]

        self.table.setRowCount(len(fake_products))

        for row, prod in enumerate(fake_products):
            self.table.setItem(row, 0, QTableWidgetItem(prod["nome"]))
            self.table.setItem(row, 1, QTableWidgetItem(prod["preco"]))
            self.table.setItem(row, 2, QTableWidgetItem(prod["quantidade"]))
            self.table.setItem(row, 3, QTableWidgetItem(prod["status"]))

            # Botões de ação
            btn_pause = QPushButton("⏸" if prod["status"] == "Ativo" else "▶️")
            btn_delete = QPushButton("❌")

            action_layout = QHBoxLayout()
            action_layout.addWidget(btn_pause)
            action_layout.addWidget(btn_delete)

            # Widget de ações
            action_cell = QWidget()
            action_cell.setLayout(action_layout)
            self.table.setCellWidget(row, 4, action_cell)

        layout.addWidget(self.table)
        self.setLayout(layout)
