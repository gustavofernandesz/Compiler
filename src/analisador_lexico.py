import ply.lex as lex
import ply.yacc as yacc
import re
from collections import Counter

# Palavras reservadas estruturais 
reserved = {
    # Palavras reservadas principais 
    'ontology': 'ONTOLOGY',
    'class': 'CLASS',
    'subclassof': 'SUBCLASSOF',
    'individual': 'INDIVIDUAL',
    'property': 'PROPERTY',
    'domain': 'DOMAIN',
    'range': 'RANGE',
    'datatype': 'DATATYPE',
    'annotation': 'ANNOTATION',
    'equivalentto': 'EQUIVALENTTO',
    'disjointwith': 'DISJOINTWITH',
    'sameas': 'SAMEAS',
    'differentfrom': 'DIFFERENTFROM',
    'import': 'IMPORT',
    'genset': 'GENSET',
    'disjoint': 'DISJOINT',
    'complete': 'COMPLETE',
    'general': 'GENERAL',
    'specifics': 'SPECIFICS',
    'where': 'WHERE',
    'package': 'PACKAGE',
    'enum': 'ENUM',         
    'relation': 'RELATION', 
    'specializes': 'SPECIALIZES',
    
    # Tipos de dados nativos
    'number': 'NATIVE_NUMBER',
    'string': 'NATIVE_STRING',
    'boolean': 'NATIVE_BOOLEAN',
    'date': 'NATIVE_DATE',
    'time': 'NATIVE_TIME',
    'datetime': 'NATIVE_DATETIME',
    
    # Metadados
    'const': 'META_CONST',
    'ordered': 'META_ORDERED',
    'derived': 'META_DERIVED',
    'subsets': 'META_SUBSETS',
    'redefines': 'META_REDEFINES',
}

# Estereótipos de classe (case-sensitive)
stereotypes_class = {
    'kind', 'subkind', 'collective', 'quantity', 'quality', 'mode',
    'intrisicMode', 'extrinsicMode', 'role', 'phase', 'historicalRole',
    'event', 'situation', 'process', 'category', 'mixin', 'phaseMixin',
    'roleMixin', 'historicalRoleMixin', 'relator'
}

# Estereótipos de relação
stereotypes_rel = {
    'material', 'derivation', 'comparative', 'mediation', 'characterization',
    'externalDependence', 'componentOf', 'memberOf', 'subCollectionOf', 
    'subQualityOf', 'instantiation', 'termination', 'participational', 
    'participation', 'historicalDependence', 'creation', 'manifestation', 
    'bringsAbout', 'triggers', 'composition', 'aggregation', 'inherence', 
    'value', 'formal', 'constitution'
}


# Lista de tokens
tokens = [
    # Símbolos
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'LBRACKET', 'RBRACKET',
    'COMMA',
    'MAIORIGUAL', 'MENORIGUAL',
    'MAIOR', 'MENOR',
    'CONTEM', 'CONTIDO',
    'ASTERISCO',
    'ARROBA',
    'COLON',
    'DOT',           
    'HYPHEN',
    
    # Literais
    'STRING',         
    'NUMBER',
    'BOOLEAN_LITERAL',
    
    # Identificadores específicos
    'ID',
    'CLASS_NAME',
    'RELATION_NAME',
    'INSTANCE',
    'NEW_DATATYPE',
    
    # Estereótipos
    'EST_CLASS',
    'EST_REL',
] + list(set(reserved.values()))


t_LPAREN = r'\('      # abre parêntese
t_RPAREN = r'\)'      # fecha parêntese
t_LBRACE = r'\{'      # abre chave
t_RBRACE = r'\}'      # fecha chave
t_COMMA = r'\,'       # vírgula
t_ignore = ' \t'      # ignora tabulações
t_MAIORIGUAL = r'>='  # operador >=
t_MENORIGUAL = r'<='  # operador <=
t_MAIOR = r'>'        # operador >
t_MENOR = r'<'        # operador <
t_CONTEM = r'<>--'
t_CONTIDO = r'--<>'
t_LBRACKET = r'\['   # abre colchete
t_RBRACKET = r'\]'   # fecha colchete
t_DOT = r'\.'        # ponto
t_HYPHEN = r'-'      # hífen
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
    r'[A-Za-z][A-Za-z0-9_]*'
    lexeme = t.value
    low = lexeme.lower()
    
    if low in reserved:
        t.type = reserved[low]
        return t
    
    if lexeme in stereotypes_class:
        t.type = 'EST_CLASS'
        return t
    
    if lexeme in stereotypes_rel:
        t.type = 'EST_REL'
        return t
    
    if lexeme in ('true', 'false'):
        t.type = 'BOOLEAN_LITERAL'
        t.value = (lexeme == 'true')
        return t
    
    if lexeme.endswith('DataType') and re.fullmatch(r'[A-Za-z]+DataType', lexeme):
        t.type = 'NEW_DATATYPE'
        return t
    
    if re.fullmatch(r'[A-Z][A-Za-z0-9_]*', lexeme):
        t.type = 'CLASS_NAME'
        return t
    
    if re.fullmatch(r'[a-z][A-Za-z_0-9]*\d+', lexeme):
        t.type = 'INSTANCE'
        return t
    
    if re.fullmatch(r'[a-z][A-Za-z0-9_]*', lexeme):
        t.type = 'RELATION_NAME'
        return t
    
    t.type = 'ID'
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
    counts = Counter()
    while True:
        tok = lexer.token()
        if not tok:
            break
        table.append((tok.lineno, tok.type, tok.value))
        counts[tok.type] += 1
    return table, counts

def exibir_analise_lexica(tabela, contagem):
    print("\n" + "="*80)
    print("ANÁLISE LÉXICA")
    print("="*80)
    
    print(f"\n{'Linha':<8} {'Token':<25} {'Valor'}")
    print("-" * 60)
    for linha, tipo, valor in tabela:
        print(f"{linha:<8} {tipo:<25} {valor}")
    
    print(f"\nTotal de tokens: {len(tabela)}")
    print("\nContagem por tipo:")
    print("-" * 40)
    for tipo, qtd in sorted(contagem.items()):
        print(f"  {tipo:<25}: {qtd}")

saida = [] # tabela de simbolos