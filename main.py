import math
import argparse

import sys
sys.stdout.flush()

parser = argparse.ArgumentParser()

parser.add_argument('-e', action='store', const='NoValue', nargs='?')
parser.add_argument('-c', action='store', const='NoValue', nargs='?')
parser.add_argument('-p', action='store', const='NoValue', nargs='?')

args = parser.parse_args()

def getArguments():
    try:
        if args.e:
            filePath = args.e
        if args.c:
            nbCirconscription = args.c
        if args.p:
            print = True
        else:
            print = False
        return filePath, nbCirconscription, print
    except:
        print("Missing arguments.")
        return "exemplaires/10_20_0.txt", 10


def getData(filePath):
    # "exemplaires/10_20_0.txt"
    with open(filePath) as f:
        lines = f.readlines()
        matrix = []
        i=0
        l = 0
        h = 0
        for line in lines:
            lineSplit = line.split(" ")
            cleanLine = list(filter(None, lineSplit))
            if(i==0):
                l = int(cleanLine[0])
                h = int(cleanLine[1].replace("/n", ""))
            else:
                cleanLine.pop()
                tempArray = []
                for i in range(0, len(cleanLine)):
                    cleanLine[i] = int(cleanLine[i])
                    tempArray.append(cleanLine[i])
                matrix.append(tempArray)
            i = i+1
        return l, h, matrix

def calculate_manhattan_distance(municipality1, municipality2) :
    return (abs(municipality2["x"] - municipality1["x"]) + abs(municipality2["y"] - municipality1["y"]))
    # point 1 = [1,3]

def getManhathanValue(n, m):
    return math.ceil(n/(2*m))

# Trouver si l'ajout d'une municipalite est valide dependamment de la distance de manhathan
def isMunicipalityValid(circonscriptionArray, newMinicipality, manhathanLimit):
    isValid = True
    for i in circonscriptionArray:
            if calculate_manhattan_distance(i, newMinicipality) > manhathanLimit:
                isValid = False
                break
    return isValid
    
# Initialiser les variables necessaires au probleme 
filePath, nbCirconscription, printArg = getArguments()

l, h, matrix  = getData(filePath)

nbMuni = int(l*h) #n
nbCircon = int(nbCirconscription) #m

manhathanLimit = math.ceil(nbMuni/(2*nbCircon))

k_min = math.floor(nbMuni/nbCircon)
k_max = math.ceil(nbMuni/nbCircon)

circonscriptionSize = k_min

configurations = []
temp_circonscription = []

for i in range(h):
    for j in range(l):
        new_point = {
                "x": j,
                "y": i,
                "votes": matrix[i][j]
            }

        if len(temp_circonscription) == 0:
            temp_circonscription.append(new_point)
        else:
            if isMunicipalityValid(temp_circonscription, new_point, manhathanLimit):
                temp_circonscription.append(new_point)

        # Si la circonscription est plein, on l'ajoute au tableau 
        if len(temp_circonscription) == circonscriptionSize:
            configurations.append(temp_circonscription)
            temp_circonscription = []

votesArray = []
index = 0

# Creer tableau du nombre de votes par circonscription
for i in range(len(configurations)) :
    index = index + 1
    votes = 0
    for j in range(len(configurations[i])) :
        votes += configurations[i][j]["votes"]
    votesArray.append(votes)

minVotesToWin = nbMuni / nbCircon * 50 + 1

# Trouver le nombre de circonscriptions qu'on gagne initialement
nbCirconWon = 0
for votes in votesArray :
    if votes >= minVotesToWin :
        nbCirconWon += 1


def printConfig() :
    for i in range(len(configurations)) :
        string = ''
        for j in range(len(configurations[i])) :
            string = string + str(configurations[i][j]["x"]) + ' ' + str(configurations[i][j]["y"]) + ' '
        
        print(string, flush=True)
    print(' ', flush=True)

# Aller chercher la meilleure configuration
for k in range(len(configurations)) :
    for l in range(len(configurations)) :
        if k != l :
            #K < l, Ils sont < 1001, K donne a L
            #K < l: veut dire quon verification avant
            if votesArray[k] < votesArray[l]:
                if votesArray[l] < minVotesToWin and votesArray[k] < minVotesToWin :
                    for i in range(len(configurations[k])) :
                        for j in range(len(configurations[l])) :
                            if configurations[k][i]["votes"] > configurations[l][j]["votes"] and votesArray[l] < minVotesToWin :
                                if isMunicipalityValid(configurations[k], configurations[l][j], manhathanLimit) and isMunicipalityValid(configurations[l], configurations[k][i], manhathanLimit) :
                                    
                                    temp = configurations[k][i]
                                    configurations[k][i] = configurations[l][j]
                                    configurations[l][j] = temp

                                    votes = 0
                                    for j in range(len(configurations[k])) :
                                        votes += configurations[k][j]["votes"]

                                    votesArray[k] = votes
                                    
                                    votes = 0
                                    for j in range(len(configurations[l])) :
                                        votes += configurations[l][j]["votes"]

                                    votesArray[l] = votes

                                    newNbCirconWon = 0
                                    for votes in votesArray :
                                        if votes >= minVotesToWin : 
                                            newNbCirconWon += 1

                                    if printArg :
                                        if nbCirconWon < newNbCirconWon :
                                            printConfig()
                                            nbCirconWon = newNbCirconWon
            else :
                if votesArray[k] > minVotesToWin and votesArray[l] < minVotesToWin:
                    for i in range(len(configurations[k])) :
                        for j in range(len(configurations[l])) :
                            if configurations[k][i]["votes"] > configurations[l][j]["votes"] and votesArray[l] < minVotesToWin and votesArray[k] >= minVotesToWin :
                                if isMunicipalityValid(configurations[k], configurations[l][j], manhathanLimit) and isMunicipalityValid(configurations[l], configurations[k][i], manhathanLimit) :
                                    
                                    temp = configurations[k][i]
                                    configurations[k][i] = configurations[l][j]
                                    configurations[l][j] = temp

                                    votes = 0
                                    for j in range(len(configurations[k])) :
                                        votes += configurations[k][j]["votes"]

                                    votesArray[k] = votes
                                    
                                    votes = 0
                                    for j in range(len(configurations[l])) :
                                        votes += configurations[l][j]["votes"]

                                    votesArray[l] = votes

                                    newNbCirconWon = 0
                                    for votes in votesArray :
                                        if votes >= minVotesToWin : 
                                            newNbCirconWon += 1

                                    if printArg :
                                        if nbCirconWon < newNbCirconWon :
                                            printConfig()
                                            nbCirconWon = newNbCirconWon



# if printArg:
#     displayArray = []
# 
#     for i in range(20):
#         row = []
#         for j in range(10):
#             row.append(0)
#         displayArray.append(row)    
# 
# 
#     for i in range(len(configurations)) :
#         for j in range(len(configurations[i])) :
#             y = int(configurations[i][j]["y"])
#             x = int(configurations[i][j]["x"])
#             displayArray[y][x] = i
# 
# 
#     for row in displayArray :
#         print(row)
