import math


def getData():
    with open("exemplaires/5_10_0.txt") as f:
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

        print(matrix)
        return l, h, matrix

def getVotes(matrix, h, l):
    votesVerts = 0
    votesJaunes = 0
    for i in range(0, h):
        for j in range(0, l):
            if matrix[i][j] > 50 :
                votesVerts = votesVerts + 1
            else:
                votesJaunes = votesJaunes + 1
    return votesVerts, votesJaunes

def calculate_manhattan_distance(point1, point2) :     
    return sum(abs(value1 - value2) for value1, value2 in zip(point1, point2))
    # point 1 = [1,3]


#MAIN

l, h, matrix  = getData()

nbMuni = l*h #n
nbCircon = 5 #m

votesVerts, votesJaunes = getVotes(matrix, h, l)

k_min = math.floor(nbMuni/nbCircon)
k_max = math.ceil(nbMuni/nbCircon)

# minWinsParCirconscriptions = nbMuni/nbCircon 

#For i in range(k)
#votes verts/k > .5

dist = math.ceil(nbMuni/(2*nbCircon))

#aller chercher le minimum de vote possible right away
#ensuite complet la circonscription avec des blancs




print(l)
print(h)
print(matrix)
print(votesVerts)
print(votesJaunes)