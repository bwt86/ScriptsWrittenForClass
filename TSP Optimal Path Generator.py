#import math library
import math
from random import randint
import random
from tracemalloc import start
from turtle import color
import matplotlib.pyplot as plt

#define function to return euclidean distance from 2 tuples of coordinates
def euclideanDistance(starting, ending):
    distance = math.sqrt((ending[0] - starting[0])**2 + (ending[1] - starting[1])**2)   
    return distance;

#plots optimized route from points and visit order
def plotPrintRoute(locationsVisited, visitOrder, totalDistance):
    #print results
    print(f'Visit Order Starting From {visitOrder[0]} = {visitOrder}\nTotal Distance Starting From {visitOrder[0]} = {totalDistance}\n')
     
    #plot results using matplotlib
    x = []
    y = []

    #plot points as scatter plot
    for key in locationsVisited:
        x.append(locationsVisited.get(key)[0])
        y.append(locationsVisited.get(key)[1])
    plt.scatter(x,y)
    plt.scatter(x[0], y[0], color = 'red')

    #label points
    for key in locationsVisited:
        plt.annotate(key, (locationsVisited.get(key)[0], locationsVisited.get(key)[1]), (locationsVisited.get(key)[0] + .25, locationsVisited.get(key)[1] + .05), fontsize = 18)

    #add arrows
    for i in range(0,8):
        dx = locationsVisited.get(visitOrder[i+1])[0] - locationsVisited.get(visitOrder[i])[0]
        dy = locationsVisited.get(visitOrder[i+1])[1] - locationsVisited.get(visitOrder[i])[1]
        plt.arrow(locationsVisited.get(visitOrder[i])[0], locationsVisited.get(visitOrder[i])[1],dx,dy, length_includes_head = True,
        head_width = .5, head_length = .5)
    
    plt.title(f'Optimized Route Starting From {visitOrder[0]}')
    plt.show()

#runs nearest neighbor algorithm from a given starting node
def nearestNeighbor(startingNode):
    
    #Define Variables for the function
    locationsUnvisited =  {
        'a': (7,9),
        'b': (7,19),
        'c': (19,4),
        'd': (10,12),
        'e': (6,7),
        'f': (14,5),
        'g': (10,7),
        'h': (2,18)
    }

    locationsVisited = {}

    visitOrder = []

    totalDistance = 0;

    #add starting node to visited locations and visit order
    locationsVisited[startingNode] = locationsUnvisited.pop(startingNode);

    visitOrder.append(startingNode)

    #while there are unvisited locations do NN algorithm
    while(len(locationsUnvisited) > 0):
        distanceToPoints = {}
        #for each unvisited location get the distance between that and the last node added
        for key in locationsUnvisited:
            distanceToPoints[key] = euclideanDistance(locationsVisited.get(visitOrder[-1]), locationsUnvisited.get(key))
        #get point with min distance to last point
        minDist = min(distanceToPoints, key = distanceToPoints.get)
        #add that point to the visted locations, add to visit order, add the distance to total distance
        locationsVisited[minDist] = locationsUnvisited.pop(minDist)
        visitOrder.append(minDist)
        totalDistance += distanceToPoints[minDist]

    #add return distance to starting node
    totalDistance += euclideanDistance(locationsVisited.get(visitOrder[-1]), locationsVisited.get(visitOrder[0]))
    visitOrder.append(visitOrder[0])

    #print and plot results
    plotPrintRoute(locationsVisited, visitOrder, totalDistance)


#a
nearestNeighbor('a')
#b
nearestNeighbor('d')
#c
nearestNeighbor('c')
#d
nearestNeighbor('b')

#runs nearest insertion algorithm from a given starting node
def nearestInsertion(startingNode):
    #create variable required for dunction
    locationsUnvisited =  {
        'a': (7,9),
        'b': (7,19),
        'c': (19,4),
        'd': (10,12),
        'e': (6,7),
        'f': (14,5),
        'g': (10,7),
        'h': (2,18)
    }

    locationsVisited = {}

    visitOrder = []

    totalDistance = 0;

    #add starting node to visited and visit order
    locationsVisited[startingNode] = locationsUnvisited.pop(startingNode)

    visitOrder.append(startingNode)


    #while locations havent been visited run NI algorithm
    while(len(locationsUnvisited) > 0):
        
        distanceToPoints = {}
        #find closest node to last visted node
        for key in locationsUnvisited:
            distanceToPoints[key] = euclideanDistance(locationsVisited.get(visitOrder[-1]), locationsUnvisited.get(key))
        minDist = min(distanceToPoints, key = distanceToPoints.get)

        #if theres only 1 node in the locations visited add closest node, add the distance between nodes, add to visit order, and remove from unvisited locations
        if len(locationsVisited) == 1:
            locationsVisited[minDist] = locationsUnvisited.pop(minDist)
            visitOrder.append(minDist)
            totalDistance += distanceToPoints[minDist]
        #if theres more than 1 node in the list use nearest insertion calculation to get optimal insertion point, add to visited nodes, add to visit order in correct spot, and remove from unvisited locations
        else:
            minInsert = {}
            #for all key pairs see distance impact of inserting nodes between those keys 
            for key in locationsVisited:
                for key2 in locationsVisited:
                    #this if statement checks to make sure keys arent the same and that the opposite key hasnt already been measured for less computation
                    if key != key2 and (key2, key) not in minInsert:
                        minInsert[(key, key2)] = euclideanDistance(locationsVisited.get(key), locationsUnvisited.get(minDist)) + euclideanDistance(locationsUnvisited.get(minDist), locationsVisited.get(key2)) - euclideanDistance(locationsVisited.get(key), locationsVisited.get(key2))
            # get min key pair and insert after first key
            minInsertPt = min(minInsert, key = minInsert.get)
            locationsVisited[minDist] = locationsUnvisited.pop(minDist)
            totalDistance += minInsert[minInsertPt]
            visitOrder.insert(visitOrder.index(minInsertPt[0]) + 1,minDist)

    #add return distance to starting node
    totalDistance += euclideanDistance(locationsVisited.get(visitOrder[-1]), locationsVisited.get(visitOrder[0]))
    visitOrder.append(visitOrder[0])

    #print and plot results
    plotPrintRoute(locationsVisited, visitOrder, totalDistance)

   
        
