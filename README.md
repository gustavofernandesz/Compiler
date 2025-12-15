# Compilador 

# PROJETO DE ANÁLISE LÉXICA, SINTÁTICA E SEMÂNTICA - TEXTUAL ONTOLOGY LANGUAGE

Este projeto implementa um compilador para a linguagem TONTO (Textual Ontology Language) com as seguintes funcionalidades:

## ANÁLISE LÉXICA
* Identificação de estereótipos de classe, estereótipos de relações, palavras reservadas, cardinalidades, símbolos especiais, convenção para nomes de classe, convenção para nomes de relações, convenção para nomes de instâncias, tipos de dados nativos, novos tipos, meta-atributos e suas propriedades.
* Validação e classificação de tokens de acordo com suas regras.
* Registro de tokens em tabelas formatadas.

## ANÁLISE SINTÁTICA
* Reconhecimento de estruturas da linguagem através de gramática formal LALR.
* Validação de declarações de pacotes, classes, tipos de dados, enumerações, relações e conjuntos de generalização.
* Construção de árvore sintática abstrata (AST).
* Detecção e relatório de erros sintáticos com sugestões de correção.
* Geração de tabela de síntese com elementos identificados.

## ANÁLISE SEMÂNTICA
* Validação de Padrões de Projeto de Ontologia (Ontology Design Patterns - ODP).
* Identificação de padrões completos e incompletos no código.
* Resolução automática de imports entre arquivos.
* Geração de relatório com classificação: `[OK]`, `[ALERTA]` ou `[INFO]`.

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
│   ├── analisador_lexico.py     # Analisador léxico (lexer)
│   ├── analisador_sintatico.py  # Analisador sintático (parser)
│   ├── analisador_semantico.py  # Analisador semântico (validação ODP)
│   ├── main.py                  # Script principal com menus
│   └── example.tonto            # Arquivo de exemplo
├── Compiladores_UFERSA-main/    # Pasta de testes
│   ├── CarExample/              # Exemplo de aluguel de carros
│   ├── FoodAllergyExample/      # Exemplo de alergia alimentar
│   ├── Hospital_Model/          # Modelo de hospital/UBS
│   ├── Ontology Design Patterns em Tonto/  # 6 padrões ODP
│   ├── Pizzaria_Model/          # Modelo de pizzaria
│   └── TDAHExample/             # Exemplo TDAH
├── data/
│   └── data.txt
└── README.md
```

## COMO EXECUTAR

```bash
python3 src/main.py
```

### Menu Principal

```
================================================================================
                                COMPILADOR TONTO                                
                     Análise Léxica, Sintática e Semântica                      
================================================================================

  [1] Selecionar Arquivo de Teste
  [0] Sair
```

### Menu de Seleção de Projeto

Ao escolher a opção 1, será exibida a lista de projetos de teste disponíveis:

```
================================================================================
                          SELEÇÃO DE PROJETO DE TESTE                           
================================================================================
  [1] CarExample (2 arquivo(s))
  [2] FoodAllergyExample (1 arquivo(s))
  [3] Hospital_Model (7 arquivo(s))
  [4] Ontology Design Patterns em Tonto (6 arquivo(s))
  [5] Pizzaria_Model (8 arquivo(s))
  [6] TDAHExample (1 arquivo(s))

  [7] Arquivo local (example.tonto)
  [0] Voltar
```

Após selecionar o projeto, escolha o arquivo `.tonto` específico.

### Menu de Análise

```
--------------------------------------------------------------------------------
ARQUIVO: src/Cliente.tonto
--------------------------------------------------------------------------------

  [1] Análise Léxica
  [2] Análise Sintática
  [3] Análise Semântica 

  [4] Trocar arquivo
  [0] Sair
```

## TIPOS DE ANÁLISE

### Análise Léxica
* Tabela de tokens identificados (linha, tipo, valor)
* Total de tokens encontrados
* Contagem por tipo de token

### Análise Sintática
* Tabela de síntese com estruturas identificadas
* Relatório de erros com sugestões de correção

### Análise Semântica
* Resolução automática de imports (carrega arquivos dependentes)
* Validação dos 6 Padrões de Projeto de Ontologia
* Relatório com padrões completos, incompletos e ausentes

## PADRÕES DE PROJETO DE ONTOLOGIA (ODP)

O analisador semântico valida os seguintes 6 padrões:

| Padrão | Descrição |
|--------|-----------|
| **Subkind** | Verifica se subkinds especializam um kind e possuem genset com modificador disjoint |
| **Role** | Verifica se roles especializam um kind e participam de relação material ou mediação |
| **Phase** | Verifica se phases especializam um kind e possuem genset disjoint obrigatório |
| **Relator** | Verifica se o relator possui pelo menos 2 mediações apontando para roles |
| **Mode** | Verifica se o mode possui relações de characterization e externalDependence |
| **RoleMixin** | Verifica se o roleMixin possui pelo menos 2 roles associados e genset definido |

### Classificação dos Resultados

* `[OK]` - Padrão implementado corretamente (completo)
* `[ALERTA]` - Padrão com implementação incompleta
* `[INFO]` - Padrão não encontrado no código

## RESOLUÇÃO DE IMPORTS

Na análise semântica, o compilador resolve automaticamente as instruções `import`:

1. Lê o arquivo principal
2. Identifica declarações de import
3. Carrega recursivamente os arquivos importados
4. Mescla as definições (classes, relações, gensets, etc.) na AST principal
5. Executa a análise semântica na AST unificada

Isso permite analisar projetos com múltiplos arquivos interdependentes.

## DETALHES DA IMPLEMENTAÇÃO

### Analisador Léxico
* Implementado usando PLY (Python Lex-Yacc)
* Reconhece tokens através de expressões regulares
* Suporta comentários de linha única (`//`) e multilinha (`/* */`)
* Diferencia tipos de identificadores por convenção de nomenclatura

### Analisador Sintático
* Implementado usando PLY com gramática LALR
* Constrói árvore sintática abstrata (AST) durante o parsing
* Implementa recuperação de erros para continuar análise
* Gera tabela de síntese e relatório de erros

### Analisador Semântico
* Varre a AST gerada pelo analisador sintático
* Constrói índices para busca eficiente de classes, gensets e relações
* Valida os 6 padrões ODP com regras específicas para cada um
* Gera relatório detalhado com contagem de resultados

## PROJETOS DE TESTE INCLUÍDOS

| Projeto | Descrição | Arquivos |
|---------|-----------|----------|
| CarExample | Modelo de aluguel de carros | 2 |
| FoodAllergyExample | Modelo de alergia alimentar | 1 |
| Hospital_Model | Modelo de UBS com pacientes, funcionários e vacinação | 7 |
| Ontology Design Patterns | Exemplos dos 6 padrões ODP | 6 |
| Pizzaria_Model | Modelo completo de pizzaria | 8 |
| TDAHExample | Modelo de TDAH | 1 |
