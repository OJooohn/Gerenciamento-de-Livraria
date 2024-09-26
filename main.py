import pandas as pd
import banco

def adicionar_livro():
    print('-- ADICIONAR LIVRO --')
    titulo = input('Digite o título: ')
    autor = input('Digite o autor: ')
    ano = int(input('Digite o ano de publicação: '))
    preco = float(input('Digite o preço do livro: '))

    # Chama a funcao de banco.py para adicionar
    banco.adicionar(titulo, autor, ano, preco)

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

    opcao = int(input('Digite uma opção: '))

    if opcao == 1:
        adicionar_livro()
    elif opcao == 2:
        print('2')
    elif opcao == 3:
        print('3')
    elif opcao == 4:
        print('4')
    elif opcao == 5:
        print('5')
    elif opcao == 6:
        print('6')
    elif opcao == 7:
        print('7')
    elif opcao == 8:
        print('8')
    else:
        break