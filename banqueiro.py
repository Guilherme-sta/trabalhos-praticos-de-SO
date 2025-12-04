def realiza_banqueiro(P_inicial,N_inicial,livre_inicial): 

    P = P_inicial.copy()
    N = N_inicial.copy()
    livre = livre_inicial

    estados = []
    livres = []

    # Inicia com deadlock como False, caso ache um muda para True
    deadLock_detectado = False
    # Salva os Estados iniciais
    def salvar():
        estados.append([(P[i], N[i]) for i in range(3)])
        livres.append(livre)

    salvar()

    while True:
        executou = False
        for i in range(len(P)):
            # Processo finalizou e continua para o próximo 
            if N[i] == "-":
                continue
            
            # Para ser executado deve haver Posse + Livre >= Necessário 
            if P[i] + livre >= N[i]:
                # Execução 
                falta = N[i] - P[i]
                livre -= falta
                P[i] = N[i]
                salvar()

                # Libera o Recurso ao terminar o processo!
                livre += P[i]
                P[i] = 0
                N[i] = "-"
                salvar()

                executou = True
                break # Encontra o processo e retoma a busca de um outro

        if not executou:
            # Caso um processo não acabe, é um DeadLock
            if any(N[i] != "-" for i in range(3)):
                deadLock_detectado = True
            break # Fim da Simulação
    
    return estados, livres, deadLock_detectado

def fmt(text, w):
    return str(text).center(w)

def montar_tabela(estados, livres, deadLock_detectado):
    col = len(estados)
    largura = 14   
    largura_proc = 12  

    print("┌" + "─"*largura_proc + "┬" + "┬".join(["─"*largura]*col) + "┐")

    header = "│" + fmt("Processo", largura_proc) + "│"
    for i in range(col):
        header += fmt(f"E{i+1}", largura) + "│"
    print(header)

    print("├" + "─"*largura_proc + "┼" + "┼".join(["─"*largura]*col) + "┤")

    for p_idx, nome in enumerate(processos):
        linha = "│" + fmt(nome, largura_proc) + "│"
        for e in range(col):
            Pv, Nv = estados[e][p_idx]
            linha += fmt(f"P:{Pv} N:{Nv}", largura) + "│"
        print(linha)

    print("├" + "─"*largura_proc + "┼" + "┼".join(["─"*largura]*col) + "┤")

    linha = "│" + fmt("Livre", largura_proc) + "│"
    for L in livres:
        linha += fmt(L, largura) + "│"
    print(linha)

    print("└" + "─"*largura_proc + "┴" + "┴".join(["─"*largura]*col) + "┘")

    if deadLock_detectado:
        print("\nAVISO: O sistema entrou em um estado inseguro e em DEADLOCK.")
        print("Nenhum processo pode ser executado, pois a condição P + Livre >= N não é satisfeita.")
    else:
        print("\nO sistema está em um estado seguro (todos os processos terminaram).")


# Processo sem DeadLock
processos = ["A", "B", "C"]
P_inicial = [3, 2, 2]
N_inicial = [9, 4, 7]
livre_inicial = 3

# Processoo para Deadlock
P_inicial_deadLock = [4, 2, 2] # P de A alterado para 4
N_inicial = [9, 4, 7]
livre_inicial_deadLock = 2 # Livre alterado para 2

# Resultados do Algoritimo
print("----------------- Algoritimo Banqueiro -----------------\n")
estado_seguro, livres_seguro, deadLock_seguro =  realiza_banqueiro(P_inicial, N_inicial, livre_inicial)
montar_tabela(estado_seguro, livres_seguro, deadLock_seguro)
print("----------------------------------------------------------------------------------------\n")
input("Proseguir para Tabela com DeadLock ->")
estado_inseguro, livre_inseguro, deadLock_inseguro = realiza_banqueiro(P_inicial_deadLock, N_inicial, livre_inicial_deadLock)
montar_tabela(estado_inseguro, livre_inseguro, deadLock_inseguro)