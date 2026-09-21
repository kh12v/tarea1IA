import os
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
    return mapToUse, maps[mapToUse-1]

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
    map_index, original_map = setMap()
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
            
            # print(f"Turno: {turn + 1}")
            # print(mapToUse)
            turn += 1
            # input("Presione enter para ver el siguiente turno")
            
        stats["turns"] = turn
        print(f"Fin de la iteración {i + 1}. Escaparon: {stats['escaped']} | Murieron: {stats['died']} | Turnos: {turn}")
        all_stats.append(stats)
        
    total_escaped = sum(s["escaped"] for s in all_stats)
    total_died = sum(s["died"] for s in all_stats)
    
    # Cada iteración tiene exactamente 3 personas al inicio (config.py)
    total_initial = 3 * iterations
    survival_rate = (total_escaped / total_initial) * 100
    
    # Distribución del tiempo de los turnos
    turns_list = [s["turns"] for s in all_stats]
    mean_turns = np.mean(turns_list)
    std_turns = np.std(turns_list)
    min_turns = np.min(turns_list)
    max_turns = np.max(turns_list)
    
    print("\n--- Estadísticas Finales (Relevancia Estadística) ---")
    print(f"Total de iteraciones jugadas: {iterations}")
    print(f"Total personas que escaparon: {total_escaped} / {total_initial}")
    print(f"Total personas que murieron: {total_died} / {total_initial}")
    print(f"Tasa de supervivencia: {survival_rate:.2f}%")
    
    print("\n--- Distribución del Tiempo de Despeje (Turnos) ---")
    print(f"Media de turnos (Mean): {mean_turns:.2f}")
    print(f"Desviación estándar (Std Dev): {std_turns:.2f}")
    print(f"Mínimo de turnos (Min): {min_turns}")
    print(f"Máximo de turnos (Max): {max_turns}")
    
    # Save statistics to file
    map_names = {1: "highDensity", 2: "mediumDensity", 3: "lowDensity"}
    algo_names = {1: "dijkstra", 2: "bfs", 3: "a_star", 4: "greedy", 5: "genetic"}
    
    algo_name = algo_names.get(algo, "unknown_algo")
    map_name = map_names.get(map_index, "unknown_map")
    
    dir_path = os.path.join("data", algo_name)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, f"{map_name}.txt")
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("--- Estadísticas Finales (Relevancia Estadística) ---\n")
            f.write(f"Total de iteraciones jugadas: {iterations}\n")
            f.write(f"Total personas que escaparon: {total_escaped} / {total_initial}\n")
            f.write(f"Total personas que murieron: {total_died} / {total_initial}\n")
            f.write(f"Tasa de supervivencia: {survival_rate:.2f}%\n\n")
            f.write("--- Distribución del Tiempo de Despeje (Turnos) ---\n")
            f.write(f"Media de turnos (Mean): {mean_turns:.2f}\n")
            f.write(f"Desviación estándar (Std Dev): {std_turns:.2f}\n")
            f.write(f"Mínimo de turnos (Min): {min_turns}\n")
            f.write(f"Máximo de turnos (Max): {max_turns}\n")
        print(f"\nEstadísticas guardadas exitosamente en: {file_path}")
    except Exception as e:
        print(f"\nError al guardar las estadisticas: {e}")

if __name__ == "__main__":
    main()