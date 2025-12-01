import ply.yacc as yacc
import analisador_lexico

tokens = analisador_lexico.tokens

precedence = ()

class OntologyAST:
    def __init__(self):
        self.package_name = None
        self.classes = []
        self.datatypes = []
        self.enums = []
        self.gensets = []
        self.relations = []
        self.errors = []
    
    def add_error(self, line, message, suggestion=""):
        self.errors.append({
            'line': line,
            'message': message,
            'suggestion': suggestion
        })

ast = OntologyAST()

def p_program(p):
    '''program : package_declaration content_list
               | package_declaration'''
    if len(p) == 3:
        p[0] = ('program', p[1], p[2])
    else:
        p[0] = ('program', p[1], [])
    ast.package_name = p[1][1]

def p_package_declaration(p):
    '''package_declaration : PACKAGE CLASS_NAME
                          | PACKAGE RELATION_NAME'''
    p[0] = ('package', p[2])

def p_content_list(p):
    '''content_list : content_list content
                    | content'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

# def p_content(p):
#     '''content : class_declaration
#                | datatype_declaration
#                | enum_declaration
#                | genset_declaration
#                | relation_declaration'''
#     p[0] = p[1]

def p_content(p):
    '''content : class_declaration
               | datatype_declaration
               | enum_declaration
               | genset_declaration
               | relation_declaration
               | error content
    '''
    # Se len(p) for 2, é uma redução normal (class_declaration, datatype_declaration, etc.)
    if len(p) == 2:
        p[0] = p[1]

    # Se len(p) for 3 e p[1] for 'error', é a regra de recuperação: content -> error content
    elif len(p) == 3:
        # Pula o erro e continua com a próxima declaração (p[2])
        # A função p_error já registrou o erro.
        if p[2] is not None:
            print(f"[AVISO SINTÁTICO] Recuperação de erro. Continuando a análise a partir da próxima declaração.")
            p[0] = p[2]
        else:
            # Caso a próxima declaração também seja None (fim do arquivo ou erro grave)
            p[0] = None




def p_class_declaration(p):
    '''class_declaration : EST_CLASS CLASS_NAME LBRACE class_body RBRACE
                         | EST_CLASS CLASS_NAME LBRACE RBRACE
                         | EST_CLASS CLASS_NAME SPECIALIZES CLASS_NAME
                         | EST_CLASS CLASS_NAME'''
    if len(p) == 6:
        p[0] = ('class', p[1], p[2], p[4])
        attributes = [item for item in p[4] if item[0] == 'attribute']
        internal_rels = [item for item in p[4] if item[0] == 'internal_relation']
        ast.classes.append({
            'stereotype': p[1],
            'name': p[2],
            'attributes': attributes,
            'internal_relations': internal_rels,
            'specializes': None
        })
    elif len(p) == 5 and p[3] == 'specializes':
        p[0] = ('class_specializes', p[1], p[2], p[4])
        ast.classes.append({
            'stereotype': p[1],
            'name': p[2],
            'attributes': [],
            'internal_relations': [],
            'specializes': p[4]
        })
    elif len(p) == 5:
        p[0] = ('class', p[1], p[2], [])
        ast.classes.append({
            'stereotype': p[1],
            'name': p[2],
            'attributes': [],
            'internal_relations': [],
            'specializes': None
        })
    else:
        p[0] = ('class', p[1], p[2], [])
        ast.classes.append({
            'stereotype': p[1],
            'name': p[2],
            'attributes': [],
            'internal_relations': [],
            'specializes': None
        })

def p_class_body(p):
    '''class_body : class_body_item
                  | class_body class_body_item'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_class_body_item(p):
    '''class_body_item : attribute
                       | internal_relation'''
    p[0] = p[1]

def p_attribute(p):
    '''attribute : RELATION_NAME COLON type cardinality_opt
                 | RELATION_NAME COLON type cardinality_opt metadata_block
                 | ID COLON type cardinality_opt
                 | ID COLON type cardinality_opt metadata_block
                 | NATIVE_NUMBER COLON type cardinality_opt
                 | NATIVE_NUMBER COLON type cardinality_opt metadata_block
    '''
    if len(p) == 5:
        p[0] = ('attribute', p[1], p[3], p[4], None)
    else:
        p[0] = ('attribute', p[1], p[3], p[4], p[5])


def p_type(p):
    '''type : NATIVE_STRING
            | NATIVE_NUMBER
            | NATIVE_BOOLEAN
            | NATIVE_DATE
            | NATIVE_TIME
            | NATIVE_DATETIME
            | CLASS_NAME
            | RELATION_NAME
            | ID'''
    p[0] = ('type', p[1])

def p_metadata_block(p):
    '''metadata_block : LBRACE metadata_list RBRACE'''
    p[0] = ('metadata', p[2])

def p_metadata_list(p):
    '''metadata_list : metadata_item
                     | metadata_list metadata_item'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_metadata_item(p):
    '''metadata_item : META_CONST
                     | META_ORDERED
                     | META_DERIVED
                     | META_SUBSETS
                     | META_REDEFINES'''
    p[0] = p[1]

