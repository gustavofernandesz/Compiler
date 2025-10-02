import ply.lex as lex
import ply.yacc as yacc

#palavras reservadas do dicionário TONTO
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
}