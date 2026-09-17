import numpy as np
from config import NUM_FIRE_TURNS
from algorithms import algoIteration
from config import maps

def setMap():
    print("Seleccione el mapa:")
    print("1. Alta densidad")
    print("2. Media densidad")
    print("3. Baja densidad")
    mapToUse = -1
    while mapToUse < 1 or mapToUse > 3:
        try:
            mapToUse = int(input("Ingrese el numero del mapa: "))
            if (mapToUse not in [1, 2, 3]):
                print("Ingrese una opción válida")
        except ValueError:
            print("Error: El valor ingresado debe ser un numero")
    return maps[mapToUse-1]

def setIterations():
    iterations = -1
    while iterations < 1 or iterations > 200:
        try:
            iterations = int(input("Ingrese la cantidad de iteraciones [1, 200] ideal 80 mínimo: "))
            if (iterations < 1 or iterations > 200):
                print("Ingrese un valor válido")
        except ValueError:
            print("Error: El valor ingresado debe ser un numero")
    return iterations

def setAlgo():
    print("Seleccione el algoritmo:")
    print("1. Dijkstra")
    print("2. BFS")
    print("3. A*")
    print("4. Greedy Best-First Search")
    print("5. Algoritmo genético")
    algoToUse = -1
    while algoToUse < 1 or algoToUse > 5:
        try:
            algoToUse = int(input("Ingrese el numero del algoritmo: "))
            if (algoToUse not in [1, 2, 3, 4, 5]):
                print("Ingrese una opción válida")
        except ValueError:
            print("Error: El valor ingresado debe ser un numero")
    return algoToUse

def spreadFire(mapToUse: np.ndarray, stats: dict):
    mapWithFire = np.copy(mapToUse)
    rows, cols = mapToUse.shape
    for i in range(rows):
        for j in range(cols):
            if (mapToUse[i, j] == '*'):
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + dr, j + dc
                    if 0 <= ni < rows and 0 <= nj < cols:
                        if mapToUse[ni, nj] != '#' and mapToUse[ni, nj] != '*':
                            if mapToUse[ni, nj] in ['1', '2', '3'] and mapWithFire[ni, nj] != '*':
                                stats["died"] += int(mapToUse[ni, nj])
                            mapWithFire[ni, nj] = '*'
    return mapWithFire

def main():
    original_map = setMap()
    iterations = setIterations()
    algo = setAlgo()
    print("Mapa seleccionado:\n", original_map)
    print("Iteraciones: ", iterations)
    print("Algoritmo: ", algo)

    all_stats = []

    print("\nResultados:")
    for i in range(iterations):
        mapToUse = np.copy(original_map)
        stats = {"escaped": 0, "died": 0}
        turn = 0
        
        print(f"\n--- Iniciando Simulación (Iteración {i + 1}) ---")
        
        while True:
            # Verificar si quedan personas en el mapa
            people_left = np.any(np.isin(mapToUse, ['1', '2', '3']))
            if not people_left:
                break
                
            if (turn % NUM_FIRE_TURNS == 0 and turn > 0):
                mapToUse = spreadFire(mapToUse, stats)
            mapToUse = algoIteration(algo, mapToUse, stats)
            
            print(f"Turno: {turn + 1}")
            print(mapToUse)
            turn += 1
            input("Presione enter para ver el siguiente turno")
            
        print(f"Fin de la iteración {i + 1}. Escaparon: {stats['escaped']} | Murieron: {stats['died']}")
        all_stats.append(stats)
        
    total_escaped = sum(s["escaped"] for s in all_stats)
    total_died = sum(s["died"] for s in all_stats)
    
    print("\n--- Estadísticas Finales ---")
    print(f"Total de iteraciones jugadas: {iterations}")
    print(f"Total personas que escaparon: {total_escaped}")
    print(f"Total personas que murieron: {total_died}")

if __name__ == "__main__":
    main()