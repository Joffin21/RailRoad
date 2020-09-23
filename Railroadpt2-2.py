#from math import pi , acos , sin , cos
## HOW DO I UPDATE MY TKINTER  OMGGGG

from math import *
import sys, time
from Tkinter import*#Tk, Canvas
import Queue
from heapq import heappop, heappush

city1 = "Seattle"#sys.argv[1]
city2 = "Miami"#sys.argv[2]

#methods
def calcd(y1,x1, y2,x2):
    y1  = float(y1)
    #print(y1)
    x1  = float(x1)
    #print(x1)
    y2  = float(y2)
    #print(y2)
    x2  = float(x2)
    #print(x2)
    radius = 3959 # miles = 6371 km
    y1 *= pi/180.0
    x1 *= pi/180.0
    y2 *= pi/180.0
    x2 *= pi/180.0
    num1 = sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1)
    if(num1 > 1.0):
       num = acos(round(num1))
    else:
       num = acos(num1)
    return num * radius

#--------------So everything commented out here just decides whether its USA
#--------------or Romania, but for part 1 just do Romania

# if country == "USA":
locations = open("rrNodes.txt", "r")
Edges = open("rrEdges.txt", "r")
CityNames = open("rrNodeCity.txt", "r")

startTime = time.clock()
nodesGraph = {} #Key is ID &&& Value is tuple with (latitude, longtitude)

#----------------This is to make the dictionary for the cities & locations-------------#

listOfNodes = locations.readlines() #taking in each line and putting it into a list
l = []
for line in listOfNodes: #for each line in the list
    indivNodes = line.split()
    ID = indivNodes[0]
    l.append(ID)
    latitude = indivNodes[1]
    longtitude = indivNodes[2]
    nodesGraph[ID] = (latitude, longtitude)


#--------------------This is to make the dictionary for the edges----------------------#

edgeGraph = {} #graph of IDs that have edges between them (i.e pair would be --> (ID: [neighbor1, neighbor2, neighborEtc]))

#txtFileEdges = open("romEdges.txt", "r")
listofEdges = Edges.readlines()
for lines in listofEdges:
    indivEdges = lines.split()
    edge1 = (indivEdges[0])
    edge2 = (indivEdges[1])
    if edge1 not in edgeGraph:
        edgeGraph[edge1] = [edge2]
    else:
        edgeGraph[edge1].append(edge2)
    if edge2 not in edgeGraph:
        edgeGraph[edge2] = [edge1]
    else:
        edgeGraph[edge2].append(edge1)
#edgeGraph adjacency list made

#------------------This is to make the dictionary for the actual city names--------------------#

namesLookup = {}
#txtFileNames = open("romFullNames.txt", "r")

theCityNames = CityNames.readlines()
for line in theCityNames:
    indvNames = line.split()
    namesLookup[indvNames[1]] = indvNames[0]

#--------------------This is to make the shortest path into a list----------------------#

def findpath(dictionary, end, start):
    parent = dictionary.get(end)
    array = []
    array.append(end)
    array.append(parent)
    while parent != start:
        #print(parent)
        parent = dictionary.get(parent)
        array.append(parent)
    length = len(array)-1
    array = array[::-1]
    print("Distance Traveled: " + str(distanceTraveled(array)) + " miles")
    #return length-1
    #print("The number of cities: " + str(length))
    return(array)

#-----------------------------Find the distance traveled-------------------------------#

def distanceTraveled(array):
    sumOfDistances = 0
    sumOfDistancesKilo = 0
    for x in range(0,len(array)-2):
        c1 = array[x]
        c2 = array[x+1]
        coor1Lat = nodesGraph[c1][0]
        coor1Long = nodesGraph[c1][1]
        coor2Lat = nodesGraph[c2][0]
        coor2Long = nodesGraph[c2][1]
        sumOfDistances = sumOfDistances + calcd(coor1Lat, coor1Long, coor2Lat, coor2Long)
    #sumOfDistancesKilo = int(sumOfDistancesKilo)
    return sumOfDistances


#--------------------All of this is for the aStar stuff--------------------------------#

city1ID = namesLookup.get(city1)
city2ID = namesLookup.get(city2)
startX = nodesGraph.get(city1ID)[0]
startY = nodesGraph.get(city1ID)[1]
x1End = nodesGraph.get(city2ID)[0]
y1End = nodesGraph.get(city2ID)[1]

