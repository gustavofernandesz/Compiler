# Compilador 

# PROJETO DE ANÁLISE LÉXICA, SINTÁTICA E SEMÂNTICA - TEXTUAL ONTOLOGY LANGUAGE

Este projeto implementa um compilador para a linguagem TONTO (Textual Ontology Language) com as seguintes funcionalidades:

## ANÁLISE LÉXICA
* Identificação de esteriótipos de classe, esteriótipos de relações, palavras reservadas, cardinalidades, símbolos especiais, convenção para nomes de classe, convenção para nomes de relações, convenção para nomes de instâncias, tipos de dados nativos, novos tipos, meta-atributos e suas propriedades.
* Validação e classificação de tokens de acordo com suas regras, como identificadores, números inteiros, operadores aritméticos, palavras reservadas e delimitadores.
* Registro de tokens em tabelas formatadas.

## ANÁLISE SINTÁTICA
* Reconhecimento de estruturas da linguagem através de gramática formal LALR.
* Validação de declarações de pacotes, classes, tipos de dados, enumerações, relações e conjuntos de generalização.
* Construção de árvore sintática abstrata (AST).
* Detecção e relatório de erros sintáticos com sugestões de correção.
* Geração de tabela de síntese com elementos identificados.

## ANÁLISE SEMÂNTICA
* Validação de padrões de projetos de ontologias (Ontology Design Patterns - ODP)
* Identificação de padrões completos no código
* Identificação de padrões incompletos através de sobrecarregamento

## FERRAMENTAS UTILIZADAS

* Linguagem Python 3.6 ou superior
* Biblioteca PLY (Python Lex-Yacc) para análise léxica e sintática
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
pip3 install ply
```

## ESTRUTURA DO PROJETO

```
Compiler/
├── src/
│   ├── analisador_lexico.py     # Analisador léxico (lexer) da linguagem TONTO
│   ├── analisador_sintatico.py  # Analisador sintático (parser) da linguagem TONTO
│   ├── main.py                  # Script principal com menu interativo
│   ├── example.tonto            # Arquivo de exemplo em TONTO
│   ├── parser.out               # Arquivo de saída do parser (gerado automaticamente)
│   └── parsetab.py              # Tabela de parsing (gerada automaticamente)
├── data/
│   └── data.txt
└── README.md
```

## COMO EXECUTAR

### Executar o compilador

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

### Menu Interativo

Ao executar o programa, será apresentado um menu com as seguintes opções:

```
============================================================
Selecione o tipo de análise:
[1] - Análise léxica
[2] - Análise sintática
[0] - sair
============================================================
```

#### Opção 1 - Análise Léxica
Realiza a análise léxica do arquivo `example.tonto` e exibe:
* Tabela formatada com os tokens identificados (linha, tipo, valor)
* Total de tokens encontrados
* Contagem de tokens por tipo

#### Opção 2 - Análise Sintática
Realiza a análise sintática do arquivo `example.tonto` e exibe:
* Tabela de síntese com todas as estruturas identificadas (pacote, classes, tipos de dados, enumerações, relações e conjuntos de generalização)
* Relatório de erros sintáticos com sugestões de correção
* Análise detalhada é salva no arquivo `parser.out`

#### Opção 3 - Análise Semântica
* --A ser implementada--


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

## ESTRUTURAS SINTÁTICAS RECONHECIDAS

### Declaração de Pacote
```
package NomeDoPacote
```

### Declaração de Classes
```
estereotipo NomeDaClasse {
    atributo: tipo [cardinalidade] {metadados}
    @estereotipo [card] simbolo [card] ClasseRelacionada
}

estereotipo NomeDaClasse specializes ClassePai
```

### Declaração de Tipos de Dados
```
datatype NomeDoTipo {
    atributo: tipo [cardinalidade]
}
```

### Declaração de Enumerações
```
enum NomeEnum {
    Valor1, Valor2, Valor3
}
```

### Declaração de Relações
```
@estereotipo relation ClasseOrigem [card] simbolo [card] ClasseDestino

relation ClasseOrigem [card] simbolo nomeRelacao simbolo [card] ClasseDestino
```

### Conjuntos de Generalização
```
genset NomeGenSet {
    general ClasseGeral
    specifics ClasseEspecifica1, ClasseEspecifica2
}

