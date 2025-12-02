processos = ["A", "B", "C"]
P_inicial = [3, 2, 2]
N_inicial = [9, 4, 7]
livre_inicial = 3

P = P_inicial.copy()
N = N_inicial.copy()
livre = livre_inicial

estados = []
livres = []

def salvar():
    estados.append([(P[i], N[i]) for i in range(3)])
    livres.append(livre)
salvar()

ordem = [1, 2, 0]
while True:
    executou = False
    for i in range(3):
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
        break

def fmt(text, w):
    return str(text).center(w)

def montar_tabela(estados, livres):
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

montar_tabela(estados, livres)