def p_internal_relation(p):
    '''internal_relation : ARROBA EST_REL cardinality relation_symbol cardinality CLASS_NAME
                         | EST_REL cardinality relation_symbol cardinality CLASS_NAME'''
    if len(p) == 7:
        p[0] = ('internal_relation', p[2], p[3], p[4], p[5], p[6])
    else:
        p[0] = ('internal_relation', p[1], p[2], p[3], p[4], p[5])

def p_datatype_declaration(p):
    '''datatype_declaration : DATATYPE CLASS_NAME LBRACE attribute_list RBRACE
                            | DATATYPE CLASS_NAME LBRACE RBRACE'''
    if len(p) == 6:
        p[0] = ('datatype', p[2], p[4])
        ast.datatypes.append({
            'name': p[2],
            'attributes': p[4]
        })
    else:
        p[0] = ('datatype', p[2], [])
        ast.datatypes.append({
            'name': p[2],
            'attributes': []
        })

def p_attribute_list(p):
    '''attribute_list : attribute
                      | attribute_list attribute'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_enum_declaration(p):
    '''enum_declaration : ENUM CLASS_NAME LBRACE instance_list RBRACE
                        | ENUM CLASS_NAME LBRACE RBRACE'''
    if len(p) == 6:
        p[0] = ('enum', p[2], p[4])
        ast.enums.append({
            'name': p[2],
            'instances': p[4]
        })
    else:
        p[0] = ('enum', p[2], [])
        ast.enums.append({
            'name': p[2],
            'instances': []
        })

def p_instance_list(p):
    '''instance_list : CLASS_NAME
                     | instance_list CLASS_NAME'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_genset_declaration(p):
    '''genset_declaration : modifiers GENSET CLASS_NAME WHERE class_list SPECIALIZES CLASS_NAME
                          | GENSET CLASS_NAME WHERE class_list SPECIALIZES CLASS_NAME
                          | GENSET CLASS_NAME LBRACE GENERAL CLASS_NAME SPECIFICS class_list RBRACE
                          | modifiers GENSET CLASS_NAME LBRACE GENERAL CLASS_NAME SPECIFICS class_list RBRACE'''
    if len(p) == 8 and p[4] == 'where':
        p[0] = ('genset', p[3], p[1], p[7], p[5])
        ast.gensets.append({
            'name': p[3],
            'modifiers': p[1],
            'general': p[7],
            'specifics': p[5]
        })
    elif len(p) == 7 and p[3] == 'where':
        p[0] = ('genset', p[2], None, p[6], p[4])
        ast.gensets.append({
            'name': p[2],
            'modifiers': None,
            'general': p[6],
            'specifics': p[4]
        })
    elif len(p) == 9 and p[4] == '{':
        p[0] = ('genset_block', p[3], p[1], p[6], p[8])
        ast.gensets.append({
            'name': p[3],
            'modifiers': p[1],
            'general': p[6],
            'specifics': p[8]
        })
    else:
        p[0] = ('genset_block', p[2], None, p[5], p[7])
        ast.gensets.append({
            'name': p[2],
            'modifiers': None,
            'general': p[5],
            'specifics': p[7]
        })

def p_modifiers(p):
    '''modifiers : DISJOINT COMPLETE
                 | COMPLETE DISJOINT
                 | DISJOINT
                 | COMPLETE'''
    if len(p) == 3:
        p[0] = [p[1], p[2]]
    else:
        p[0] = [p[1]]

