import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
import principal


# Verifica se o usuário passa um argumento, ao invés de sempre tentar abrir o mesmo arquivo
if len(sys.argv) < 2:
    print("Uso: python src/main.py <arquivo.tonto>")
    sys.exit(1)

file_path = sys.argv[1]

# Verificando pra ver se o arquivo existe
if not os.path.exists(file_path):
    print(f"Erro: arquivo '{file_path}' não encontrado.")
    sys.exit(1)

# Lendo o conteúdo do arquivo
with open(file_path, 'r') as f:
    data = f.read()
lexer = principal.build()

tabela, contagem = principal.lex_table(data, lexer)

print(f"{'Linha':<8} {'Token':<25} {'Valor'}")
print("=" * 60)
for linha, tipo, valor in tabela:
    print(f"{linha:<8} {tipo:<25} {valor}")

print(f"\nTotal de tokens: {len(tabela)}")
print("\nContagem por tipo:")
print("=" * 30)
for tipo, qtd in contagem.items():
    print(f"{tipo:<25}: {qtd}")
