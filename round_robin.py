from collections import deque
import matplotlib.pyplot as plt

tasks = {
    't1': {'arrival': 5,  'burst': 10},
    't2': {'arrival': 15, 'burst': 30},
    't3': {'arrival': 10, 'burst': 20},
    't4': {'arrival': 0,  'burst': 40},
}
quantum = 15
ctx = 4

remaining = {t: tasks[t]['burst'] for t in tasks}
finish = {t: None for t in tasks}

ready = deque()
arrived = set()
time = 0
on_cpu = None
slice_used = 0
timeline = []  

def check_arrivals(curr_time):
    for t in ("t1", "t2", "t3", "t4"):
        if tasks[t]["arrival"] == curr_time and t not in arrived:
            ready.append(t)
            arrived.add(t)

while any(remaining[t] > 0 for t in tasks):
    check_arrivals(time)

    if on_cpu is None and not ready:
        future_arrivals = [tasks[t]["arrival"] for t in tasks if t not in arrived]
        if future_arrivals:
            time = min(future_arrivals)
            check_arrivals(time)
            continue
        break

    if on_cpu is None and ready:
        on_cpu = ready.popleft()
        slice_used = 0
        exec_start = time

    remaining[on_cpu] -= 1
    slice_used += 1
    time += 1
    check_arrivals(time)

    if remaining[on_cpu] == 0:
        exec_end = time
        timeline.append((exec_start, exec_end, on_cpu))
        finish[on_cpu] = exec_end

        if any(remaining[x] > 0 for x in tasks):
            for _ in range(ctx):
                time += 1
                check_arrivals(time)
        on_cpu = None
        slice_used = 0
        continue

    if slice_used == quantum:
        exec_end = time
        timeline.append((exec_start, exec_end, on_cpu))
        for _ in range(ctx):
            time += 1
            check_arrivals(time)
        ready.append(on_cpu)
        on_cpu = None
        slice_used = 0
        continue

turnaround = {t: finish[t] - tasks[t]['arrival'] for t in tasks}
waiting = {t: turnaround[t] - tasks[t]['burst'] for t in tasks}

print("\n=== RESULTADOS FINAIS  ===\n")
for t in ("t1","t2","t3","t4"):
    print(f"{t}: término = {finish[t]} u.t, T_vida = {turnaround[t]} u.t, T_espera = {waiting[t]} u.t")
print()
print("Tm_vida   =", sum(turnaround.values())/4 ,"u.t")
print("Tm_espera =", sum(waiting.values())/4, )

fig, ax = plt.subplots(figsize=(12, 4))
ypos = {'t1': 3, 't2': 2, 't3': 1, 't4': 0}
colors = {'t1': 'tab:blue', 't2': 'tab:green', 't3': 'tab:orange', 't4': 'tab:red'}

for start, end, task in timeline:
    ax.barh(ypos[task], end - start, left=start, height=0.6,
            color=colors[task], edgecolor='black')
    ax.text((start + end)/2, ypos[task], task, ha='center', va='center',
            color="white", fontsize=9)

ax.set_yticks([0,1,2,3])
ax.set_yticklabels(["t4","t3","t2","t1"])
ax.set_xlabel("Tempo")
ax.set_title("Round Robin — Quantum = 15, Context Switch = 4")
plt.grid(axis='x', linestyle='--')
plt.tight_layout()
plt.show()