def p_class_list(p):
    '''class_list : CLASS_NAME
                  | class_list COMMA CLASS_NAME'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_relation_declaration(p):
    '''relation_declaration : ARROBA EST_REL RELATION CLASS_NAME cardinality relation_symbol cardinality CLASS_NAME
                            | RELATION CLASS_NAME cardinality relation_symbol cardinality CLASS_NAME
                            | RELATION CLASS_NAME cardinality relation_symbol RELATION_NAME relation_symbol cardinality CLASS_NAME
                            | CLASS_NAME cardinality relation_symbol RELATION_NAME relation_symbol cardinality CLASS_NAME'''
    if len(p) == 9 and p[1] == '@':
        p[0] = ('relation', p[2], p[4], p[5], p[6], p[7], p[8])
        ast.relations.append({
            'stereotype': p[2],
            'domain': p[4],
            'domain_card': p[5],
            'symbol': p[6],
            'range_card': p[7],
            'range': p[8],
            'name': None
        })
    elif len(p) == 8 and p[3] == '[':
        p[0] = ('relation', None, p[2], p[3], p[4], p[5], p[6])
        ast.relations.append({
            'stereotype': None,
            'domain': p[2],
            'domain_card': p[3],
            'symbol': p[4],
            'range_card': p[5],
            'range': p[6],
            'name': None
        })
    elif len(p) == 9:
        p[0] = ('relation_named', None, p[2], p[3], p[4], p[5], p[6], p[7], p[8])
        ast.relations.append({
            'stereotype': None,
            'domain': p[2],
            'domain_card': p[3],
            'symbol': p[4],
            'name': p[5],
            'symbol2': p[6],
            'range_card': p[7],
            'range': p[8]
        })
    else:
        p[0] = ('relation_named', None, p[1], p[2], p[3], p[4], p[5], p[6], p[7])
        ast.relations.append({
            'stereotype': None,
            'domain': p[1],
            'domain_card': p[2],
            'symbol': p[3],
            'name': p[4],
            'symbol2': p[5],
            'range_card': p[6],
            'range': p[7]
        })

def p_cardinality(p):
    '''cardinality : LBRACKET NUMBER DOT DOT ASTERISCO RBRACKET
                   | LBRACKET NUMBER RBRACKET
                   | LBRACKET NUMBER DOT DOT NUMBER RBRACKET
                   | LBRACKET ASTERISCO RBRACKET'''
    if len(p) == 7:
        p[0] = ('cardinality', p[2], '*')
    elif len(p) == 4:
        p[0] = ('cardinality', p[2], p[2])
    elif len(p) == 7 and isinstance(p[5], int):
        p[0] = ('cardinality', p[2], p[5])
    else:
        p[0] = ('cardinality', '*', '*')

def p_relation_symbol(p):
    '''relation_symbol : HYPHEN HYPHEN
                       | CONTEM
                       | CONTIDO'''
    if len(p) == 3:
        p[0] = '--'
    else:
        p[0] = p[1]

def p_cardinality_opt(p):
    '''cardinality_opt : cardinality
                       | empty'''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    p[0] = None


def p_error(p):
    if p:
        error_msg = f"Token inesperado '{p.value}' (Tipo: {p.type})"
        suggestion = ""
        
        if p.type == 'CLASS_NAME':
            suggestion = "Verifique se há uma palavra reservada ou estereótipo faltando antes do nome da classe."
        elif p.type == 'LBRACE':
            suggestion = "Verifique se a declaração anterior está completa."
        elif p.type == 'RBRACE':
            suggestion = "Pode estar faltando um atributo, relação ou vírgula."
        
        ast.add_error(p.lineno, error_msg, suggestion)
        print(f"[ERRO] Linha {p.lineno}: {error_msg}")
        if suggestion:
            print(f"  → Sugestão: {suggestion}")
    else:
        ast.add_error(-1, "Fim inesperado do arquivo", "Verifique se todas as chaves e parênteses foram fechados.")
        print("[ERRO] Fim inesperado do arquivo")
        print("  → Sugestão: Verifique se todas as chaves e parênteses foram fechados.")

def exibir_analise_sintatica():
    print("\n" + "="*80)
    print("ANÁLISE SINTÁTICA")
    print("="*80)
    
    gerar_tabela_sintese()
    gerar_relatorio_erros()

def gerar_tabela_sintese():
    print("\n" + "="*80)
    print("TABELA DE SÍNTESE - ANÁLISE SINTÁTICA")
    print("="*80)
    
    print(f"\nPACOTE: {ast.package_name if ast.package_name else 'Nenhum'}")
    
    print(f"\nCLASSES: {len(ast.classes)}")
    if ast.classes:
        for cls in ast.classes:
            specializes_info = f" -> especializa {cls['specializes']}" if cls['specializes'] else ""
            attrs_count = len(cls['attributes'])
            rels_count = len(cls['internal_relations'])
            print(f"  {cls['name']} ({cls['stereotype']}){specializes_info}")
            print(f"    {attrs_count} atributo(s)")
            if attrs_count > 0:
                for attr in cls['attributes']:
                    attr_name = attr[1]
                    attr_type = attr[2][1] if attr[2] else "?"
                    metadata = f" {attr[3]}" if attr[3] else ""
                    print(f"      {attr_name}: {attr_type}{metadata}")
            print(f"    {rels_count} relação(ões) interna(s)")
            if rels_count > 0:
                for rel in cls['internal_relations']:
                    stereotype = f"@{rel[1]}" if rel[1] else ""
                    target = rel[5] if len(rel) > 5 else "?"
                    print(f"      {stereotype} para {target}")
    
    print(f"\nTIPOS DE DADOS CUSTOMIZADOS: {len(ast.datatypes)}")
    if ast.datatypes:
        for dt in ast.datatypes:
            attrs_count = len(dt['attributes'])
            print(f"  {dt['name']} ({attrs_count} atributo(s))")
            for attr in dt['attributes']:
                attr_name = attr[1]
                attr_type = attr[2][1] if attr[2] else "?"
                print(f"    {attr_name}: {attr_type}")
    
    print(f"\nENUMERAÇÕES: {len(ast.enums)}")
    if ast.enums:
        for enum in ast.enums:
            instances_count = len(enum['instances'])
            print(f"  {enum['name']} ({instances_count} instância(s))")
            if instances_count > 0:
                instances_str = ", ".join(enum['instances'])
                print(f"    {instances_str}")
    
    print(f"\nRELAÇÕES EXTERNAS: {len(ast.relations)}")
    if ast.relations:
        for rel in ast.relations:
            stereotype = f"@{rel.get('stereotype')} " if rel.get('stereotype') else ""
            domain = rel.get('domain', '?')
            range_cls = rel.get('range', '?')
            name = rel.get('name', '')
            name_str = f" -- {name} -- " if name else " -- "
            
            domain_card = rel.get('domain_card', '')
            if isinstance(domain_card, tuple):
                card_str = f"[{domain_card[1]}..{domain_card[2]}]"
            else:
                card_str = str(domain_card)
            
            range_card = rel.get('range_card', '')
            if isinstance(range_card, tuple):
                range_card_str = f"[{range_card[1]}..{range_card[2]}]"
            else:
                range_card_str = str(range_card)
            
            print(f"  {stereotype}{domain} {card_str}{name_str}{range_card_str} {range_cls}")
    
    print(f"\nCONJUNTOS DE GENERALIZAÇÃO: {len(ast.gensets)}")
    if ast.gensets:
        for genset in ast.gensets:
            modifiers_str = ""
            if genset['modifiers']:
                modifiers_str = f" ({', '.join(genset['modifiers'])})"
            specifics_str = ", ".join(genset['specifics'])
            print(f"  {genset['name']}{modifiers_str}")
            print(f"    Geral: {genset['general']}")
            print(f"    Específicas: {specifics_str}")
    
    print("\n" + "="*80)

def gerar_relatorio_erros():
    print("\n" + "="*80)
    print("RELATÓRIO DE ERROS")
    print("="*80)
    
    if not ast.errors:
        print("\nNenhum erro sintático encontrado.")
        print("A análise foi concluída com sucesso.")
    else:
        print(f"\n{len(ast.errors)} erro(s) encontrado(s):\n")
        for i, error in enumerate(ast.errors, 1):
            line = error['line']
            msg = error['message']
            suggestion = error['suggestion']
            
            line_str = f"Linha {line}" if line > 0 else "Final do arquivo"
            print(f"{i}. [{line_str}] {msg}")
            if suggestion:
                print(f"   Sugestão: {suggestion}")
            print()
    
    print("="*80)

def reset_ast():
    global ast
    ast = OntologyAST()

def build(**kwargs):
    return yacc.yacc(**kwargs)

def parse(code, **kwargs):
    reset_ast()
    lexer = analisador_lexico.build()
    parser = build(**kwargs)
    result = parser.parse(code, lexer=lexer)
    return result, ast
