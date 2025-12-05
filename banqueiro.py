def realiza_banqueiro(P_inicial,N_inicial,livre_inicial): 
    P = P_inicial.copy()
    N = N_inicial.copy()
    livre = livre_inicial

    estados = []
    livres = []

    deadLock_detectado = False
    def salvar():
        estados.append([(P[i], N[i]) for i in range(3)])
        livres.append(livre)

    salvar()

    while True:
        executou = False
        for i in range(len(P)):
            if N[i] == "-":
                continue
            if P[i] + livre >= N[i]:
                falta = N[i] - P[i]
                livre -= falta
                P[i] = N[i]
                salvar()

                livre += P[i]
                P[i] = 0
                N[i] = "-"
                salvar()

                executou = True
                break

        if not executou:
            if any(N[i] != "-" for i in range(3)):
                deadLock_detectado = True
            break
    
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


processos = ["A", "B", "C"]
P_inicial = [3, 2, 2]
N_inicial = [9, 4, 7]
livre_inicial = 3

P_inicial_deadLock = [4, 2, 2] 
N_inicial = [9, 4, 7]
livre_inicial_deadLock = 2 

print("----------------- Algoritimo Banqueiro -----------------\n")
estado_seguro, livres_seguro, deadLock_seguro =  realiza_banqueiro(P_inicial, N_inicial, livre_inicial)
montar_tabela(estado_seguro, livres_seguro, deadLock_seguro)
print("----------------------------------------------------------------------------------------\n")
input("Proseguir para Tabela com DeadLock ->")
estado_inseguro, livre_inseguro, deadLock_inseguro = realiza_banqueiro(P_inicial_deadLock, N_inicial, livre_inicial_deadLock)
montar_tabela(estado_inseguro, livre_inseguro, deadLock_inseguro)