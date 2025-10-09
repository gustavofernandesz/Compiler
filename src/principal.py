import ply.lex as lex
import ply.yacc as yacc

#palavras reservadas do dicionário TONTO
reserved = {
    # Palavras reservadas principais 
    'ontology': 'ONTOLOGY',
    'class': 'CLASS',
    'subclassOf': 'SUBCLASSOF',
    'individual': 'INDIVIDUAL',
    'property': 'PROPERTY',
    'domain': 'DOMAIN',
    'range': 'RANGE',
    'datatype': 'DATATYPE',
    'annotation': 'ANNOTATION',
    'equivalentTo': 'EQUIVALENTTO',
    'disjointWith': 'DISJOINTWITH',
    'sameAs': 'SAMEAS',
    'differentFrom': 'DIFFERENTFROM',
    'import': 'IMPORT',

    # Estereótipos de classe 
    'kind': 'KIND',
    'subkind': 'SUBKIND',
    'collective': 'COLLECTIVE',
    'quantity': 'QUANTITY',
    'quality': 'QUALITY',
    'mode': 'MODE',
    'intrisicMode': 'INTRISICMODE',
    'extrinsicMode': 'EXTRINSICMODE',
    'role': 'ROLE',
    'phase': 'PHASE',
    'historicalRole': 'HISTORICALROLE',
    'event': 'EVENT',
    'situation': 'SITUATION',
    'process': 'PROCESS',
    'category': 'CATEGORY',
    'mixin': 'MIXIN',
    'phaseMixin': 'PHASEMIXIN',
    'roleMixin': 'ROLEMIXIN',
    'historicalRoleMixin': 'HISTORICALROLEMIXIN',

    # Estereótipos de relação
    'material': 'MATERIAL',
    'derivation': 'DERIVATION',
    'comparative': 'COMPARATIVE',
    'mediation': 'MEDIATION',
    'characterization': 'CHARACTERIZATION',
    'externalDependence': 'EXTERNALDEPENDENCE',
    'componentOf': 'COMPONENTOF',
    'memberOf': 'MEMBEROF',
    'subCollectionOf': 'SUBCOLLECTIONOF',
    'subQualityOf': 'SUBQUALITYOF',
    'instantiation': 'INSTANTIATION',
    'termination': 'TERMINATION',
    'participational': 'PARTICIPATIONAL',
    'participation': 'PARTICIPATION',
    'historicalDependence': 'HISTORICALDEPENDENCE',
    'creation': 'CREATION',
    'manifestation': 'MANIFESTATION',
    'bringsAbout': 'BRINGSABOUT',
    'triggers': 'TRIGGERS',
    'composition': 'COMPOSITION',
    'aggregation': 'AGGREGATION',
    'inherence': 'INHERENCE',
    'value': 'VALUE',
    'formal': 'FORMAL',
    'constitution': 'CONSTITUTION',
    
    # Tipos de dados 
    'number': 'TYPE_NUMBER',
    'string': 'TYPE_STRING',
    'boolean': 'TYPE_BOOLEAN',
    'date': 'TYPE_DATE',
    'time': 'TYPE_TIME',
    'datetime': 'TYPE_DATETIME',
}

tokens=[
    'ID',             
    'STRING',         
    'NUMBER',         
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'COMMA',
    'MAIORIGUAL', 'MENORIGUAL',
    'MAIOR', 'MENOR',
    'CONTEM', 'CONTIDO',
    'ASTERISCO',
    'ARROBA',
    'COLON'
]+ list(set(reserved.values()))


t_LPAREN = r'\('      # abre parêntese
t_RPAREN = r'\)'      # fecha parêntese
t_LBRACE = r'\{'      # abre chave
t_RBRACE = r'\}'      # fecha chave
t_COMMA = r'\,'       # vírgula
t_ignore = ' \n\t'      # ignora espaços e tabulações
t_MAIORIGUAL = r'>='  # operador >=
t_MENORIGUAL = r'<='  # operador <=
t_MAIOR = r'>'        # operador >
t_MENOR = r'<'        # operador <
t_CONTEM = r'<>--'
t_CONTIDO = r'--<>'
t_ASTERISCO = r'\*'
t_ARROBA = r'@'
t_COLON = r':'

def t_COMMENT_SINGLELINE(t):
    r'//[^\n]*'
    pass

def t_COMMENT_MULTILINE(t):
    r'/\*([^*]|\*+[^*/])*\*+/'
    t.lexer.lineno += t.value.count('\n')
    pass

def t_STRING(t):
    r'(\"([^\\\"]|\\.)*\"|\'([^\\\']|\\.)*\')'
    t.value = t.value[1:-1]
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value.lower(), 'ID') 
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print(f"[LEX ERROR] Linha {t.lexer.lineno}: símbolo inesperado {repr(t.value[0])}")
    t.lexer.skip(1)

def build(**kwargs):
    return lex.lex(**kwargs)

def lex_table(input_text, lexer=None):
    if lexer is None:
        lexer = build()
    lexer.input(input_text)
    table = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        table.append((tok.lineno, tok.type, tok.value))
    return table

saida = [] # tabela de simbolos