# test_lexer.py
import sys
sys.path.append('/home/ricardo/Compiler/src')
import principal

# Lê o arquivo de exemplo
with open('/home/ricardo/Compiler/src/example.tonto', 'r') as f:
    codigo = f.read()

# Constrói o lexer
lexer = principal.build()

# Gera a tabela de tokens
tabela = principal.lex_table(codigo, lexer)

# Exibe a tabela formatada
print(f"{'Linha':<8} {'Token':<25} {'Valor'}")
print("=" * 60)
for linha, tipo, valor in tabela:
    print(f"{linha:<8} {tipo:<25} {valor}")

print(f"\nTotal de tokens: {len(tabela)}")