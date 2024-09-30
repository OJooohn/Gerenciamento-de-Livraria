import datetime
import sqlite3
import criarBanco
import pandas as pd
from pathlib import Path

def is_empty(cursor):
    cursor.execute("SELECT COUNT(*) FROM livros")
    resultado = cursor.fetchone()[0]

    return resultado == 0

def verificar_livro_existente(titulo : str):
    diretorio_banco = Path('./data/livros.db')

    conexao = sqlite3.connect(diretorio_banco)
    cursor = conexao.cursor()

    cursor.execute('SELECT COUNT(*) FROM livros WHERE titulo = ?', (titulo, ))
    resultado = cursor.fetchone()[0]

    return resultado == 0

def impirmir_livro(titulo : str):
    diretorio_banco = Path('./data/livros.db')

    conexao = sqlite3.connect(diretorio_banco)

    query = 'SELECT titulo, autor, ano_publicacao, preco FROM livros WHERE titulo = ?'

    livro = pd.read_sql_query(query, conexao, params=(titulo,))

    conexao.close()

    return livro.to_string(index=False)

def backup_banco():
    diretorio_banco = Path('./data/livros.db')

    # Conectando ao banco original
    conexao = sqlite3.connect(diretorio_banco)

    # Caso o banco nao exista, ira criar
    if not conexao:
        criarBanco.criar()

    # Pegando dados para a criação do backup
    data_hora = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    diretorio_backup = Path(f'./backups/backup_livraria_{data_hora}.db')

    if not diretorio_backup.parent.exists():
        diretorio_backup.parent.mkdir(parents=True, exist_ok=True)

    backup = sqlite3.connect(diretorio_backup)

    backup.cursor().execute('''
        CREATE TABLE IF NOT EXISTS livros(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano_publicacao INTEGER NOT NULL,
            preco FLOAT NOT NULL
        )
    ''')

    conexao.backup(backup, pages=1)

    conexao.close()
    backup.close()

    return str(diretorio_backup)

def adicionar(titulo : str, autor : str, ano : int, preco : float):
    diretorio_banco = Path('./data/livros.db')

    conexao = sqlite3.connect(diretorio_banco)
    cursor = conexao.cursor()

    # Realizar o backup antes de adicionar um novo livro
    if not is_empty(cursor):
        backup_banco()

    cursor.execute('''
        INSERT INTO livros (titulo, autor, ano_publicacao, preco) VALUES (?, ?, ?, ?)
    ''', (titulo, autor, ano, preco))
    conexao.commit()

    conexao.close()

def exibir_livros():
    diretorio_banco = Path('./data/livros.db')

    conexao = sqlite3.connect(diretorio_banco)

    query = 'SELECT titulo, autor, ano_publicacao, preco FROM livros'
    tabela_livros = pd.read_sql_query(query, conexao)
    return tabela_livros.to_string(index=False)

def atualizar_preco(titulo : str, preco : float):
    diretorio_banco = Path('./data/livros.db')

    conexao = sqlite3.connect(diretorio_banco)
    cursor = conexao.cursor()

    backup_banco()

    cursor.execute('''
        UPDATE livros SET preco = ? WHERE titulo = ?
    ''', (preco, titulo))

    conexao.commit()

    print('>> Preco atualizado com sucesso!')

    conexao.close()

def remover_livro(titulo : str):
    diretorio_banco = Path('./data/livros.db')

    conexao = sqlite3.connect(diretorio_banco)
    cursor = conexao.cursor()

    backup_banco()

    cursor.execute('DELETE FROM livros WHERE titulo = ?', (titulo, ))
    conexao.commit()

    conexao.close()

def buscar_por_autor(nome_autor):
    diretorio_banco = Path('./data/livros.db')

    conexao = sqlite3.connect(diretorio_banco)
    cursor = conexao.cursor()

    query = 'SELECT * FROM livros WHERE autor = ?'

    tabela_livro = pd.read_sql_query(query, conexao, params=(nome_autor, ))

    conexao.close()

    return tabela_livro.to_string(index=False)

def exportar_livros(nome_arquivo : str):
    diretorio_banco = Path('./data/livros.db')

    conexao = sqlite3.connect(diretorio_banco)
    cursor = conexao.cursor()

    query = 'SELECT * FROM livros'
    tabela_livros = pd.read_sql_query(query, conexao)

    diretorio_exportado = Path(f'./exports/{nome_arquivo}.csv')

    if not diretorio_exportado.parent.exists():
        diretorio_exportado.parent.mkdir(parents=True, exist_ok=True)

    tabela_livros.to_csv(diretorio_exportado, index=False)

    conexao.close()

    return str(diretorio_exportado)

def importar_livros(nome_arquivo):
    diretorio_banco = Path('./data/livros.db')

    conexao = sqlite3.connect(diretorio_banco)
    cursor = conexao.cursor()

    diretorio_imports = Path(f'./imports/{nome_arquivo}.csv')

    try:
        df = pd.read_csv(diretorio_imports)

        df.to_sql('livros', conexao, if_exists='append', index=False)

        print(f'Dados importados de {nome_arquivo}.csv com sucesso!')
    except Exception as e:
        print(f'Erro ao importar dados: {e}')
    finally:
        conexao.close()