openSet = []
closedSet = {}
#heappush(openSet, (calcd(y1End,x1End,startY,startX),city1ID,0,None))
heappush(openSet, (calcd(startX, startY,x1End,y1End),city1ID,0,None))
#heappush(openSet, (0,city1ID,None))
while(len(openSet) != 0):
    tup = heappop(openSet)
    name = tup[1]
    d = tup[2]
    #name = tup[1]
    #d = tup[0]
    aList = edgeGraph.get(name)
    if(name == city2ID):
        closedSet[name] = tup[3]
        #closedSet[name] = tup[2]
        sPath = findpath(closedSet,city2ID, city1ID)
        break
    for each in aList:
        x1 = nodesGraph.get(name)[1]
        y1 = nodesGraph.get(name)[0]
        x2 = nodesGraph.get(each)[1]
        y2 = nodesGraph.get(each)[0]
        aNewD = d + calcd(y1,x1,y2,x2)
        someD = calcd(y2,x2,x1End,y1End)
        if each in closedSet:
            continue
        if each not in openSet:
            heappush(openSet, (someD+aNewD,each, aNewD, name))
            #heappush(openSet, (aNewD,each, name))
        elif each in openSet:
            print("hello")
            #I should be updating here
        closedSet[name] = tup[3]
        #closedSet[name] = tup[2]

#----------------------------------Gives Sum of all Edges --------------------------#

# sumOfDistances = 0
# sumOfDistancesKilo = 0
# edges = list(edgeGraph.keys())
# for pairs in listofEdges:
#     pairList = pairs.split(" ")
#     edge1 = pairList[0]
#     edge2 = pairList[1].rstrip("\n")
#     coor1Lat = nodesGraph[edge1][0]
#     coor1Long = nodesGraph[edge1][1]
#     coor2Lat = nodesGraph[edge2][0]
#     coor2Long = nodesGraph[edge2][1]
#     sumOfDistances = sumOfDistances + calcd(coor1Lat, coor1Long, coor2Lat, coor2Long)
# #sumOfDistancesKilo = int(sumOfDistancesKilo)
# sumOfDistances = int(sumOfDistances)
# print("Sum of edges: " + str(sumOfDistances) + " miles")


#-----------------------------TKINTER GRAPHICS DISPLAY PROCESS----------------------#
root = Tk()
canvas = Canvas(root, width=900,height=700, background="white")
canvas.pack()

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle_arc = _create_circle_arc

#assign coordiantes to the points
minX = 10000000000 #round down
minY = 10000000000 #round down
coordinates = {} #each ID has its coordinate --> {ID: (xVal, yVal)}
for ID in nodesGraph:
    rawX = float(nodesGraph[ID][0])
    rawY = float(nodesGraph[ID][1])
    if (rawX)<minX:
        minX = rawX-1
    if (rawY)<minY:
        minY = rawY-1
coorX = 0
coorY = 0

for ID in nodesGraph.keys():
    rawX = float(nodesGraph[ID][0])
    rawY = float(nodesGraph[ID][1])
    coorX = (((rawX) - minX)*(-11))+600
    coorY = (((rawY) - minY)*(11))+50
    coordinates[ID] = (coorX, coorY)
#(((rawX) - minX)*(-140))+600
#(((rawY) - minY)*(120))+30

#---------------------------
    #canvas.create_oval(coorX, , coorY, , outline="black",fill="white", width=2)
    #canvas.create_circle(coorX, coorY, 15, fill="grey")
    #canvas.create_text(coorX,coorY,text=ID, fill="black", width=2)

    #w = Label(root, text="Hello, world!")
    #w.pack()
#---------------------------
print(openSet)
totalDistanceCheck = 0
for ID in nodesGraph:
    allNeighbors = edgeGraph[ID]
    xVal = coordinates[ID][0]
    yVal = coordinates[ID][1]
    rawLat = nodesGraph[ID][0]
    rawLong = nodesGraph[ID][1]
    for nbs in allNeighbors:
        currentXV = coordinates[nbs][0]
        currentYV = coordinates[nbs][1]
        currentLat = nodesGraph[nbs][0]
        currentLong = nodesGraph[nbs][1]
        if(ID in openSet):
            canvas.create_circle(yVal, xVal, 2, fill="green")
        if(ID in closedSet):
            canvas.create_circle(yVal, xVal, 2, fill="yellow")
        if(ID in sPath and nbs in sPath and sPath.index(ID) == sPath.index(nbs)-1):
            canvas.create_line(yVal, xVal, currentYV, currentXV, fill="red", width=3)
        elif(ID in sPath and nbs in sPath and sPath.index(ID) == sPath.index(nbs)+1):
            canvas.create_line(yVal, xVal, currentYV, currentXV, fill="red", width=3)
        else:
            canvas.create_line(yVal, xVal, currentYV, currentXV, fill="black", width=1)
            #canvas.create_circle(xVal, yVal, 1, fill="grey")
        midpointX = (xVal + currentXV)/2
        midpointY = (yVal + currentYV)/2
        distance = round(calcd(rawLat, rawLong, currentLat, currentLong),1)
        totalDistanceCheck = totalDistanceCheck + distance
x = 0
root.mainloop()

print(str(time.clock()) + "s")
sys.exit()
