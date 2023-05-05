from collections import deque

def boxsLocationsToString(array):
    string = ""
    for i in range(0, len(array)):
        string = string + "(" + str(array[i][0]) + "," + str(array[i][1]) + ")"
    return string

# Búsqueda preferente por amplitud
def BFS(initialState):
    # Creamos una cola para almacenar los nodos a evaluar
    queue = deque()
    queue.append(initialState)
    visited = set()
    while queue:
        # Obtenemos el primer nodo a evaluar
        currentState = queue.popleft()

        # Añadimos la posición actual del personaje y de las cajas a un conjunto
        # de nodos visitados, para luego evitar bucles
        visited.add(str(currentState.position[0]) + "," + str(
            currentState.position[1]) + boxsLocationsToString(currentState.box_locations))

        # Verificamos si la depth del nodo es mayor a 64, si es así, no evaluamos el nodo y
        # continuamos con los siguientes de la cola
        if (currentState.depth > 64):
            continue

        # Verificamos si en el estado actual se ha perdido la partida, si es así,
        # no evaluamos el nodo y continuamos con los siguientes de la cola
        if (currentState.lostGame()):
            continue

        else:
            # Verificamos si el nodo actual es solución, si es así, terminamos el ciclo
            if (currentState.finishedGame()):
                break

            # Realizamos las posibles acciones del nodo actual y agregamos los nuevos
            # nodos que no se han visitado, a la cola
            movements = currentState.correctMovements()
            for movement in movements:
                tempState = currentState.updateState(movement)

                # Verificamos si el nodo actual se ha visitado, si es así,
                # continuamos con los siguientes de la cola
                if (str(tempState.position[0]) + "," + str(tempState.position[1]) + boxsLocationsToString(tempState.box_locations) in visited):
                    continue
                else:
                    queue.append(tempState)
    return currentState

# Búsqueda preferente por profundidad
def DFS(initialState):
    stack = deque([initialState])
    visited = set()
    while stack:
        currentState = stack.pop()
        if (currentState.depth > 64):
            continue
        visited.add(str(currentState.position[0]) + "," + str(
            currentState.position[1]) + boxsLocationsToString(currentState.box_locations))
        if (currentState.lostGame()):
            continue
        else:
            if (currentState.finishedGame()):
                break
            movements = currentState.correctMovements()
            movements.reverse()
            for movement in movements:
                tempState = currentState.updateState(movement)
                if (str(tempState.position[0]) + "," + str(tempState.position[1]) + boxsLocationsToString(tempState.box_locations) in visited):
                    continue
                else:
                    stack.append(tempState)
    return currentState

# Búsqueda preferente por profundidad iterativa
def IDFS(initialState, limite):
    stack = deque()
    stack.append(initialState)
    visited = set()
    depth = 0
    while stack:
        currentState = stack.pop()
        if (currentState.depth == limite):
            return currentState
        if (currentState.depth > 64):
            continue
        visited.add(str(currentState.position[0]) + "," + str(
            currentState.position[1]) + boxsLocationsToString(currentState.box_locations))
        if (currentState.lostGame()):
            continue
        else:
            if (currentState.finishedGame()):
                break
            movements = currentState.correctMovements()
            movements.reverse()
            for movement in movements:
                tempState = currentState.updateState(movement)
                if (str(tempState.position[0]) + "," + str(tempState.position[1]) + boxsLocationsToString(tempState.box_locations) in visited):
                    continue
                else:
                    stack.append(tempState)
    return currentState


def executeIDFS(initialState):
    limit = 10
    solution = False
    while (not solution):
        temp_solution = IDFS(initialState, limit)
        if (temp_solution.finishedGame()):
            solution = True
            return temp_solution
        else:
            limit = limit + 1