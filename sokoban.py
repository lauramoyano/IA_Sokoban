import sys


def listToString(s):  
    str1 = ""  
    for element in s:  
        str1 += element  
    return str1

def boxsLocationToString(array):
    string = ""
    for i in range(0,len(array)):
        string = string + "(" + str(array[i][0]) + "," + str(array[i][1]) + ")"
    return string

def readFile():
    file = open(sys.argv[1], 'r')
    Lines = file.readlines()
    rows = 0
    columns = 0
    counter = 0
    position = []
    boxs_location = []
    board = []

    for i in range(0,len(Lines)):
        Lines[i] = Lines[i].replace("\n","")

    for i in range(0,len(Lines)):
        if(Lines[i][0] == 'W' or Lines[i][0] == '0'):
            rows = rows + 1
            board.append(Lines[i])
        if(Lines[i][0] != 'W' and Lines[i][0] != '0' and counter != 0):
            boxs_location.append([int(Lines[i][0]), int(Lines[i][2])])
            print([int(Lines[i][0]), int(Lines[i][2])])
        if(Lines[i][0] != 'W' and Lines[i][0] != '0' and counter == 0):
            position.append(int(Lines[i][0]))
            position.append(int(Lines[i][2]))
            print([int(Lines[i][0]), int(Lines[i][2])])
            counter = counter + 1

    columns = len(Lines[0])

    return rows, columns, position, boxs_location, board

rows, columns, position, boxes_positions, board = readFile()
