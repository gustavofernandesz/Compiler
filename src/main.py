import os
import sys

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
sys.path.append(diretorio_atual)

import analisador_lexico
import analisador_sintatico
import analisador_semantico

LARGURA = 80

def linha(char="="):
    return char * LARGURA

def cabecalho(titulo):
    print("\n" + linha())
    print(titulo.center(LARGURA))
    print(linha())

def subcabecalho(titulo):
    print("\n" + linha("-"))
    print(titulo)
    print(linha("-"))

def listar_testes():
    projetos = {}
    caminho_testes = os.path.join(os.path.dirname(diretorio_atual), 'Compiladores_UFERSA-main')
    
    if not os.path.exists(caminho_testes):
        return None

    for nome_pasta in sorted(os.listdir(caminho_testes)):
        caminho_pasta = os.path.join(caminho_testes, nome_pasta)
        if os.path.isdir(caminho_pasta):
            arquivos_tonto = []
            for root, dirs, files in os.walk(caminho_pasta):
                for file in sorted(files):
                    if file.endswith(".tonto"):
                        caminho_completo = os.path.join(root, file)
                        arquivos_tonto.append(caminho_completo)
            
            if arquivos_tonto:
                projetos[nome_pasta] = arquivos_tonto
    
    return projetos

def selecionar_arquivo():
    projetos = listar_testes()
    
    if not projetos:
        print("\n  [AVISO] Pasta de testes não encontrada.")
        print("  Usando arquivo de exemplo padrão.")
        return os.path.join(diretorio_atual, 'example.tonto')

    cabecalho("SELEÇÃO DE PROJETO DE TESTE")
    
    lista_projetos = list(projetos.keys())
    for i, proj in enumerate(lista_projetos, 1):
        qtd = len(projetos[proj])
        print(f"  [{i}] {proj} ({qtd} arquivo(s))")
    
    print(f"\n  [{len(lista_projetos)+1}] Arquivo local (example.tonto)")
    print("  [0] Voltar")
    
    escolha_proj = input("\n  Escolha o PROJETO: ").strip()
    
    if escolha_proj == "0":
        return None
    
    if escolha_proj == str(len(lista_projetos)+1):
        return os.path.join(diretorio_atual, 'example.tonto')
    
    if not escolha_proj.isdigit():
        print("\n  [ERRO] Opção inválida!")
        return None
        
    idx_proj = int(escolha_proj) - 1
    if 0 <= idx_proj < len(lista_projetos):
        nome_projeto = lista_projetos[idx_proj]
        arquivos = projetos[nome_projeto]
        
        subcabecalho(f"ARQUIVOS EM: {nome_projeto}")
        for i, arq in enumerate(arquivos, 1):
            nome_arq = os.path.basename(arq)
            pasta_pai = os.path.basename(os.path.dirname(arq))
            print(f"  [{i}] {pasta_pai}/{nome_arq}")
        
        print("\n  [0] Voltar")
        escolha_arq = input("\n  Escolha o ARQUIVO: ").strip()
        
        if escolha_arq == "0":
            return None
            
        if escolha_arq.isdigit():
            idx_arq = int(escolha_arq) - 1
            if 0 <= idx_arq < len(arquivos):
                return arquivos[idx_arq]
    
    print("\n  [ERRO] Seleção inválida.")
    return None

def processar_imports_recursivamente(caminho_arquivo, ast_principal, arquivos_processados=None):
    if arquivos_processados is None:
        arquivos_processados = set()
    
    arquivos_processados.add(os.path.abspath(caminho_arquivo))
    
    if not hasattr(ast_principal, 'imports') or not ast_principal.imports:
        return

    diretorio_base = os.path.dirname(caminho_arquivo)
    
    for item_import in ast_principal.imports:
        if isinstance(item_import, tuple) and len(item_import) >= 2:
            nome_arquivo_import = item_import[1]
        else:
            nome_arquivo_import = str(item_import)
        
        caminho_import = os.path.join(diretorio_base, f"{nome_arquivo_import}.tonto")
        caminho_import_abs = os.path.abspath(caminho_import)
        
        if caminho_import_abs in arquivos_processados:
            continue
            
        if os.path.exists(caminho_import):
            print(f"     Importando: {nome_arquivo_import}.tonto")
            
            with open(caminho_import, 'r') as f:
                codigo_import = f.read()
            
            _, ast_importada = analisador_sintatico.parse(codigo_import)
            
            processar_imports_recursivamente(caminho_import, ast_importada, arquivos_processados)
            
            ast_principal.classes.extend(ast_importada.classes)
            ast_principal.relations.extend(ast_importada.relations)
            ast_principal.gensets.extend(ast_importada.gensets)
            ast_principal.datatypes.extend(ast_importada.datatypes)
            ast_principal.enums.extend(ast_importada.enums)
            
        else:
            print(f"    [AVISO] Arquivo não encontrado: {nome_arquivo_import}.tonto")

