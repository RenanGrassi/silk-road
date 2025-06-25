from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QTableWidget,
    QTableWidgetItem
)
from PyQt6.QtCore import Qt

class TransactionHistoryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Histórico de Transações")
        self.resize(600, 400)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("<h2>Histórico de Transações</h2>"))

        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Data", "Produto", "Quantidade", "Valor"])

        # Dados simulados
        transacoes = [
            {"data": "2025-06-20", "produto": "Produto A", "quantidade": 2, "valor": "฿41.00"},
            {"data": "2025-06-21", "produto": "Produto C", "quantidade": 1, "valor": "฿19.25"},
            {"data": "2025-06-22", "produto": "Produto A", "quantidade": 1, "valor": "฿20.50"},
        ]

        table.setRowCount(len(transacoes))

        for row, t in enumerate(transacoes):
            table.setItem(row, 0, QTableWidgetItem(t["data"]))
            table.setItem(row, 1, QTableWidgetItem(t["produto"]))
            table.setItem(row, 2, QTableWidgetItem(str(t["quantidade"])))
            table.setItem(row, 3, QTableWidgetItem(t["valor"]))

            for col in range(4):
                table.item(row, col).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(table)
        self.setLayout(layout)
