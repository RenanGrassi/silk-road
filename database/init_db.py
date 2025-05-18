import sqlite3
from pathlib import Path

# TODO - Passar isso daqui pra um arquivo SQL
# Caminho do banco de dados
db_path = Path(__file__).parent / "silk_road.db"

# Conexão e criação do banco de dados
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Tabela de usuários
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_usuario TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
);
"""
)

# Tabela de lojas
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS lojas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    usuario_id INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
"""
)

# Tabela de produtos
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    preco REAL NOT NULL,
    imagem1 TEXT NOT NULL,
    imagem2 TEXT,
    imagem3 TEXT,
    status TEXT DEFAULT 'ativo',
    loja_id INTEGER NOT NULL,
    FOREIGN KEY (loja_id) REFERENCES lojas(id)
);
"""
)

# Tabela de transações
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS transacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comprador_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 1,
    data TEXT NOT NULL,
    FOREIGN KEY (comprador_id) REFERENCES usuarios(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);
"""
)