disjoint complete genset NomeGenSet where ClasseEsp1, ClasseEsp2 specializes ClasseGeral
```

### Cardinalidades
- `[N]` - Cardinalidade exata
- `[N..M]` - Cardinalidade com intervalo
- `[N..*]` - Cardinalidade com limite superior indefinido
- `[*]` - Cardinalidade indefinida

## ESTRUTURAS SEMÂNTICAS RECONHECIDAS

### Subkind Pattern
```
package Subkind_Pattern

kind ClassName
subkind SubclassName1 specializes ClassName
subkind SubclassName2 specializes ClassName

disjoint complete genset Kind_Subkind_Genset_Name {
    general ClassName
    specifics SubclassName1, SubclassName2
}
// "complete" is optional, but "disjoint" applies to subkinds
```

### Role Pattern
```
package Role_Pattern

kind ClassName
role Role_Name1 specializes ClassName
role Role_Name2 specializes ClassName

complete genset Class_Role_Genset_Name {
    general ClassName
    specifics Role_Name1, Role_Name2
}
// "complete" is optional, but "disjoint" doesn't apply to roles
```

### Phase Pattern
```
package Phase_Pattern

kind ClassName

phase Phase_Name1 specializes ClassName
phase Phase_Name2 specializes ClassName
phase Phase_NameN specializes ClassName

disjoint complete genset Class_Phase_Genset_Name {
    general ClassName
    specifics Phase_Name1, Phase_Name2, Phase_NameN
}
// "disjoint" is mandatory for phases, but "complete" is optional
```

### Relator Pattern
```
package Relator_Pattern

kind ClassName1
kind ClassName2

role Role_Name1 specializes ClassName1
role Role_Name2 specializes ClassName2

relator Relator_Name{
    @mediation [1..*] -- [1..*] Role_Name1
    @mediation [1..*] -- [1..*] Role_Name2
}

@material relation Role_Name1 [1..*] -- relationName -- [1..*] Role_Name2
// "relationName" can be replaced by a specific name for the relation
```

### Mode Pattern
```
package Mode_Pattern

kind ClassName1
kind ClassName2

mode Mode_Name1 {
    @characterization [1..*] -- [1] ClassName1
    @externalDependence [1..*] -- [1] ClassName2
}
```

### RoleMixin Pattern
```
package RoleMixin_Pattern

kind ClassName1
kind ClassName2

roleMixin RoleMixin_Name

role Role_Name1 specializes ClassName1, RoleMixin_Name
role Role_Name2 specializes ClassName2, RoleMixin_Name

disjoint complete genset RoleMixin_Genset_Name {
    general RoleMixin_Name
    specifics Role_Name1, Role_Name2
}
```

## PERSONALIZAR ANÁLISE

Para analisar seu próprio arquivo `.tonto`, modifique o arquivo `main.py` na linha 6:

```python
# Opção 1: Arquivo no mesmo diretório do main.py
caminho_exemplo = os.path.join(diretorio_atual, 'seu_arquivo.tonto')

# Opção 2: Arquivo em outro local (caminho relativo ao main.py)
caminho_exemplo = os.path.join(diretorio_atual, '..', 'data', 'seu_arquivo.tonto')

# Opção 3: Arquivo com caminho absoluto
caminho_exemplo = '/caminho/completo/para/seu_arquivo.tonto'
```

## DETALHES DA IMPLEMENTAÇÃO

### Analisador Léxico
* Implementado usando PLY (Python Lex-Yacc)
* Reconhece tokens através de expressões regulares
* Suporta comentários de linha única (`//`) e multilinha (`/* */`)
* Diferencia tipos de identificadores por convenção de nomenclatura

### Analisador Sintático
* Implementado usando PLY com gramática LALR
* Constrói árvore sintática abstrata (AST) durante o parsing
* Implementa recuperação de erros para continuar análise após encontrar problemas
* Gera tabela de síntese com estatísticas dos elementos encontrados
* Produz relatório detalhado de erros com sugestões de correção

### Gramática
A gramática reconhece a estrutura completa da linguagem TONTO incluindo:
* Declarações de pacotes
* Classes com estereótipos OntoUML
* Relações internas e externas com cardinalidades
* Tipos de dados customizados
* Enumerações
* Conjuntos de generalização (disjoint, complete)
* Meta-atributos (const, ordered, derived, subsets, redefines)
* Padrões de Projeto de Ontologia (Ontology Design Patterns - ODP)
