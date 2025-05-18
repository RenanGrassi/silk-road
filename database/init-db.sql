CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS shop (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    images TEXT NOT NULL,
    imagem2 TEXT,
    imagem3 TEXT,
    status TEXT DEFAULT 'ativo',
    loja_id INTEGER NOT NULL,
    FOREIGN KEY (loja_id) REFERENCES lojas(id)
);

CREATE TABLE IF NOT EXISTS images (
    name TEXT NOT NULL,
    alt_text TEXT NOT NULL,
    url TEXT NOT NULL,
)