import sys
from algoritmos import BFS, DFS, executeIDFS

def listToString(s):
    str1 = ""
    for element in s:
        str1 += element
    return str1

# leer el archivo y definir en board las filas, columnas, paredes y positiones de las cajas
def readFile():
    file = open(sys.argv[1], 'r')
    Lines = file.readlines()
    rows = 0
    columns = 0
    counter = 0
    position = []
    box_locations = []
    board = []

    for i in range(0, len(Lines)):
        Lines[i] = Lines[i].replace("\n", "")

    for i in range(0, len(Lines)):
        if (Lines[i][0] == 'W' or Lines[i][0] == '0'):
            rows = rows + 1
            board.append(Lines[i])
        if (Lines[i][0] != 'W' and Lines[i][0] != '0' and counter != 0):
            box_locations.append([int(Lines[i][0]), int(Lines[i][2])])
            counter += 1
        if (Lines[i][0] != 'W' and Lines[i][0] != '0' and counter == 0):
            position.append(int(Lines[i][0]))
            position.append(int(Lines[i][2]))
            counter += 1

    columns = len(Lines[0])

    return rows, columns, position, box_locations, board

# esta clase nos permite identificar el estado actual de juego. Por lo que nos ayudará a identificar los nodos de nuestros árboles de búsqueda
class State:
    def __init__(self, rows, columns, position, box_locations,
                 board, actions, depth):
        self.rows = rows
        self.columns = columns
        self.position = position
        self.box_locations = box_locations
        self.board = board
        self.actions = actions
        self.final_positions = self.boxsDestination()
        self.depth = depth

    def printBoard(self):
        for row in board:
            print(f"{row}\n")

    # guardamos en un array las positiones finales de donde deberían estar las cajas "X"
    def boxsDestination(self):
        final_positions = []
        # recorremos el tablero por filas y columnas
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                if (self.board[i][j] == 'X'):
                    final_positions.append([i, j])
        return final_positions

    # evaluamos si el estado actual es solución
    def finishedGame(self):
        state = True
        for i in range(0, len(self.final_positions)):
            # se evalua si las positiones de destino corresponden a las positiones de las cajas
            if (self.final_positions[i] in self.box_locations):
                continue
            else:
                state = False
        return state

    # evalua que movements se pueden hacer dependiendo a la position del agente y de las cajas
    def correctMovements(self):
        # se almacenan los movements que puede hacer el agente
        movement = []
        # si arriba no hay una pared entonces suba
        if (self.board[self.position[0]-1][self.position[1]] != 'W'):
            movement.append('U')

        # si abajo no hay una pared entonces baje
        if (self.board[self.position[0]+1][self.position[1]] != 'W'):
            movement.append('D')

        # si a la izquierda no hay una pared entonces mueva izquierda
        if (self.board[self.position[0]][self.position[1]-1] != 'W'):
            movement.append('L')

        # si a la derecha no hay una pared entonces mueva derecha
        if (self.board[self.position[0]][self.position[1]+1] != 'W'):
            movement.append('R')

        # movements que no puede hacer (recordemos que no se puede mover dos cajas a la vez):

        # si arriba hay una caja y arriba de esa caja hay una pared o hay otra caja, no puede ir arriba
        if ([self.position[0]-1, self.position[1]] in self.box_locations
            and (self.board[self.position[0]-2][self.position[1]] == 'W'
                 or [self.position[0]-2, self.position[1]] in self.box_locations)):
            movement.remove('U')

        # si abajo hay una caja y además abajo de esa caja hay una pared o hay otra caja, no puede ir abajo
        if ([self.position[0]+1, self.position[1]] in self.box_locations
            and (self.board[self.position[0]+2][self.position[1]] == 'W'
                 or [self.position[0]+2, self.position[1]] in self.box_locations)):
            movement.remove('D')

        # si a la izquierda hay una caja
        # y además a la izquierda de esa caja hay una pared o hay otra caja, no puede ir a la izq
        if ([self.position[0], self.position[1]-1] in self.box_locations
            and (self.board[self.position[0]][self.position[1]-2] == 'W'
                 or [self.position[0], self.position[1]-2] in self.box_locations)):
            movement.remove('L')

        # si a la derecha hay una caja
        # y además a la derecha de esa caja hay una pared o hay otra caja, no puede ir a la derecha
        if ([self.position[0], self.position[1]+1] in self.box_locations
            and (self.board[self.position[0]][self.position[1]+2] == 'W'
                 or [self.position[0], self.position[1]+2] in self.box_locations)):
            movement.remove('R')

        return movement

    # recibe el estado actual del juego y retorna true en caso de que haya perdido
    # o false en caso deque todavía pueda jugar
    def lostGame(self):

        # este for itera sobre todas las cajas
        for i in range(0, len(self.box_locations)):
            # Si la caja tiene  a la derecha y abajo una pared perdió
            if (self.board[self.box_locations[i][0]][self.box_locations[i][1]+1] == 'W'
               and self.board[self.box_locations[i][0]+1][self.box_locations[i][1]] == 'W'):
                return True

            # Si la caja tiene  a la izquierda y abajo una pared perdió
            elif (self.board[self.box_locations[i][0]][self.box_locations[i][1]-1] == 'W'
                  and self.board[self.box_locations[i][0]+1][self.box_locations[i][1]] == 'W'):
                return True

            # Si la caja tiene  a la izquierda y arriba una pared perdió
            elif (self.board[self.box_locations[i][0]][self.box_locations[i][1]-1] == 'W'
                  and self.board[self.box_locations[i][0]-1][self.box_locations[i][1]] == 'W'):
                return True

            # Si la caja tiene  a la derecha y arriba una pared perdió
            elif (self.board[self.box_locations[i][0]][self.box_locations[i][1]+1] == 'W'
                  and self.board[self.box_locations[i][0]-1][self.box_locations[i][1]] == 'W'):
                return True

            # Si la caja tiene  a la derecha una "pared" o "caja",
            # y adicional abajo tiene una "pared" o " caja", y
            # adicional tiene en la diagonal de abajo a la derecha una "pared" o "caja", perdió
            elif ((self.board[self.box_locations[i][0]][self.box_locations[i][1]+1] == 'W'
                   or [self.box_locations[i][0], self.box_locations[i][1]+1] in self.box_locations)
                  and (self.board[self.box_locations[i][0]+1][self.box_locations[i][1]] == 'W'
                       or [self.box_locations[i][0]+1, self.box_locations[i][1]] in self.box_locations)
                  and (self.board[self.box_locations[i][0]+1][self.box_locations[i][1]+1] == 'W'
                       or [self.box_locations[i][0]+1, self.box_locations[i][1]+1] in self.box_locations)):
                return True

            # Si la caja tiene  a la derecha una "pared" o "caja",
            # y adicional arriba tiene una "pared" o " caja", y
            # adicional tiene en la diagonal de arriba a la derecha una "pared" o "caja", perdió
            elif ((self.board[self.box_locations[i][0]][self.box_locations[i][1]+1] == 'W'
                   or [self.box_locations[i][0], self.box_locations[i][1]+1] in self.box_locations)
                  and (self.board[self.box_locations[i][0]-1][self.box_locations[i][1]] == 'W'
                       or [self.box_locations[i][0]-1, self.box_locations[i][1]] in self.box_locations)
                  and (self.board[self.box_locations[i][0]-1][self.box_locations[i][1]+1] == 'W'
                       or [self.box_locations[i][0]-1, self.box_locations[i][1]+1] in self.box_locations)):
                return True

            # Si la caja tiene  a la izquierda una "pared" o "caja",
            # y adicional arriba tiene una "pared" o " caja", y
            # adicional tiene en la diagonal de arriba a la izquierda una "pared" o "caja", perdió
            elif ((self.board[self.box_locations[i][0]][self.box_locations[i][1]-1] == 'W'
                   or [self.box_locations[i][0], self.box_locations[i][1]-1] in self.box_locations)
                  and (self.board[self.box_locations[i][0]-1][self.box_locations[i][1]] == 'W'
                       or [self.box_locations[i][0]-1, self.box_locations[i][1]] in self.box_locations)
                  and (self.board[self.box_locations[i][0]-1][self.box_locations[i][1]-1] == 'W'
                       or [self.box_locations[i][0]-1, self.box_locations[i][1]-1] in self.box_locations)):
                return True

            # Si la caja tiene  a la izquierda una "pared" o "caja",
            # y adicional abajo tiene una "pared" o " caja", y
            # adicional tiene en la diagonal de abajo a la izquierda una "pared" o "caja", perdió
            elif ((self.board[self.box_locations[i][0]][self.box_locations[i][1]-1] == 'W'
                   or [self.box_locations[i][0], self.box_locations[i][1]-1] in self.box_locations)
                  and (self.board[self.box_locations[i][0]+1][self.box_locations[i][1]] == 'W'
                       or [self.box_locations[i][0]+1, self.box_locations[i][1]] in self.box_locations)
                  and (self.board[self.box_locations[i][0]+1][self.box_locations[i][1]-1] == 'W'
                       or [self.box_locations[i][0]+1, self.box_locations[i][1]-1] in self.box_locations)):
                return True
            else:
                return False

    # método para cambiar el estado dada una acción
    def updateState(self, movement):
        # se cambia la position actual a [position_x - 1, position_y] para ir arriba
        if (movement == 'U'):
            new_position_agent = [self.position[0]-1, self.position[1]]
            new_position_boxes = self.box_locations.copy()
            # si la position actual del agente corresponde a la position de alguna caja
            if (new_position_agent in new_position_boxes):
                # iteramos las cajas
                for i in range(0, len(new_position_boxes)):
                    # se busca la position de la caja que corresponda a la nueva position del agente
                    if (new_position_boxes[i] == new_position_agent):
                        # modificamos la position actual de la caja para  arriba
                        new_position_boxes[i] = [
                            new_position_agent[0]-1, new_position_agent[1]]
            newactions = self.actions.copy()
            newactions.append('U')
            # se retorna el estado actual con este movement
            return State(self.rows, self.columns, new_position_agent, new_position_boxes, self.board, newactions, self.depth + 1)

        # se cambia la position actual a [position_x + 1, position_y] para ir abajo
        elif (movement == 'D'):
            new_position_agent = [self.position[0]+1, self.position[1]]
            new_position_boxes = self.box_locations.copy()
            # si la position actual del agente corresponde a la position de alguna caja
            if (new_position_agent in new_position_boxes):
                # iteramos las cajas
                for i in range(0, len(new_position_boxes)):
                    # se busca la position de la caja que corresponda a la nueva position del agente
                    if (new_position_boxes[i] == new_position_agent):
                        # modificamos la position actual de la caja para abajo
                        new_position_boxes[i] = [
                            new_position_agent[0]+1, new_position_agent[1]]
            newactions = self.actions.copy()
            newactions.append('D')
            # se retorna el estado actual con este movement
            return State(self.rows, self.columns, new_position_agent, new_position_boxes, self.board, newactions, self.depth + 1)

        # se cambia la position actual a [position_x, position_y - 1] para ir a la izquierda
        elif (movement == 'L'):
            new_position_agent = [self.position[0], self.position[1]-1]
            new_position_boxes = self.box_locations.copy()
            # si la position actual del agente corresponde a la position de alguna caja
            if (new_position_agent in new_position_boxes):
                # iteramos las cajas
                for i in range(0, len(new_position_boxes)):
                    # se busca la position de la caja que corresponda a la nueva position del agente
                    if (new_position_boxes[i] == new_position_agent):
                        # se modifica la position actual de la caja para  la izquierda
                        new_position_boxes[i] = [
                            new_position_agent[0], new_position_agent[1]-1]
            newactions = self.actions.copy()
            newactions.append('L')
            # se retorna el estado actual con este movement
            return State(self.rows, self.columns, new_position_agent, new_position_boxes, self.board, newactions, self.depth + 1)

        # se cambia la position actual a [position_x, position_y + 1] para ir a la derecha
        elif (movement == 'R'):
            new_position_agent = [self.position[0], self.position[1]+1]
            new_position_boxes = self.box_locations.copy()
            # si la position actual del agente corresponde a la position de alguna caja
            if (new_position_agent in new_position_boxes):
                # iteramos las cajas
                for i in range(0, len(new_position_boxes)):
                    # se busca la position de la caja que corresponda a la nueva position del agente
                    if (new_position_boxes[i] == new_position_agent):
                        # se modifica la position actual de la caja para la derecha
                        new_position_boxes[i] = [
                            new_position_agent[0], new_position_agent[1]+1]
            newactions = self.actions.copy()
            newactions.append('R')
            # se retorna el estado actual con este movement
            return State(self.rows, self.columns, new_position_agent, new_position_boxes, self.board, newactions, self.depth + 1,)


rows, columns, position, boxes_positions, board = readFile()

# Estado inicial con los datos obtenidos del nivel seleccionado
initialState = State(rows, columns, position, boxes_positions, board, [], 0)

# Salida
output = listToString(DFS(initialState).actions) + "\n" + listToString(BFS(initialState).actions) + \
    "\n" + \
    listToString(executeIDFS(initialState).actions)

print(output)
