__author__ = '22208_65138'

import csv

class grafo:
    def __init__(self):
        self._spo = [] # subject – predicate - object

    #imprimir toda a triple store
    def printIndex(self):
        print(self._spo)

    #carregar um ficheiro csv com triplos
    def load(self, filename):
        print("A ler ficheiro", filename)
        f = open (filename, "r", encoding="utf8")
        reader = csv.reader(f)
        for tuple in reader:
            tuplelength = len(tuple)
            if tuplelength == 3:
                self.add(tuple[0], tuple[1], tuple[2], False)
        f.close()
        print("Ficheiro carregado com sucesso!")

    #adicionar um tuplo a lista existe, o parametro testa existe define se a função se preocupa ou não em prevenir duplicados
    def add(self, sub, pred, obj, preventDuplicate):
        tuple = (sub,pred,obj)
        if preventDuplicate:
            if tuple not in self._spo:
                self._spo.append(tuple)
            else:
                print ('O registo indicado já existe')
        else:
            self._spo.append(tuple)

    #remover um tuplo da lista
    def remove(self, sub, pred, obj):
        self._spo.remove((sub, pred, obj))

    #testar se existe um tuplo na lista
    def existsTuple(self, t):
        if t in self._spo:
            return True
        return False

    #https://docs.python.org/2/tutorial/datastructures.html#list-comprehensions
    def filter(self, element, list):
        return [item for item in list if element in item]

    #Check if an element exists
    def existsElement(self, element, index):
        if any(element in tuple for tuple in list):
            return True
        return False

    def applyinference(self, rule):
        queries = rule.getqueries()
        bindings = []
        for q in queries:
            bindings += self.query(q)
        for b in bindings:
            new_triples = rule.maketriples(b)
            for s, p, o in new_triples:
                self.add(s,p,o,False)
        print('Inferências aplicadas!')

    def searchPos(self, element, pos, list):
        if pos == 1:
            return [(a,b,c) for a,b,c in list if a == element]
        if pos == 2:
            return [(a,b,c) for a,b,c in list if b == element]
        if pos == 3:
            return [(a,b,c) for a,b,c in list if c == element]

    #devolve uma lista de tuplos que preencham os requisitos
    #se alguma posição do tuplo vier com None, a função  não filtra por essa posição, todos os tuplos
    def search(self, tuple):

        subject = tuple[0]
        predicate = tuple[1]
        object = tuple[2]
        result = []#list()

        if  subject != None:
            if  predicate != None:
                if object != None:
                    for a, b, c in self._spo :
                        if a==subject and b==predicate and c==object:
                                result.append ((subject,predicate,object))
                else:
                    for a, b, c in self._spo:
                        if a==subject and b==predicate:
                                result.append ((subject, predicate, c))
            else:
                if object != None:
                    for a, b, c in self._spo:
                        if a==subject and c==object:
                            result.append ((subject, b, object))
                else:
                    #p e o = none
                    for a, b, c in self._spo:
                        if a==subject:
                                result.append ((subject, b, c))
        else: # s não vem preenchido
            if  predicate != None:
                #p tem valor
                if object != None:
                    for a, b, c in self._spo:
                        if b==predicate and c==object:
                            result.append ((a, predicate, object))
                else:
                    for a, b, c in self._spo:
                        if b==predicate:
                                result.append ((a, predicate, c))
            else:
                # s e p sem valor
                if object != None:
                    for a, b, c in self._spo:
                        if c==object:
                            result.append ((a, b, object))
                else:
                    for a, b, c in self._spo:
                        result.append ((a, b, c))


        return result


    # passa uma lista de tuplos (triplos restrição)
    # devolve uma lista de dicionários (var:valor)
    def query(self, clauses):
        bindings = None # resltado a devolver
        for clause in clauses: # para cada triplo
            bpos = {} # dicionário que associa a variável à sua posição no triplo
            qc = [] # lista de elementos a passar ao método triples
            # enumera o triplo, para poder ir buscar cada elemento e sua posição
            for pos, x in enumerate(clause):
                if x.startswith('?'): # para as variáveis
                    # adiciona o valor None à lista de elementos a passar ao método triples
                    qc.append(None)
                    # guarda a posição da variável no triplo (0,1 ou 2)
                    bpos[x[1:]]=pos
                else:
                    # adiciona o valor dado à lista de elementos a passar ao método triples
                    qc.append(x)
            # faz a pesquisa com o triplo acabado de construir
            rows = self.search((qc[0], qc[1], qc[2]))

            ##rows = list(self.triples(qc[0], qc[1], qc[2]))
            # primeiro triplo pesquisa, todos os resultados servem
            # para cada triplo resultado, cria um dicionario de variaveis (1 a 3
            # variaveis)
            # em cada dicionario, as variaveis tomam o valor devolvido pelo elemento
            # na mesma posicao da variavel
            if bindings == None:
                bindings = [] # cria a lista a devolver
                for row in rows: # para cada triplo resultado
                    binding = {} # cria um dicionario
                    for var, pos in bpos.items(): # para cada variável e sua posição
                        # associa à variável o valor do elemento do triplo na sua posição
                        binding[var] = row[pos]
                    bindings.append(binding) # adiciona o dicionario à lista
            else: # triplos pesquisa seguintes, eliminar resultados que não servem
                newb = [] # cria nova lista a devolver
                for binding in bindings: # para cada dicionario da lista de dicionarios
                    for row in rows: # para cada triplo resultado
                        validmatch = True # começa por assumir que o dicionario serve
                        tempbinding = binding.copy() # faz copia temporaria do dicionario
                        for var, pos in bpos.items(): # para cada variavel em sua posição
                            # caso a variavel esteja presente no dicionario
                            if var in tempbinding:
                                # se o valor da variavel diferente do valor na sua posicao no triplo
                                if tempbinding[var] != row[pos]:
                                    validmatch = False # o dicionário não serve
                                else:
                                    # associa à variável o valor do elemento do triplo na sua posição
                                    tempbinding[var] = row[pos]
                        if validmatch and not tempbinding in newb:
                            # se dicionario serve, inclui-o na nova lista
                            newb.append(tempbinding)
                bindings = newb # sbstituiu lista por nova
        return bindings

    #limpa o uri para devolver apenas o valor do objecto
    def CleanUri (self, uri):
        arr = str.split (uri, "/")
        if len (arr) == 1:
            return arr[0]
        return arr[len(arr)-1]

