import os
import shutil

from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QMessageBox, QFileDialog
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from src.server.products import ProductServer
from src.server.models.products import ProductModel, ProductIdModel


class RegisterProductWindow(QWidget):
    def __init__(self, loja_id: int):
        super().__init__()
        self.setWindowTitle("Cadastro de Produto")
        self.resize(400, 550)
        self.loja_id = loja_id

        self.selected_image_path = ""
        self.product_server = ProductServer()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h3>Novo Produto</h3>"))

        # Nome
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nome do produto")
        layout.addWidget(self.name_input)

        # Descrição
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Descrição do produto")
        self.description_input.setFixedHeight(80)
        layout.addWidget(self.description_input)

        # Preço
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Preço (ex: 19.99)")
        layout.addWidget(self.price_input)

        # Imagem
        self.image_label = QLabel("Nenhuma imagem selecionada")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedHeight(150)
        layout.addWidget(self.image_label)

        self.select_image_button = QPushButton("Escolher Imagem")
        self.select_image_button.clicked.connect(self.select_image)
        layout.addWidget(self.select_image_button)

        # Botão de cadastrar
        self.create_button = QPushButton("Cadastrar Produto")
        self.create_button.clicked.connect(self.register_product)
        layout.addWidget(self.create_button)

        self.setLayout(layout)

    def select_image(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(
            self, "Selecionar Imagem", "", "Imagens (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.selected_image_path = file_path
            pixmap = QPixmap(file_path).scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)
        else:
            self.selected_image_path = ""
            self.image_label.setText("Nenhuma imagem selecionada")

    def register_product(self):
        name = self.name_input.text().strip()
        description = self.description_input.toPlainText().strip()
        price = self.price_input.text().strip()

        if not name or not price or not self.selected_image_path:
            QMessageBox.warning(self, "Erro", "Preencha nome, preço e selecione uma imagem.")
            return

        try:
            price_float = float(price)
        except ValueError:
            QMessageBox.warning(self, "Erro", "Preço inválido.")
            return

        # 1. Envia via Pyro (sem imagem ainda)
        product_model = ProductModel(
            name=name,
            description=description,
            price=price_float,
            images="",  # será atualizado depois
            loja_id=self.loja_id
        )

        create_response = self.product_server.create(product_model)

        if "error" in create_response.keys():
            QMessageBox.warning(self, "Erro", create_response.get("error"))
            return

        # 2. Obtém o ID do último produto da loja

        product_id = create_response.get("id")

        # 3. Salva a imagem no caminho certo
        ext = os.path.splitext(self.selected_image_path)[1] or ".png"
        filename = f"{product_id}{ext}"
        dest_folder = "src/resources/products"
        os.makedirs(dest_folder, exist_ok=True)
        dest_path = os.path.join(dest_folder, filename)

        try:
            shutil.copy(self.selected_image_path, dest_path)
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao salvar imagem: {e}")
            return

        QMessageBox.information(self, "Sucesso", f"Produto '{name}' cadastrado com imagem salva!")
        self.close()
