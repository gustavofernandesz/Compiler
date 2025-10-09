import ply.lex as lex
import ply.yacc as yacc

#palavras reservadas do dicionário TONTO
class_stereotypes = {
    'event', 'situation', 'process', 'category', 'mixin',
    'phaseMixin', 'roleMixin', 'historicalRoleMixin','kind','collective',
    'quantity', 'quality', 'mode', 'intrisicMode', 'extrinsicMode',
    'subkind', 'phase', 'role', 'historicalRole',
}

stereotype_relation = {
    'material', 'derivation', 'comparative', 'mediation', 'characterization',
    'externalDependence', 'componentOf', 'memberOf', 'subCollectionOf', 'subQualityOf',
    'instantiation', 'termination', 'participational', 'participation', 'historicalDependence',
    'creation', 'manifestation', 'bringsAbout', 'triggers', 'composition',
    'aggregation', 'inherence', 'value', 'formal', 'constitution',
}

reservadas={
    'ontology',
    'class',
    'subclassOf',
    'individual',
    'property',
    'domain',
    'range',
    'datatype',
    'annotation',
    'equivalentTo',
    'disjointWith',
    'sameAs',
    'differentFrom',
    'import'
    'kind'
    'role'
    'phase'
}
type_data=[
    'number',
    'string',
    'boolean',
    'date',
    'time',
    'datetime'
]

tokens=[

]+ list(set(reservadas.values()))


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


saida = [] # tabela de simbolos