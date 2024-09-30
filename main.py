import pandas as pd
import banco

from pathlib import Path

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
    caminho = Path('./imports')

    if caminho.exists() and caminho.is_dir():
        print("Arquivos encontrados:")

        for arquivo in caminho.iterdir():
            if arquivo.is_file():
                print(arquivo.name)
    else:
        print("Diretório não encontrado.")

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
        nome_livro = input('Digite o nome do livro: ')

        if not banco.verificar_livro_existente(nome_livro):
            preco = float(input('Digite o preço do livro: '))
            banco.atualizar_preco(nome_livro, preco)
        else:
            print('>> Livro não existente no banco de dados')

    elif opcao == 4:
        nome_livro = input('Digite o nome do livro: ')

        if not banco.verificar_livro_existente(nome_livro):
            print('======= LIVRO =======')
            print(banco.impirmir_livro(nome_livro))

            while True:
                confirmacao = input('Deseja confirmar a remoção do livro? [S/N] ').strip().upper()

                if confirmacao == 'S':
                    banco.remover_livro(nome_livro)
                    print(f'>> Livro "{nome_livro}" removido com sucesso!')
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
        listar_arquivos()

        nome_arquivo = input('Digite o nome do arquivo (sem o tipo do arquivo): ')
        banco.importar_livros(nome_arquivo)

    elif opcao == 8:
        print('Backup criado em: ' + banco.backup_banco())
    else:
        break