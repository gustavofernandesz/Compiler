import ply.lex as lex
import ply.yacc as yacc
import analisador_lexico
import os

tokens = analisador_lexico.tokens

def p_program(p):
    p[0] = ('programa', p[1])

def p_package_declaration(p):
    p[0] = ('package_declaration', p[2])

def p_content(p):
    if len(p) == 3:
        p[0] = p[1] + [p[2]] 
    else:
        p[0] = [p[1]]

def p_class_declaration(p):
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Erro de sintaxe no token '{p.value}' (Tipo: {p.type}) na linha {p.lineno}")
    else:
        print("Erro de sintaxe: Fim inesperado do arquivo")

