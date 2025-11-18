import os
import analisador_lexico
import analisador_sintatico

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_exemplo = os.path.join(diretorio_atual, 'example.tonto')

with open(caminho_exemplo, 'r') as f:
    codigo = f.read()

lexer = analisador_lexico.build()

tabela, contagem = analisador_lexico.lex_table(codigo, lexer)

print(f"{'Linha':<8} {'Token':<25} {'Valor'}")
print("=" * 60)
for linha, tipo, valor in tabela:
    print(f"{linha:<8} {tipo:<25} {valor}")

print(f"\nTotal de tokens: {len(tabela)}")
print("\nContagem por tipo:")
print("=" * 30)
for tipo, qtd in contagem.items():
    print(f"{tipo:<25}: {qtd}")

resultado, ast = analisador_sintatico.parse(codigo)

analisador_sintatico.gerar_tabela_sintese()
analisador_sintatico.gerar_relatorio_erros()
