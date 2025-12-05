def algoritmo_do_banqueiro(E, A, C, R):
    """
    Implementa o Algoritmo do Banqueiro para detecção de deadlock.

    :param E: Vetor de Recursos Existentes (Existentes).
    :param A: Vetor de Recursos Disponíveis (Available).
    :param C: Matriz de Alocação Corrente (Allocation).
    :param R: Matriz de Requisições (Request/Need).
    :return: Sequência de execução segura ou None se o estado for inseguro.
    """
    
    # Número de processos (n) e de tipos de recursos (m)
    n = len(C)
    m = len(E)
    
    # Vetor de processos marcados/concluídos
    marcado = [False] * n
    # Cópia do vetor A (Recursos Disponíveis) que será atualizada
    trabalho = list(A)
    # Lista para armazenar a sequência segura
    sequencia_segura = []
    
    print(f"--- Início da Simulação ---")
    print(f"Recursos Disponíveis Iniciais (A): {trabalho}\n")
    
    # Loop principal para encontrar uma sequência de execução segura
    # O loop faz no máximo 'n' iterações externas, garantindo que a execução termine
    while len(sequencia_segura) < n:
        processo_encontrado = False
        
        # 1. Procure por um processo desmarcado P_i para o qual R_i <= trabalho
        for i in range(n):
            if not marcado[i]:
                # i-ésima linha de R é a requisição de P_i
                Requisicao_i = R[i]
                
                # Verifica se R_i <= trabalho (comparação elemento por elemento)
                pode_rodar = True
                for j in range(m):
                    if Requisicao_i[j] > trabalho[j]:
                        pode_rodar = False
                        break # Se P_i precisar de mais recursos do que 'trabalho' possui, ele não pode rodar
                
                # 2. Se um processo com tais características for encontrado:
                if pode_rodar:
                    processo_encontrado = True
                    
                    print(f"✅ Processo P{i+1} pode rodar. R{i+1} ({Requisicao_i}) <= Trabalho ({trabalho}).")
                    
                    # Adicione a i-ésima linha de C a trabalho (liberação de recursos)
                    Alocacao_i = C[i]
                    for j in range(m):
                        trabalho[j] += Alocacao_i[j]
                    
                    # Marque o processo
                    marcado[i] = True
                    sequencia_segura.append(f"P{i+1}")
                    
                    print(f"   P{i+1} rodou e liberou recursos C{i+1} ({Alocacao_i}).")
                    print(f"   Novo Recursos Disponíveis (A): {trabalho}")
                    print("-" * 25)
                    
                    # Volte para o passo 1 (que é o início do loop 'while')
                    break 
        
        # 3. Se não houver nenhum processo nesta situação, o algoritmo termina.
        if not processo_encontrado and len(sequencia_segura) < n:
            print(f"❌ Não foi possível encontrar um processo desmarcado para rodar.")
            print("--- Conclusão: ESTADO INSEGURO (DEADLOCK) ---")
            return None # Retorna None indicando que o estado é inseguro

    print("\n--- Conclusão: ESTADO SEGURO ---")
    return sequencia_segura


# --- DADOS DO EXEMPLO (Adaptados do slide) ---

# Vetor de Recursos Existentes E (4 tipos: Hd Ext, SSD Ext, Impressoras, Scanner)
E_exemplo = [4, 2, 3, 1] 

# Vetor de Recursos Disponíveis A
A_exemplo = [2, 1, 0, 0]

# Matriz de Alocação Corrente C (P1, P2, P3)
# C_ij = recursos j entregues ao processo i
C_exemplo = [
    [0, 0, 1, 0],  # P1 alocado
    [2, 0, 0, 1],  # P2 alocado
    [0, 1, 2, 0]   # P3 alocado
]

# Matriz de Requisições R (P1, P2, P3)
# R_ij = recursos j de que o processo i precisa
R_exemplo = [
    [2, 0, 0, 1],  # P1 precisa
    [1, 0, 1, 0],  # P2 precisa
    [2, 1, 0, 0]   # P3 precisa
]

# --- CHAMADA DO ALGORITMO ---
resultado = algoritmo_do_banqueiro(E_exemplo, A_exemplo, C_exemplo, R_exemplo)

if resultado:
    print(f"Sequência Segura Encontrada: {resultado}")
