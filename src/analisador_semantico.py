# ============================================
# ANALISADOR SEMÂNTICO PARA TONTO (UFERSA)
# Compatível com seu analisador_sintatico.py
# ============================================

from collections import defaultdict


# --------------------------------------------
# Função principal
# --------------------------------------------
def analisar_semantica(ast):
    print("\n" + "=" * 80)
    print("ANÁLISE SEMÂNTICA (Padrões ODP)")
    print("=" * 80)

    resultados = []

    resultados += validar_subkind(ast)
    resultados += validar_role(ast)
    resultados += validar_phase(ast)
    resultados += validar_relator(ast)
    resultados += validar_mode(ast)
    resultados += validar_rolemixin(ast)

    exibir_relatorio(resultados)


# --------------------------------------------
# SUBKIND PATTERN
# --------------------------------------------
def validar_subkind(ast):
    resultados = []

    for cls in ast.classes:
        if cls['stereotype'] != 'subkind':
            continue

        filho = cls['name']
        pai = cls['specializes']

        if pai is None:
            resultados.append(("Subkind incompleto", f"{filho} não possui 'specializes'."))
            continue

        # Encontrar classe pai no AST
        pai_tipo = None
        for c in ast.classes:
            if c['name'] == pai:
                pai_tipo = c['stereotype']
                break

        if pai_tipo != 'kind':
            resultados.append(("Subkind inválido",
                               f"{filho} deveria especializar um kind, mas especializa '{pai_tipo}'."))
        else:
            resultados.append(("Subkind completo", f"{filho} → {pai}"))

    if not any(c['stereotype'] == 'subkind' for c in ast.classes):
        resultados.append(("Subkind ausente", "Nenhum Subkind Pattern encontrado."))

    return resultados


# --------------------------------------------
# ROLE PATTERN
# --------------------------------------------
def validar_role(ast):
    resultados = []

    # Mapear todas as relações externas
    relacoes = ast.relations

    for cls in ast.classes:
        if cls['stereotype'] != 'role':
            continue

        nome = cls['name']
        pai = cls['specializes']

        # 1) role deve especializar outro role OU kind
        pai_tipo = None
        for c in ast.classes:
            if c['name'] == pai:
                pai_tipo = c['stereotype']
                break

        if pai_tipo not in ('role', 'kind'):
            resultados.append(("Role inválido",
                               f"{nome} especializa '{pai_tipo}', mas deveria especializar 'kind' ou 'role'."))
            continue

        # 2) role deve estar envolvido em alguma relação externa
        participa = False
        for rel in relacoes:
            if rel.get('domain') == nome or rel.get('range') == nome:
                participa = True
                break

        if not participa:
            resultados.append(("Role incompleto",
                               f"{nome} não participa de nenhuma relação material/mediada."))
        else:
            resultados.append(("Role completo", f"{nome} participa de relações e é válido."))

    if not any(c['stereotype'] == 'role' for c in ast.classes):
        resultados.append(("Role ausente", "Nenhum Role Pattern encontrado."))

    return resultados


# --------------------------------------------
# PHASE PATTERN
# --------------------------------------------
def validar_phase(ast):
    resultados = []

    fases_por_pai = defaultdict(list)

    for cls in ast.classes:
        if cls['stereotype'] == 'phase':
            fases_por_pai[cls['specializes']].append(cls['name'])

    if not fases_por_pai:
        resultados.append(("Phase ausente", "Nenhum Phase Pattern encontrado."))
        return resultados

    for pai, fases in fases_por_pai.items():
        if len(fases) < 2:
            resultados.append(("Phase incompleto",
                               f"O kind '{pai}' tem apenas uma fase: {fases[0]}."))
        else:
            resultados.append(("Phase completo",
                               f"{pai} é particionado por fases: {', '.join(fases)}"))

    return resultados


# --------------------------------------------
# RELATOR PATTERN
# --------------------------------------------
def validar_relator(ast):
    resultados = []

    # Relator é um EST_CLASS com nome 'relator'
    relators = [c for c in ast.classes if c['stereotype'] == 'relator']

    if not relators:
        resultados.append(("Relator ausente", "Nenhum Relator Pattern encontrado."))
        return resultados

    for rel in relators:
        nome = rel['name']

        # Mediações internas: internal_relation onde estereótipo = 'mediation'
        mediacoes = [
            i for i in rel['internal_relations']
            if i[1] == 'mediation'
        ]

        if len(mediacoes) < 2:
            resultados.append(("Relator incompleto",
                               f"{nome} tem apenas {len(mediacoes)} mediação(ões)."))
        else:
            resultados.append(("Relator completo",
                               f"{nome} possui {len(mediacoes)} mediações."))

    return resultados


# --------------------------------------------
# MODE PATTERN
# --------------------------------------------
def validar_mode(ast):
    if any(c['stereotype'] == 'mode' for c in ast.classes):
        return [("Mode presente", "Há classes do tipo mode (não validadas ainda).")]
    else:
        return [("Mode ausente", "Nenhum Mode Pattern encontrado.")]

    # --------------------------------------------


# ROLEMIXIN PATTERN
# --------------------------------------------
def validar_rolemixin(ast):
    if any(c['stereotype'] == 'roleMixin' for c in ast.classes):
        return [("RoleMixin presente", "Há RoleMixins declarados.")]
    else:
        return [("RoleMixin ausente", "Nenhum RoleMixin Pattern encontrado.")]


# --------------------------------------------
# RELATÓRIO FINAL
# --------------------------------------------
def exibir_relatorio(resultados):
    print("\n" + "=" * 80)
    print("RESULTADO FINAL DA ANÁLISE SEMÂNTICA")
    print("=" * 80)

    for status, msg in resultados:
        if "completo" in status.lower():
            print(f"[OK] {status}: {msg}")
        elif "incompleto" in status.lower():
            print(f"[ALERTA] {status}: {msg}")
        else:
            print(f"[INFO] {status}: {msg}")

    print("=" * 80)