"""
    def queryTuple(self, clauses):
        bindings = None # resltado a devolver
        for clause in clauses: # para cada triplo
            bpos = [] # dicionário que associa a variável à sua posição no triplo
            qc = [] # lista de elementos a passar ao método triples
            # enumera o triplo, para poder ir buscar cada elemento e sua posição
            for pos, x in enumerate(clause):
                if x.startswith('?'): # para as variáveis
                    # adiciona o valor None à lista de elementos a passar ao método triples
                    qc.append(None)
                    # guarda a posição da variável no triplo (0,1 ou 2)
                    #bpos[x[1:]]=pos
                    bpos.append((x[1:],pos))
                else:
                    # adiciona o valor dado à lista de elementos a passar ao método triples
                    qc.append(x)
            # faz a pesquisa com o triplo acabado de construir
            #rows = self.search((qc[0], qc[1], qc[2]), self._spo)

            rows = list(self.triples(qc[0], qc[1], qc[2]))
            # primeiro triplo pesquisa, todos os resultados servem
            # para cada triplo resultado, cria um dicionario de variaveis (1 a 3
            # variaveis)
            # em cada dicionario, as variaveis tomam o valor devolvido pelo elemento
            # na mesma posicao da variavel
            if bindings == None:
                bindings = [] # cria a lista a devolver
                for row in rows: # para cada triplo resultado
                    binding = [] # cria um dicionario
                    for var, pos in bpos: # para cada variável e sua posição
                        # associa à variável o valor do elemento do triplo na sua posição
                        #binding[var] = row[pos]
                        #if pos == 0
                        #    b0 = row[pos]
                        #elif pos == 1:
                        #    b1 = row[pos]
                        #else:
                        #    b1 = row[pos]
                        bindings.append((var, row[pos]))
                    #bindings.append(var(b0,b1, b2)) # adiciona o dicionario à lista

            else: # triplos pesquisa seguintes, eliminar resultados que não servem
                newb = [] # cria nova lista a devolver
                for binding in bindings: # para cada dicionario da lista de dicionarios
                    for row in rows: # para cada triplo resultado
                        validmatch = True # começa por assumir que o dicionario serve
                        tempbinding = binding # faz copia temporaria do dicionario
                        for var, pos in bpos: # para cada variavel em sua posição
                            # caso a variavel esteja presente no dicionario
                            if var in tempbinding:
                                # se o valor da variavel diferente do valor na sua posicao no triplo
                                if tempbinding[pos] != row[pos]:
                                    validmatch = False # o dicionário não serve
                                else:
                                    # associa à variável o valor do elemento do triplo na sua posição
                                    tempbinding[pos] = row[pos]
                        if validmatch and not tempbinding in newb:
                            # se dicionario serve, inclui-o na nova lista
                            newb.append(tempbinding)
                            print (tempbinding)
                bindings = newb # sbstituiu lista por nova
        return bindings

    # passa uma lista de tuplos (triplos restrição)
    # devolve uma lista de dicionários (var:valor)
    def queryPB(self, clauses):
        clauseConditions = []
        bindings = None # resltado a devolver
        for clause in clauses: # para cada triplo
            bpos = [] # dicionário que associa a variável à sua posição no triplo
            qc = [] # lista de elementos a passar ao método triples
            # enumera o triplo, para poder ir buscar cada elemento e sua posição
            for pos, x in enumerate(clause):
                if x.startswith('?'): # para as variáveis
                    # adiciona o valor None à lista de elementos a passar ao método triples
                    qc.append(None)
                    # guarda a posição da variável no triplo (0,1 ou 2)
                    bpos.append((x,pos))
                else:
                    # adiciona o valor dado à lista de elementos a passar ao método triples
                    qc.append(x)

            # faz a pesquisa com o triplo acabado de construir
            tuple = (qc[0],qc[1],qc[2])
            rows = self.search(tuple, self._spo)
            if bindings == None:
                clauseConditions.append(bpos);
                bindings = [];
                for row in rows:
                    bindings.append(row)
            # primeiro triplo pesquisa, todos os resultados servem
            # para cada triplo resultado, cria um dicionario de variaveis (1 a 3
            # variaveis)
            # em cada dicionario, as variaveis tomam o valor devolvido pelo elemento
            # na mesma posicao da variavel
            else: # triplos pesquisa seguintes, eliminar resultados que não servem
                bindingPos = 0
                newb = [] # cria nova lista a devolver
                for binding in bindings: # para cada dicionario da lista de dicionarios
                    searchTuple = [None,None,None]
                    for row in rows: # para cada triplo resultado
                        #j=0
                        for cc in clauseConditions[bindingPos]:
#                            for (clauseData, posB) in cc:
                                for pt in bpos:
                                    if pt[0]==cc[0]and pt[1] == cc[1]: # as variaveis são comun
                                        searchTuple[pt[1]] = binding[pt[1]]
                                    #else:

                        resultset = self.search( (searchTuple[0],searchTuple[1],searchTuple[2]), bindings);
                        for searchTuple in resultset:
                            newb.append(searchTuple)
                    bindingPos = bindingPos + 1;

                comuns = self.search(tuple, self._spo)
                validmatch = True # começa por assumir que o dicionario serve
                tempbinding = binding.copy() # faz copia temporaria do dicionario
                for var, pos in bpos.items(): # para cada variavel em sua posição
                    # caso a variavel esteja presente no dicionario
                    if var in tempbinding:
                        # se o valor da variavel diferente do valor na sua posicao no triplo
                        if tempbinding[var] != row[pos]:
                            validmatch = False # o dicionário não serve
                        else:
                            # associa à variável o valor do elemento do triplo na sua posição
                            tempbinding[var] = row[pos]
                if validmatch:
                    # se dicionario serve, inclui-o na nova lista
                newb.append(tempbinding)

                bindings = newb # sbstituiu lista por nova
        return bindings
"""
