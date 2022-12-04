import math


def getData():
    with open("exemplaires/10_20_0.txt") as f:
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

def isMunicipalityValid(circonscriptionArray, newMinicipality, manhathanLimit):
    isValid = True
    for i in circonscriptionArray:
            if calculate_manhattan_distance(i, newMinicipality) > manhathanLimit:
                isValid = False
                break

    return isValid

l, h, matrix  = getData()

nbMuni = l*h #n
nbCircon = 10 #m


manhathanLimit = math.ceil(nbMuni/(2*nbCircon))
print("manhathanLimit")
print(manhathanLimit)
print("manhathanLimit")

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

        #Circonscription is full, push it in configurations
        if len(temp_circonscription) == circonscriptionSize:
            configurations.append(temp_circonscription)
            temp_circonscription = []

test_point1 = {
                "x": 9,
                "y": 0,
                "votes": 39
            }

test_point2 = {
                "x": 1,
                "y": 1,
                "votes": 49
            }
print(calculate_manhattan_distance(test_point1, test_point2))

print("Manhathan limit: ", manhathanLimit)
print("Circonscription size: ", circonscriptionSize)
print("Configurations: ")

index = 0
for i in range(h):
    print("configuration:", index)
    index = index + 1
    for j in range(l):
        print(configurations[i][j]["votes"])
        



# print(l)
# print(h)
# print(matrix)