from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt


class ReportsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Relatórios e Histórico de Transações")
        self.resize(700, 500)

        layout = QVBoxLayout()

        # Simulação de dados de relatório
        total_vendas = 4
        total_faturado = "฿128.75"

        produtos_estoque = [
            {"nome": "Produto A", "estoque": 6},
            {"nome": "Produto C", "estoque": 2}
        ]

        historico = [
            {"data": "2025-06-20", "produto": "Produto A", "qtd": 2, "valor": "฿41.00"},
            {"data": "2025-06-21", "produto": "Produto C", "qtd": 1, "valor": "฿19.25"},
            {"data": "2025-06-21", "produto": "Produto A", "qtd": 1, "valor": "฿20.50"},
        ]

        # 🔢 Resumo geral
        layout.addWidget(QLabel(f"<h3>Total de Vendas: {total_vendas}</h3>"))
        layout.addWidget(QLabel(f"<h3>Total Faturado: {total_faturado}</h3>"))
        layout.addWidget(QLabel("<h4>Estoque Atual:</h4>"))

        for prod in produtos_estoque:
            layout.addWidget(QLabel(f"- {prod['nome']}: {prod['estoque']} unidades"))

        # 📊 Tabela de histórico de vendas
        layout.addWidget(QLabel("<h4>Histórico de Transações:</h4>"))

        table = QTableWidget()
        table.setRowCount(len(historico))
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Data", "Produto", "Qtd", "Valor"])

        for row, item in enumerate(historico):
            table.setItem(row, 0, QTableWidgetItem(item["data"]))
            table.setItem(row, 1, QTableWidgetItem(item["produto"]))
            table.setItem(row, 2, QTableWidgetItem(str(item["qtd"])))
            table.setItem(row, 3, QTableWidgetItem(item["valor"]))

            for col in range(4):
                table.item(row, col).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        table.setColumnWidth(0, 100)
        table.setColumnWidth(1, 200)
        table.setColumnWidth(2, 80)
        table.setColumnWidth(3, 100)

        layout.addWidget(table)
        self.setLayout(layout)
