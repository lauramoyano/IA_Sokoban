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

# La función DFS Busqueda preferente por profundidad
def DFS(initialState):
    # Se crea una pila (stack) con el estado inicial.
    stack = deque([initialState])
    # Se crea un conjunto (visited) para almacenar los estados que ya se han visitado.
    visited = set()
    # Se inicia un ciclo while que se repetirá mientras la pila tenga elementos.
    while stack:
        # Se saca el último elemento de la pila y se asigna a currentState.
        currentState = stack.pop()
        # Si el estado actual tiene una profundidad mayor a 64, se omite y se continúa con el ciclo.
        if (currentState.depth > 64):
            continue
        # Se agrega el estado actual al conjunto visited.
        visited.add(str(currentState.position[0]) + "," + str(
            currentState.position[1]) + boxsLocationsToString(currentState.box_locations))
        # Si el estado actual indica que se ha perdido el juego, se omite y se continúa con el ciclo.
        if (currentState.lostGame()):
            continue
        # Si el estado actual indica que se ha terminado el juego, se rompe el ciclo while.
        else:
            if (currentState.finishedGame()):
                break
            # Se obtienen los movimientos correctos a partir del estado actual y se invierten.
            movements = currentState.correctMovements()
            movements.reverse()
            # Se itera sobre los movimientos obtenidos.
            for movement in movements:
                # Se actualiza el estado actual con el movimiento correspondiente.
                tempState = currentState.updateState(movement)
                # Si el nuevo estado ya ha sido visitado, se omite y se continúa con el ciclo for.
                if (str(tempState.position[0]) + "," + str(tempState.position[1]) + boxsLocationsToString(tempState.box_locations) in visited):
                    continue
                # Si el nuevo estado no ha sido visitado, se agrega a la pila stack.
                else:
                     stack.append(tempState)
    return currentState

# Búsqueda preferente por profundidad iterativa
def IDFS(initialState, limit):
    stack = deque()
    stack.append(initialState)
    visited = set()
    while stack:
        currentState = stack.pop()
        # si se llego al limite y todaía no hay nodos por evaluar, continua
        if (currentState.depth == (limit+1)):
            continue
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

#búsqueda preferente profundidad iterativa (IDFS) 
# para encontrar una solución para un problema a partir de un estado inicial
def executeIDFS(initialState):
    # el nivel incial es 10
    limit = 10
    solution = False
    #Esta línea inicializa la variable solution con un valor booleano de False 
    # Esta variable será utilizada para controlar si se ha encontrado una solución
    while (not solution):
        #En cada iteración del bucle, se llama IDFS con  initialState 
        # y limit y se almacena el resultado en la variable temp_solution. 
        # La función IDFS realiza una búsqueda en profundidad limitada a la profundidad dada por limit.
        temp_solution = IDFS(initialState, limit)
        if (temp_solution.finishedGame()):
            solution = True
            return temp_solution
        else:
            #La profundidad va aumentar de 1 en 1
            limit = limit + 1