#e
nearestInsertion('a')
#f
nearestInsertion('d')
#g
nearestInsertion('b')

def kOpt(currentTour, iterations):
    #list of current locations
    locations =  {
        'a': (7,9),
        'b': (7,19),
        'c': (19,4),
        'd': (10,12),
        'e': (6,7),
        'f': (14,5),
        'g': (10,7),
        'h': (2,18)
    }
    #find current total distance and report it
    totalDistance = 0;
    for i in range(0,9):
            if i != 8:
                totalDistance += euclideanDistance(locations.get(currentTour[i]), locations.get(currentTour[i + 1]))
            else:
                totalDistance += euclideanDistance(locations.get(currentTour[-1]), locations.get(currentTour[0]))
    print(f'Total distance starting at {totalDistance} with tour {currentTour}')

    # while we still have iterations to go, go through and  perform improvement algorithm
    while(iterations > 0):
        #pick 2 pairs of points that retain the starting and ending nodes
        pair = []
        start = random.randint(1,7)
        pair.append(start)
        if start == 8:
            pair.append(0)
        else:
            pair.append(start + 1)

        pair2 = []
        start2 = random.randint(1,7)
        while start2 == start or start2 == start + 1 or (start2 == 8 and start == 0) or (start2 == 0 and start == 8):
            start2 = random.randint(1,7)
        pair2.append(start2)
        if start2 == 8:
            pair2.append(0)
        else:
            pair2.append(start2 + 1)
        
        swapped1 = [pair[0], pair2[1]]
        swapped2 = [pair2[0], pair[1]]

        locationList = currentTour.copy()

        #perform potential swap on pairs of point and get total distance of new tour
        currentTour2 = currentTour.copy()
        currentTour2[pair[1]] = locationList[pair2[1]] 
        currentTour2[pair2[1]] = locationList[pair[1]]
        totalDistance2 = 0;
        for i in range(0,9):
            if i != 8:
                totalDistance2 += euclideanDistance(locations.get(currentTour2[i]), locations.get(currentTour2[i + 1]))
            else:
                totalDistance2 += euclideanDistance(locations.get(currentTour2[-1]), locations.get(currentTour2[0]))

        #get distance impact to see if theres an improvement
        distanceImpact = totalDistance2 - totalDistance 

        # if theres and improvement make swap and report it, if not dont swap and also report that 
        if distanceImpact < 0:
            currentTour[pair[1]] = locationList[pair2[1]] 
            currentTour[pair2[1]] = locationList[pair[1]]
            print(f'Swap occured for an improvement of {distanceImpact}. Swapped {locationList[pair[0]]}-{locationList[pair[1]]} and {locationList[pair2[0]]}-{locationList[pair2[1]]} to {locationList[pair[0]]}-{locationList[pair2[1]]} and {locationList[pair2[0]]}-{locationList[pair[1]]}')
            print(f'Tour now {currentTour}')
        else:
            print(f'No swap occurred, tried swapping {locationList[pair[0]]}-{locationList[pair[1]]} and {locationList[pair2[0]]}-{locationList[pair2[1]]} to {locationList[pair[0]]}-{locationList[pair2[1]]} and {locationList[pair2[0]]}-{locationList[pair[1]]} but added {distanceImpact} to the tour.')
        totalDistance = 0;

        # after swap or no swap evaluate current total distance and report it
        for i in range(0,9):
            if i != 8:
                totalDistance += euclideanDistance(locations.get(currentTour[i]), locations.get(currentTour[i + 1]))
            else:
                totalDistance += euclideanDistance(locations.get(currentTour[-1]), locations.get(currentTour[0]))
        
        print(f'Total distance now {totalDistance}')
        iterations += -1
    print('\n')
    

#h
kOpt(['a','e','g','f', 'c', 'd', 'b', 'h', 'a' ], 2)

#i
kOpt(['d','a','e','g', 'f', 'c', 'b', 'h', 'd' ], 2)


