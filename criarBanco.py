import sqlite3
from pathlib import Path

def criar():
    diretorio_banco = Path('./meu_sistema_livraria/data/livros.db')

    if not diretorio_banco.parent.exists():
        diretorio_banco.parent.mkdir(parents=True, exist_ok=True)

    conexao = sqlite3.connect(diretorio_banco)
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano_publicacao INTEGER NOT NULL,
            preco FLOAT NOT NULL
        )
    ''')

    conexao.close()

criar()