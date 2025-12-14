class AnalisadorSemantico:
    def __init__(self, ast):
        self.ast = ast
        self.resultados = []
        
        self.classes_por_nome = {}
        self.classes_por_estereotipo = {}
        self.gensets_por_general = {}
        self.relacoes_por_classe = {}
        
        self._construir_indices()
    
    def _construir_indices(self):
        for cls in self.ast.classes:
            self.classes_por_nome[cls['name']] = cls
            
            stereotype = cls['stereotype']
            if stereotype not in self.classes_por_estereotipo:
                self.classes_por_estereotipo[stereotype] = []
            self.classes_por_estereotipo[stereotype].append(cls)
        
        for genset in self.ast.gensets:
            general = genset['general']
            if general not in self.gensets_por_general:
                self.gensets_por_general[general] = []
            self.gensets_por_general[general].append(genset)
        
        for rel in self.ast.relations:
            domain = rel.get('domain')
            range_cls = rel.get('range')
            
            if domain:
                if domain not in self.relacoes_por_classe:
                    self.relacoes_por_classe[domain] = []
                self.relacoes_por_classe[domain].append(rel)
            
            if range_cls:
                if range_cls not in self.relacoes_por_classe:
                    self.relacoes_por_classe[range_cls] = []
                self.relacoes_por_classe[range_cls].append(rel)
    
    def _adicionar_resultado(self, tipo, padrao, mensagem):
        self.resultados.append({
            'tipo': tipo,
            'padrao': padrao,
            'mensagem': mensagem
        })
    
    def _obter_classes_especializando(self, classe_pai, estereotipo=None):
        especializacoes = []
        for cls in self.ast.classes:
            if cls['specializes'] == classe_pai:
                if estereotipo is None or cls['stereotype'] == estereotipo:
                    especializacoes.append(cls)
        return especializacoes
    
    def _obter_genset_para_classe(self, classe_nome):
        return self.gensets_por_general.get(classe_nome, [])
    
    def _genset_tem_modificador(self, genset, modificador):
        if genset['modifiers']:
            return modificador in genset['modifiers']
        return False
    
    def _classe_tem_relacao_interna(self, classe, estereotipo_rel):
        for rel in classe['internal_relations']:
            if len(rel) > 1 and rel[1] == estereotipo_rel:
                return True
        return False
    
    def _classe_participa_relacao_externa(self, classe_nome, estereotipo_rel=None):
        relacoes = self.relacoes_por_classe.get(classe_nome, [])
        if estereotipo_rel:
            return any(rel.get('stereotype') == estereotipo_rel for rel in relacoes)
        return len(relacoes) > 0
    
    def validar_subkind_pattern(self):
        subkinds = self.classes_por_estereotipo.get('subkind', [])
        
        if not subkinds:
            self._adicionar_resultado('INFO', 'Subkind', 'Nenhum Subkind Pattern encontrado.')
            return
        
        subkinds_por_pai = {}
        for subkind in subkinds:
            pai = subkind['specializes']
            if pai:
                if pai not in subkinds_por_pai:
                    subkinds_por_pai[pai] = []
                subkinds_por_pai[pai].append(subkind)
        
        for pai, lista_subkinds in subkinds_por_pai.items():
            classe_pai = self.classes_por_nome.get(pai)
            if not classe_pai or classe_pai['stereotype'] != 'kind':
                self._adicionar_resultado(
                    'ALERTA', 'Subkind',
                    f"Subkind incompleto: '{lista_subkinds[0]['name']}' especializa '{pai}' que não é um kind."
                )
                continue
            
            gensets = self._obter_genset_para_classe(pai)
            tem_genset_disjoint = False
            
            for genset in gensets:
                specifics = genset['specifics']
                subkind_names = [s['name'] for s in lista_subkinds]
                if any(name in specifics for name in subkind_names):
                    if self._genset_tem_modificador(genset, 'disjoint'):
                        tem_genset_disjoint = True
                        break
            
            if tem_genset_disjoint:
                subkind_names = ', '.join([s['name'] for s in lista_subkinds])
                self._adicionar_resultado(
                    'OK', 'Subkind',
                    f"Subkind completo: {subkind_names} -> {pai}"
                )
            else:
                self._adicionar_resultado(
                    'ALERTA', 'Subkind',
                    f"Subkind incompleto: Subkinds de '{pai}' não possuem genset disjoint."
                )
    
    def validar_role_pattern(self):
        roles = self.classes_por_estereotipo.get('role', [])
        
        if not roles:
            self._adicionar_resultado('INFO', 'Role', 'Nenhum Role Pattern encontrado.')
            return
        
        for role in roles:
            pai = role['specializes']
            nome = role['name']
            
            if not pai:
                self._adicionar_resultado(
                    'ALERTA', 'Role',
                    f"Role incompleto: '{nome}' não especializa nenhuma classe."
                )
                continue
            
            classe_pai = self.classes_por_nome.get(pai)
            if not classe_pai or classe_pai['stereotype'] != 'kind':
                if not classe_pai or classe_pai['stereotype'] != 'roleMixin':
                    self._adicionar_resultado(
                        'ALERTA', 'Role',
                        f"Role incompleto: '{nome}' especializa '{pai}' que não é um kind ou roleMixin."
                    )
                    continue
            
            participa_material = self._classe_participa_relacao_externa(nome, 'material')
            participa_mediation = self._classe_participa_relacao_externa(nome, 'mediation')
            
            participa_em_relator = False
            for cls in self.ast.classes:
                if cls['stereotype'] == 'relator':
                    for rel in cls['internal_relations']:
                        if len(rel) > 5 and rel[5] == nome:
                            participa_em_relator = True
                            break
                        if len(rel) > 4 and rel[4] == nome:
                            participa_em_relator = True
                            break
            
            if participa_material or participa_mediation or participa_em_relator:
                self._adicionar_resultado(
                    'OK', 'Role',
                    f"Role completo: {nome} -> {pai}"
                )
            else:
                self._adicionar_resultado(
                    'ALERTA', 'Role',
                    f"Role incompleto: '{nome}' não participa de nenhuma relação material/mediada."
                )
    
    def validar_phase_pattern(self):
        phases = self.classes_por_estereotipo.get('phase', [])
        
        if not phases:
            self._adicionar_resultado('INFO', 'Phase', 'Nenhum Phase Pattern encontrado.')
            return
        
        phases_por_pai = {}
        for phase in phases:
            pai = phase['specializes']
            if pai:
                if pai not in phases_por_pai:
                    phases_por_pai[pai] = []
                phases_por_pai[pai].append(phase)
        
        for pai, lista_phases in phases_por_pai.items():
            classe_pai = self.classes_por_nome.get(pai)
            if not classe_pai or classe_pai['stereotype'] != 'kind':
                self._adicionar_resultado(
                    'ALERTA', 'Phase',
                    f"Phase incompleto: Phases de '{pai}' - '{pai}' não é um kind."
                )
                continue
            
            if len(lista_phases) < 2:
                self._adicionar_resultado(
                    'ALERTA', 'Phase',
                    f"Phase incompleto: O kind '{pai}' tem apenas uma fase: {lista_phases[0]['name']}."
                )
                continue
            
            gensets = self._obter_genset_para_classe(pai)
            tem_genset_disjoint = False
            
            for genset in gensets:
                specifics = genset['specifics']
                phase_names = [p['name'] for p in lista_phases]
                if any(name in specifics for name in phase_names):
                    if self._genset_tem_modificador(genset, 'disjoint'):
                        tem_genset_disjoint = True
                        break
            
            if tem_genset_disjoint:
                phase_names = ', '.join([p['name'] for p in lista_phases])
                self._adicionar_resultado(
                    'OK', 'Phase',
                    f"Phase completo: {phase_names} -> {pai}"
                )
            else:
                self._adicionar_resultado(
                    'ALERTA', 'Phase',
                    f"Phase incompleto: Phases de '{pai}' não possuem genset disjoint (obrigatório)."
                )
    
    def validar_relator_pattern(self):
        relators = self.classes_por_estereotipo.get('relator', [])
        
        if not relators:
            self._adicionar_resultado('INFO', 'Relator', 'Nenhum Relator Pattern encontrado.')
            return
        
        for relator in relators:
            nome = relator['name']
            
            mediacoes_validas = 0
            mediacoes_invalidas = []

            for rel in relator['internal_relations']:
                if len(rel) > 1 and rel[1] == 'mediation':
                    nome_alvo = rel[5] if len(rel) > 5 else (rel[4] if len(rel) > 4 else None)

                    if nome_alvo:
                        classe_alvo = self.classes_por_nome.get(nome_alvo)
                        if classe_alvo:
                            est_alvo = classe_alvo.get('stereotype')
                            if est_alvo == 'role':
                                mediacoes_validas += 1
                            else:
                                mediacoes_invalidas.append(f"'{nome_alvo}' é {est_alvo}, não role")
                        else:
                            mediacoes_invalidas.append(f"'{nome_alvo}' não encontrada")
            
            if mediacoes_validas >= 2:
                self._adicionar_resultado(
                    'OK', 'Relator',
                    f"Relator completo: {nome} possui {mediacoes_validas} mediações válidas (para roles)."
                )
            elif mediacoes_validas == 1:
                self._adicionar_resultado(
                    'ALERTA', 'Relator',
                    f"Relator incompleto: '{nome}' possui apenas {mediacoes_validas} mediação válida (mínimo 2)."
                )
            elif mediacoes_invalidas:
                erros = "; ".join(mediacoes_invalidas)
                self._adicionar_resultado(
                    'ALERTA', 'Relator',
                    f"Relator incompleto: '{nome}' não possui mediações para roles. Problemas: {erros}."
                )
            else:
                self._adicionar_resultado(
                    'ALERTA', 'Relator',
                    f"Relator incompleto: '{nome}' não possui mediações."
                )
    
    def validar_mode_pattern(self):
        modes = self.classes_por_estereotipo.get('mode', [])
        
        if not modes:
            self._adicionar_resultado('INFO', 'Mode', 'Nenhum Mode Pattern encontrado.')
            return
        
        for mode in modes:
            nome = mode['name']
            
            tem_characterization = False
            tem_external_dependence = False
            
            for rel in mode['internal_relations']:
                if len(rel) > 1:
                    if rel[1] == 'characterization':
                        tem_characterization = True
                    if rel[1] == 'externalDependence':
                        tem_external_dependence = True
            
            if tem_characterization and tem_external_dependence:
                self._adicionar_resultado(
                    'OK', 'Mode',
                    f"Mode completo: {nome} possui characterization e externalDependence."
                )
            elif tem_characterization:
                self._adicionar_resultado(
                    'ALERTA', 'Mode',
                    f"Mode incompleto: '{nome}' não possui relação de dependência externa."
                )
            elif tem_external_dependence:
                self._adicionar_resultado(
                    'ALERTA', 'Mode',
                    f"Mode incompleto: '{nome}' não possui relação de characterization."
                )
            else:
                self._adicionar_resultado(
                    'ALERTA', 'Mode',
                    f"Mode incompleto: '{nome}' não possui characterization nem externalDependence."
                )
    
    def validar_rolemixin_pattern(self):
        rolemixins = self.classes_por_estereotipo.get('roleMixin', [])
        
        if not rolemixins:
            self._adicionar_resultado('INFO', 'RoleMixin', 'Nenhum RoleMixin Pattern encontrado.')
            return
        
        for rolemixin in rolemixins:
            nome = rolemixin['name']
            
            roles_especializando = self._obter_classes_especializando(nome, 'role')
            
            if len(roles_especializando) < 2:
                self._adicionar_resultado(
                    'ALERTA', 'RoleMixin',
                    f"RoleMixin incompleto: '{nome}' não tem pelo menos 2 roles especializando."
                )
                continue
            
            gensets = self._obter_genset_para_classe(nome)
            
            if gensets:
                role_names = ', '.join([r['name'] for r in roles_especializando])
                self._adicionar_resultado(
                    'OK', 'RoleMixin',
                    f"RoleMixin completo: {nome} com roles: {role_names}"
                )
            else:
                self._adicionar_resultado(
                    'ALERTA', 'RoleMixin',
                    f"RoleMixin incompleto: '{nome}' não possui genset definido."
                )
    
    def analisar(self):
        self.resultados = []
        
        self.validar_subkind_pattern()
        self.validar_role_pattern()
        self.validar_phase_pattern()
        self.validar_relator_pattern()
        self.validar_mode_pattern()
        self.validar_rolemixin_pattern()
        
        return self.resultados
    
    def gerar_relatorio(self):
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
        
        cabecalho("ANÁLISE SEMÂNTICA")
        print("Validação de Padrões de Projeto de Ontologia".center(LARGURA))
        
        if not self.resultados:
            self.analisar()
        
        contadores = {'OK': 0, 'ALERTA': 0, 'INFO': 0}
        
        subcabecalho("VALIDAÇÃO DOS PADRÕES")
        
        for resultado in self.resultados:
            tipo = resultado['tipo']
            mensagem = resultado['mensagem']
            contadores[tipo] += 1
            
            if tipo == 'OK':
                print(f"\n  [OK]     {mensagem}")
            elif tipo == 'ALERTA':
                print(f"\n  [ALERTA] {mensagem}")
            else:
                print(f"\n  [INFO]   {mensagem}")
        
        subcabecalho("RESUMO")
        
        total = contadores['OK'] + contadores['ALERTA']
        print(f"\n  {'CATEGORIA':<25} {'QTD':>5}")
        print("  " + "-" * 32)
        print(f"  {'Padrões completos':<25} {contadores['OK']:>5}")
        print(f"  {'Padrões incompletos':<25} {contadores['ALERTA']:>5}")
        print(f"  {'Padrões ausentes':<25} {contadores['INFO']:>5}")
        print("  " + "-" * 32)
        print(f"  {'Total analisado':<25} {total:>5}")
        
        print("\n" + linha())
        if contadores['ALERTA'] == 0 and contadores['OK'] > 0:
            print("Análise semântica concluída com sucesso.".center(LARGURA))
        elif contadores['ALERTA'] > 0:
            print("Análise semântica concluída com alertas.".center(LARGURA))
        else:
            print("Análise semântica concluída.".center(LARGURA))
        print(linha())


def analisar(ast):
    analisador = AnalisadorSemantico(ast)
    analisador.analisar()
    analisador.gerar_relatorio()
    return analisador.resultados