def executar_analise_lexica(codigo):
    cabecalho("ANÁLISE LÉXICA")
    lexer = analisador_lexico.build()
    tabela, contagem = analisador_lexico.lex_table(codigo, lexer)
    
    subcabecalho("TABELA DE TOKENS")
    print(f"\n  {'LINHA':<8} {'TOKEN':<25} {'VALOR'}")
    print("  " + "-" * 50)
    for linha_num, tipo, valor in tabela:
        print(f"  {linha_num:<8} {tipo:<25} {valor}")
    
    subcabecalho("RESUMO")
    print(f"\n  Total de tokens: {len(tabela)}")
    print()
    print(f"  {'TIPO':<25} {'QTD':>5}")
    print("  " + "-" * 32)
    for tipo, qtd in sorted(contagem.items()):
        print(f"  {tipo:<25} {qtd:>5}")
    
    print("\n" + linha())
    print("Análise léxica concluída.".center(LARGURA))
    print(linha())

def executar_analise_sintatica(codigo):
    resultado, ast = analisador_sintatico.parse(codigo)
    analisador_sintatico.gerar_tabela_sintese()
    analisador_sintatico.gerar_relatorio_erros()
    return ast

def executar_analise_semantica(codigo, caminho_arquivo):
    cabecalho("ANÁLISE SEMÂNTICA")
    
    nome_arquivo = os.path.basename(caminho_arquivo)
    print(f"  Arquivo principal: {nome_arquivo}")
    
    _, ast_completa = analisador_sintatico.parse(codigo)
    
    if hasattr(ast_completa, 'imports') and ast_completa.imports:
        print("\n  Resolvendo imports...")
        processar_imports_recursivamente(caminho_arquivo, ast_completa)
        print("  Imports processados.\n")
    
    analisador_semantico.analisar(ast_completa)

def menu_tipo_analise(caminho_arquivo):
    nome_arq = os.path.basename(caminho_arquivo)
    pasta_pai = os.path.basename(os.path.dirname(caminho_arquivo))
    
    while True:
        subcabecalho(f"ARQUIVO: {pasta_pai}/{nome_arq}")
        print("\n  [1] Análise Léxica")
        print("  [2] Análise Sintática")
        print("  [3] Análise Semântica")
        print("\n  [4] Trocar arquivo")
        print("  [0] Sair")
        
        opcao = input("\n  Escolha a análise: ").strip()
        
        try:
            with open(caminho_arquivo, 'r') as f:
                codigo = f.read()
        except Exception as e:
            print(f"\n  [ERRO] Não foi possível ler o arquivo: {e}")
            return False

        if opcao == "1":
            executar_analise_lexica(codigo)
        elif opcao == "2":
            executar_analise_sintatica(codigo)
        elif opcao == "3":
            executar_analise_semantica(codigo, caminho_arquivo)
        elif opcao == "4":
            return True
        elif opcao == "0":
            return False
        else:
            print("\n  [ERRO] Opção inválida!")
            continue
            
        input("\n  Pressione ENTER para continuar...")
    
    return True

def menu_principal():
    print("\n" + linha())
    print("COMPILADOR TONTO".center(LARGURA))
    print("Análise Léxica, Sintática e Semântica".center(LARGURA))
    print(linha())
    print("\n  [1] Selecionar Arquivo de Teste")
    print("  [0] Sair")

if __name__ == "__main__":
    while True:
        menu_principal()
        opcao = input("\n  Escolha uma opção: ").strip()
        
        if opcao == "1":
            while True:
                caminho = selecionar_arquivo()
                if caminho:
                    continuar = menu_tipo_analise(caminho)
                    if not continuar:
                        break
                else:
                    break
        elif opcao == "0":
            print("\n" + linha())
            print("Encerrando...".center(LARGURA))
            print(linha() + "\n")
            break
        else:
            print("\n  [ERRO] Opção inválida!")
