import os
import analisador_lexico
import analisador_sintatico
import analisador_semantico

LARGURA = 80

def linha(char="="):
    return char * LARGURA

def cabecalho(titulo):
    print("\n" + linha())
    print(titulo.center(LARGURA))
    print(linha())

def subcabecalho(titulo):
    print("\n" + linha("-"))
    print(titulo)
    print(linha("-"))

def menu():
    print("\n" + linha())
    print("COMPILADOR TONTO".center(LARGURA))
    print("Análise Léxica, Sintática e Semântica".center(LARGURA))
    print(linha())
    print("\n  [1] Análise Léxica")
    print("  [2] Análise Sintática")
    print("  [3] Análise Semântica")
    print("  [0] Sair")
    print()

def analise_lexica(codigo):
    cabecalho("ANÁLISE LÉXICA")
    
    lexer = analisador_lexico.build()
    tabela, contagem = analisador_lexico.lex_table(codigo, lexer)
    
    subcabecalho("TABELA DE TOKENS")
    print(f"\n  {'LINHA':<8} {'TOKEN':<25} {'VALOR'}")
    print("  " + "-" * 50)
    for linha_num, tipo, valor in tabela:
        print(f"  {linha_num:<8} {tipo:<25} {valor}")
    
    subcabecalho("RESUMO")
    print(f"\n  Total de tokens: {len(tabela)}")
    print()
    print(f"  {'TIPO':<25} {'QTD':>5}")
    print("  " + "-" * 32)
    for tipo, qtd in sorted(contagem.items()):
        print(f"  {tipo:<25} {qtd:>5}")
    
    print("\n" + linha())
    print("Análise léxica concluída com sucesso.".center(LARGURA))
    print(linha())

def analise_sintatica(codigo):
    resultado, ast = analisador_sintatico.parse(codigo)
    analisador_sintatico.gerar_tabela_sintese()
    analisador_sintatico.gerar_relatorio_erros()

def analise_semantica(codigo):
    resultado, ast = analisador_sintatico.parse(codigo)
    analisador_semantico.analisar(ast)


diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_exemplo = os.path.join(diretorio_atual, 'example.tonto')

with open(caminho_exemplo, 'r') as f:
    codigo = f.read()

opcao = None
while opcao != "0":
    menu()
    opcao = input("  Escolha uma opção: ").strip()
    
    if opcao == "1":
        analise_lexica(codigo)
    elif opcao == "2":
        analise_sintatica(codigo)
    elif opcao == "3":
        analise_semantica(codigo)
    elif opcao == "0":
        print("\n" + linha())
        print("Encerrando...".center(LARGURA))
        print(linha() + "\n")
    else:
        print("\n  [ERRO] Opção inválida!")
