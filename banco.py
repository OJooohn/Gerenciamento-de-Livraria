import sqlite3

conexao = sqlite3.connect('meu_banco.db')
backup = sqlite3.connect('backup_banco.db')

cursor = conexao.cursor()

def criar_banco():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano_publicacao INTEGER NOT NULL,
            preco FLOAT NOT NULL
        )
    ''')

def criar_banco_backup():
    backup.cursor().execute('''
        CREATE TABLE IF NOT EXISTS livros(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano_publicacao INTEGER NOT NULL,
            preco FLOAT NOT NULL
        )
    ''')

criar_banco()
criar_banco_backup()

def backup_banco():
    # Receber os do banco de dados normal
    import pandas as pd
    query = 'SELECT titulo, autor, ano_publicacao, preco FROM livros'

    # O read_sql_query funciona como dicionário
    tabela = pd.read_sql_query(query, conexao)
    # print(tabela)

    livros = []
    for index, row in tabela.iterrows():
        livros.append((row['titulo'], row['autor'], row['ano_publicacao'], row['preco']))

    # Passar os dados para o backup_banco.db
    if not tabela.empty:
        # Uma maneira NADA otimizada para atualizar os dados do backup
        # 
        backup.cursor().execute('DROP TABLE livros')
        criar_banco_backup()

        backup.cursor().executemany('''
            INSERT INTO livros (titulo, autor, ano_publicacao, preco) VALUES (?, ?, ?, ?)
        ''', livros)
        backup.commit()

def adicionar(titulo : str, autor : str, ano : int, preco : float):
    # Realizar o backup antes de adicionar um novo livro
    backup_banco()

    conexao.cursor().execute('''
        INSERT INTO livros (titulo, autor, ano_publicacao, preco) VALUES (?, ?, ?, ?)
    ''', (titulo, autor, ano, preco))

    conexao.commit()