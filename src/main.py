import os
import analisador_lexico
import analisador_sintatico

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_exemplo = os.path.join(diretorio_atual, 'example.tonto')

with open(caminho_exemplo, 'r') as f:
    codigo = f.read()


print(f"\nArquivo: {caminho_exemplo}")

lexer = analisador_lexico.build()
tabela, contagem = analisador_lexico.lex_table(codigo, lexer)
analisador_lexico.exibir_analise_lexica(tabela, contagem)

resultado, ast = analisador_sintatico.parse(codigo)
analisador_sintatico.exibir_analise_sintatica()

print("\n" + "="*80)
print("FIM DA ANÁLISE")
print("="*80)
