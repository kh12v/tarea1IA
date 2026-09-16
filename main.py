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
    while iterations < 80 or iterations > 200:
        try:
            iterations = int(input("Ingrese la cantidad de iteraciones [80, 200]: "))
            if (iterations < 80 or iterations > 200):
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
    mapToUse = setMap()
    iterations = setIterations()
    algo = setAlgo()
    print("Mapa seleccionado: ", mapToUse)
    print("Iteraciones: ", iterations)
    print("Algoritmo: ", algo)

    print("\nMapa inicial:")
    print(mapToUse)

    stats = {"escaped": 0, "died": 0}

    print("\nResultados:")
    for i in range(iterations):
        if (i % NUM_FIRE_TURNS == 0):
            mapToUse = spreadFire(mapToUse, stats)
        mapToUse = algoIteration(algo, mapToUse, stats)
        print("Iteracion: ", i + 1)
        print(mapToUse)
        print(f"Escaparon: {stats['escaped']} | Murieron: {stats['died']}")
        
    print("\n--- Estadísticas Finales ---")
    print(f"Total personas que escaparon: {stats['escaped']}")
    print(f"Total personas que murieron: {stats['died']}")

if __name__ == "__main__":
    main()