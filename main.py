import pandas as pd
import banco

from pathlib import Path

diretorio_livraria = Path("meu_sistema_livraria")
diretorio_livraria.mkdir(parents=True, exist_ok=True)

def adicionar_livro():
    print('-- ADICIONAR LIVRO --')

    titulo = input('Digite o título: ')
    while not titulo.strip():
        print('O título não pode estar vazio. Digite novamente...')
        titulo = input('Digite o título: ')

    autor = input('Digite o autor: ')
    while not autor.strip():  # Garante que o autor não seja vazio
        print('O autor não pode estar vazio. Digite novamente...')
        autor = input('Digite o autor: ')

    while True:
        try:
            ano = int(input('Digite o ano de publicação: '))
            if ano < 0:
                raise ValueError('O ano não pode ser negativo.')
            break
        except ValueError as e:
            print(f'Entrada inválida: {e}. Digite novamente...')

    while True:
        try:
            preco = float(input('Digite o preço do livro: '))
            if preco < 0:
                raise ValueError('O preço não pode ser negativo.')
            break
        except ValueError as e:
            print(f'Entrada inválida: {e}. Digite novamente...')

    banco.adicionar(titulo, autor, ano, preco)
    print('Livro adicionado com sucesso!')

def listar_arquivos():
    caminho = Path('./meu_sistema_livraria/imports')

    if not caminho.exists():
        caminho.mkdir(parents=True, exist_ok=True)

    if caminho.is_dir():
        arquivos = list(caminho.iterdir())
        if arquivos:
            print("Arquivos encontrados:")

            for arquivo in arquivos:
                if arquivo.is_file():
                    print(arquivo.name)

            return True
        else:
            print("Não há arquivos no diretório.")
            return False
    else:
        print("Diretório não encontrado.")

diretorio_exports = Path('./meu_sistema_livraria/exports')
if not diretorio_exports.exists():
    diretorio_exports.mkdir(parents=True, exist_ok=True)

diretorio_imports = Path('./meu_sistema_livraria/imports')
if not diretorio_imports.exists():
    diretorio_imports.mkdir(parents=True, exist_ok=True)

while True:
    print('1. Adicionar novo livro')
    print('2. Exibir todos os livros')
    print('3. Atualizar preço de um livro')
    print('4. Remover um livro')
    print('5. Buscar livros por autor')
    print('6. Exportar livros para CSV')
    print('7. Importar dados de CSV')
    print('8. Fazer backup do banco de dados')
    print('9. Sair')

    while True:
        try:
            opcao = int(input('Digite uma opção: '))
            if opcao < 1 or opcao > 9:
                raise ValueError('A opção não pode exceder os limites')
            break
        except ValueError as e:
            print(f'Entrada inválida: {e}. Digite novamente...')


    if opcao == 1:
        adicionar_livro()
    elif opcao == 2:
        print(banco.exibir_livros())
    elif opcao == 3:
        id_livro = int(input('Digite o id do livro: '))

        if not banco.verificar_livro_existente(id_livro):
            preco = float(input('Digite o preço do livro: '))
            banco.atualizar_preco(id_livro, preco)
        else:
            print('>> Livro não existente no banco de dados')

    elif opcao == 4:
        id_livro = int(input('Digite o id do livro: '))

        if not banco.verificar_livro_existente(id_livro):
            print('======= LIVRO =======')
            print(banco.impirmir_livro(id_livro))

            while True:
                confirmacao = input('Deseja confirmar a remoção do livro? [S/N] ').strip().upper()

                if confirmacao == 'S':
                    banco.remover_livro(id_livro)
                    print(f'>> Livro "{id_livro}" removido com sucesso!')
                    break
                elif confirmacao == 'N':
                    print('Remoção de livro cancelada!')
                    break
                else:
                    print('Entrada inválida. Por favor, digite S para Sim ou N para Não.')
        else:
            print('>> Livro não existente no banco de dados')

    elif opcao == 5:
        nome_autor = input('Digite o nome do autor: ')
        print(banco.buscar_por_autor(nome_autor))
    elif opcao == 6:
        nome_arquivo = input('Digite o nome do arquivo: ')
        print('>> Livros exportados para: ' + banco.exportar_livros(nome_arquivo))
    elif opcao == 7:
        if not listar_arquivos():
            print('>> Adicione um arquivo no diretório')
        else:
            nome_arquivo = input('Digite o nome do arquivo (sem o tipo do arquivo): ')
            banco.importar_livros(nome_arquivo)

    elif opcao == 8:
        print('Backup criado em: ' + banco.backup_banco())
    else:
        break