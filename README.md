# Compilador 

# PROJETO DE ANÁLISE LÉXICA - TEXTUAL ONTOLOGY LANGUAGE

Esse projeto faz as seguintes funcionalidades léxicas:
* Identificação de esteriótipos de classe, esteriótipos de relações, palavras reservadas, cardinalidades, símbolos especiais, convenção para nomes de classe, convenção para nomes de relações, convenção para nomes de instâncias, tipos de dados nativos, novos tipos, meta-atributos e suas propriedades.
* Validação e classificação de tokens de acordo com suas regras, como identificadores, números inteiros, operadores aritméticos, palavras reservadas e delimitadores.
* Registro de tokens.

## FERRAMENTAS UTILIZADAS

* Linguagem Python e biblioteca PLY para análise léxica.
* Ambiente de trabalho: PyCharm 2025.2.2 nos sistemas operacionais Windows e Linux (Debian)

## PRÉ-REQUISITOS

* Python 3.6 ou superior
* pip (gerenciador de pacotes do Python)

## INSTALAÇÃO

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd Compiler
```

2. Instale as dependências:
```bash
pip3 install -r requirements.txt
```

Ou instale manualmente:
```bash
pip3 install ply
```

## ESTRUTURA DO PROJETO

```
Compiler/
├── src/
│   ├── principal.py    # Analisador léxico (lexer) da linguagem TONTO
│   ├── main.py         # Script de teste do lexer
│   └── example.tonto   # Arquivo de exemplo em TONTO
├── data/
│   └── data.txt
└── README.md
```

## COMO EXECUTAR

### Executar análise léxica do arquivo de exemplo

O script pode ser executado de qualquer diretório:

**Opção 1: A partir do diretório raiz do projeto**
```bash
python3 src/main.py
```

**Opção 2: A partir do diretório src**
```bash
cd src
python3 main.py
```

Este comando irá:
1. Ler o arquivo `example.tonto`
2. Realizar a análise léxica
3. Exibir uma tabela formatada com os tokens identificados (linha, tipo, valor)
4. Mostrar a contagem de tokens por tipo


## TIPOS DE TOKENS RECONHECIDOS

### Estereótipos
- **EST_CLASS**: Estereótipos de classe (kind, phase, role, etc.)
- **EST_REL**: Estereótipos de relação (mediation, componentOf, etc.)

### Identificadores
- **CLASS_NAME**: Nomes de classes (começam com maiúscula)
- **RELATION_NAME**: Nomes de relações/propriedades (começam com minúscula)
- **INSTANCE**: Instâncias (terminam com dígitos)
- **NEW_DATATYPE**: Novos tipos de dados (terminam com DataType)

### Tipos Nativos
- **NATIVE_STRING**: Tipo string
- **NATIVE_NUMBER**: Tipo number
- **NATIVE_BOOLEAN**: Tipo boolean
- **NATIVE_DATE**: Tipo date
- **NATIVE_TIME**: Tipo time
- **NATIVE_DATETIME**: Tipo datetime

### Meta-atributos
- **META_CONST**: const
- **META_ORDERED**: ordered
- **META_DERIVED**: derived
- **META_SUBSETS**: subsets
- **META_REDEFINES**: redefines

### Palavras Reservadas
- PACKAGE, ENUM, RELATION, DATATYPE, GENSET, SPECIALIZES, etc.

### Símbolos
- LBRACE `{`, RBRACE `}`
- LBRACKET `[`, RBRACKET `]`
- LPAREN `(`, RPAREN `)`
- COMMA `,`, COLON `:`
- DOT `.`, HYPHEN `-`
- CONTEM `<>--`, CONTIDO `--<>`
- ARROBA `@`, ASTERISCO `*`

## PERSONALIZAR ANÁLISE

Para analisar seu próprio arquivo `.tonto`, modifique o arquivo `main.py`:

```python
# Opção 1: Arquivo no mesmo diretório do main.py
caminho_exemplo = os.path.join(diretorio_atual, 'seu_arquivo.tonto')

# Opção 2: Arquivo em outro local (caminho relativo ao main.py)
caminho_exemplo = os.path.join(diretorio_atual, '..', 'data', 'seu_arquivo.tonto')

# Opção 3: Arquivo com caminho absoluto
caminho_exemplo = '/caminho/completo/para/seu_arquivo.tonto'
```
