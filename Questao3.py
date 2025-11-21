import time
import random
import copy
import matplotlib.pyplot as plt
import sys
from functools import wraps

sys.setrecursionlimit(200000)

# --- 1. Implementação dos 6 Algoritmos de Ordenação ---

def timing_decorator(func):
    """Garante que o tempo não é retornado, apenas a lista é modificada (in-place)."""
    @wraps(func)
    def wrapper(arr):
        func(arr)
        return arr
    return wrapper

@timing_decorator
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break

@timing_decorator
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

@timing_decorator
def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def merge_sort_in_place(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort_in_place(L)
        merge_sort_in_place(R)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr

@timing_decorator
def merge_sort(arr):
    merge_sort_in_place(arr)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort_recursive(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort_recursive(arr, low, pi - 1)
        quick_sort_recursive(arr, pi + 1, high)

@timing_decorator
def quick_sort(arr):
    quick_sort_recursive(arr, 0, len(arr) - 1)

# Cycle Sort (Q2)
@timing_decorator
def cycle_sort(arr):
    n = len(arr)
    for cycle_start in range(0, n - 1):
        item = arr[cycle_start]
        pos = cycle_start
        for i in range(cycle_start + 1, n):
            if arr[i] < item:
                pos += 1

        if pos == cycle_start:
            continue
        
        # Lida com duplicatas
        while pos < n and item == arr[pos]:
            pos += 1

        if pos != cycle_start and pos < n:
            arr[pos], item = item, arr[pos]

        while pos != cycle_start:
            pos = cycle_start
            for i in range(cycle_start + 1, n):
                if arr[i] < item:
                    pos += 1
            
            # Lida com duplicatas
            while pos < n and item == arr[pos]:
                pos += 1
            
            if pos != cycle_start and pos < n: 
                arr[pos], item = item, arr[pos]

# --- 2. Funções de Medição e Execução ---

def medir_tempo(func, arr):
    """Mede o tempo de execução de uma função de ordenação."""
    A = copy.deepcopy(arr) 

    
    start_time = time.time()
    func(A)
    end_time = time.time()
    
    return end_time - start_time

def gerar_lista_descendente(n):
    """Gera uma lista de N elementos em ordem decrescente."""
    return list(range(n, 0, -1))

def gerar_lista_randomica(n):
    """Gera uma lista de N elementos randômicos."""
    return [random.randint(1, n * 10) for _ in range(n)]

# --- 3. Execução Principal ---

TAMANHOS_Q3 = [1000, 10000, 20000, 30000, 40000, 50000]
ALGOS = {
    "Bubble (O(N²))": bubble_sort,
    "Selection (O(N²))": selection_sort,
    "Insertion (O(N²))": insertion_sort,
    "Cycle (Q2) (O(N²))": cycle_sort,
    "Merge (O(N log N))": merge_sort,
    "Quick (O(N log N))": quick_sort,
}
NOMES = list(ALGOS.keys())


tempos_randomicos = {nome: [] for nome in NOMES}
tempos_descendentes = []

# ==========================================================
# TESTE 1: Questão 3 - Listas Randômicas
# ==========================================================
print("--- TESTE Q3: Listas Randômicas ---")
for n in TAMANHOS_Q3:
    lista_base = gerar_lista_randomica(n)
    print(f"\nTestando N = {n}...")
    for nome, alg in ALGOS.items():
        try:
            tempo = medir_tempo(alg, lista_base)
            tempos_randomicos[nome].append(tempo)
            print(f"  {nome}: {tempo:.4f}s")
        except RecursionError:
            # Captura exceção para Quick/Merge Sort em caso de erro
            tempos_randomicos[nome].append(None)
            print(f"  {nome}: Erro (Recursão/Limite de tempo)")

# ==========================================================
# PLOTAGEM Q3
# ==========================================================
plt.figure(figsize=(12, 7))
for nome in NOMES:

    y_data = [t for t in tempos_randomicos[nome] if t is not None]
    x_data = [TAMANHOS_Q3[i] for i, t in enumerate(tempos_randomicos[nome]) if t is not None]
    
    if y_data:
        plt.plot(x_data, y_data, label=nome, marker='o')

plt.title("Tempo de Execução vs. Tamanho da Lista (Listas Randômicas)")
plt.xlabel("Tamanho da Lista (N)")
plt.ylabel("Tempo (Segundos)")
plt.legend(loc='upper left')
plt.grid(True)
plt.show()

# ==========================================================
# TESTE 2: Questão 4 - Lista Descendente (N=50000)
# ==========================================================
N_Q4 = 50000
lista_descendente = gerar_lista_descendente(N_Q4)
print("\n--- TESTE Q4: Lista Descendente (N=50000) ---")

for nome, alg in ALGOS.items():
    try:
        tempo = medir_tempo(alg, lista_descendente)
        tempos_descendentes.append(tempo)
        print(f"  {nome}: {tempo:.4f}s")
    except RecursionError:
        tempos_descendentes.append(0) 
        print(f"  {nome}: Erro (Recursão/Limite de tempo)")

# ==========================================================
# PLOTAGEM Q4
# ==========================================================
plt.figure(figsize=(10, 6))
plt.bar(NOMES, tempos_descendentes, color=['blue', 'blue', 'blue', 'blue', 'green', 'red'])
plt.title(f"Tempo de Execução em Lista Descendente (N={N_Q4})")
plt.xlabel("Algoritmo de Ordenação")
plt.ylabel("Tempo (Segundos)")
plt.grid(True, axis='y')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
