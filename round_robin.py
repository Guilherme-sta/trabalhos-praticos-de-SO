from collections import deque
import matplotlib.pyplot as plt

tarefas = {
    't1': {'chegada': 5,  'duracao': 10},
    't2': {'chegada': 15, 'duracao': 30},
    't3': {'chegada': 10, 'duracao': 20},
    't4': {'chegada': 0,  'duracao': 40},
}

quantum = 15
troca_contexto = 4
restante = {t: tarefas[t]['duracao'] for t in tarefas}
termino = {t: None for t in tarefas}
prontos = deque()
ja_veio = set()
tempo = 0
no_cpu = None
quantum_usado = 0
linha_do_tempo = []

def verificar_chegadas(t_atual):
    for t in ("t1", "t2", "t3", "t4"):
        if tarefas[t]["chegada"] == t_atual and t not in ja_veio:
            prontos.append(t)
            ja_veio.add(t)


while any(restante[t] > 0 for t in tarefas):
    verificar_chegadas(tempo)

    if no_cpu is None and not prontos:
        proximas_chegadas = [tarefas[t]["chegada"] for t in tarefas if t not in ja_veio]
        if proximas_chegadas:
            tempo = min(proximas_chegadas)
            verificar_chegadas(tempo)
            continue
        break

    if no_cpu is None and prontos:
        no_cpu = prontos.popleft()
        quantum_usado = 0
        inicio_exec = tempo

    restante[no_cpu] -= 1
    quantum_usado += 1
    tempo += 1
    verificar_chegadas(tempo)

    if restante[no_cpu] == 0:
        fim_exec = tempo
        linha_do_tempo.append((inicio_exec, fim_exec, no_cpu))
        termino[no_cpu] = fim_exec

        if any(restante[x] > 0 for x in tarefas):
            for _ in range(troca_contexto):
                tempo += 1
                verificar_chegadas(tempo)

        no_cpu = None
        quantum_usado = 0
        continue

    if quantum_usado == quantum:
        fim_exec = tempo
        linha_do_tempo.append((inicio_exec, fim_exec, no_cpu))

        for _ in range(troca_contexto):
            tempo += 1
            verificar_chegadas(tempo)

        prontos.append(no_cpu)
        no_cpu = None
        quantum_usado = 0
        continue

turnaround = {t: termino[t] - tarefas[t]['chegada'] for t in tarefas}
espera = {t: turnaround[t] - tarefas[t]['duracao'] for t in tarefas}

print("\n=== RESULTADOS FINAIS  ===\n")
for t in ("t1","t2","t3","t4"):
    print(f"{t}: término = {termino[t]} u.t, T_vida = {turnaround[t]} u.t, T_espera = {espera[t]} u.t")
print()
print("Tempo médio de vida   =", sum(turnaround.values())/4 ,"u.t")
print("Tempo médio de espera =", sum(espera.values())/4, "u.t")

fig, ax = plt.subplots(figsize=(12, 4))
posicao_y = {'t1': 3, 't2': 2, 't3': 1, 't4': 0}
cores = {'t1': 'tab:blue', 't2': 'tab:green', 't3': 'tab:orange', 't4': 'tab:red'}
for inicio, fim, tarefa in linha_do_tempo:
    ax.barh(posicao_y[tarefa], fim - inicio, left=inicio, height=0.6,
            color=cores[tarefa], edgecolor='black')
    ax.text((inicio + fim)/2, posicao_y[tarefa], tarefa,
            ha='center', va='center', color="white", fontsize=9)

ax.set_yticks([0,1,2,3])
ax.set_yticklabels(["t4","t3","t2","t1"])
ax.set_xlabel("Tempo")
ax.set_title("Round Robin — Quantum = 15, Troca de Contexto = 4")
plt.grid(axis='x', linestyle='--')
plt.tight_layout()
plt.show()