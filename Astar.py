import math
import sys
from collections import deque as queue
from heapq import heapify, heappush, heappop

infile = open('input.txt', 'r')  # Reading the input file in read mode

input_data = infile.read().split('\n')

# Input Line 1
algoType = input_data[0]

# Input Line 2
gridWidth, gridHeight = tuple(map(int, input_data[1].split()))

# Input Line 3
startGrid = tuple(map(int, input_data[2].split()))

# Input Line 4
stamina = int(input_data[3])

# Input Line 5
numberOfLodges = int(input_data[4])

# Input Lines (next N lines)
lodges = {}
lodges_arr = []
for i in range(numberOfLodges):
    lodges_arr.append(tuple(map(int, input_data[5 + i].split())))
    lodges[tuple(map(int, input_data[5 + i].split()))] = None

# Input Lines (next H lines)
numberofgap = 5 + numberOfLodges
mapGrid = []
for i in range(gridHeight):
    mapGrid.append(list(map(int, input_data[numberofgap + i].split())))

# defining possible neighbour relative coordinates
# (y coordinate,
#  x coordinate)
# neighbors sequence in clockwise direction strating from north side.
neiy = [-1, -1, -1, 0, 1, 1, 1, 0]
neix = [-1, 0, 1, 1, 1, 0, -1, -1]


########### BFS FUNCTION FOR SEARCHING
def backtrack(curr, visited):
    currx = curr[0]
    curry = curr[1]
    arr = []
    arr.append(curr)
    while (visited[(currx, curry)] != None):
        arr.append(visited[(currx, curry)])
        (currx, curry) = visited[(currx, curry)]
    return arr


def isValid(currVal, nexty, nextx, M=0):
    # checking boundary cases of the grid
    if (nexty >= gridHeight or nextx >= gridWidth or nextx < 0 or nexty < 0):
        return False

    # check for the nextVal and for comparison and requirement satisfaction
    nextVal = mapGrid[nexty][nextx]

    # if next location is at lower elevation then no matter what, just go there.
    if (abs(currVal) >= abs(nextVal)):
        return True

    # if next location is not lower and equal and its tree then we cant go there.
    if (nextVal < 0):
        return False

    # if next location is land and higher than the current location, then check the stamin level.
    if (nextVal > 0 and abs(currVal) < nextVal):
        if (nextVal - abs(currVal) <= stamina + M):
            return True
        else:
            return False


def BFS():
    q = queue()
    visited = {}

    # initialize q with starting grid
    q.append(startGrid)
    visited[startGrid] = None

    while (len(q) > 0 and (None in lodges.values())):

        # take left most node from queue and visit it.
        curr = q.popleft()
        currx = curr[0]
        curry = curr[1]

        if (curr in lodges):
            backpath = backtrack(curr, visited)
            lodges[curr] = backpath[::-1]

        # y is first entry in index of mapgrid and x is for second one
        currVal = mapGrid[curry][currx]

        # check for all possible neighbors and add them according to requirement to the queue and make it bfs
        for i in range(len(neix)):
            nextx = currx + neix[i]
            nexty = curry + neiy[i]

            # check for all constraints regarding neighbour tree and elevation and boundry etc.
            if (isValid(currVal, nexty, nextx) and ((nextx, nexty) not in visited)):
                q.append((nextx, nexty))
                visited[(nextx, nexty)] = (currx, curry)


def UCSdistance(curr, next):
    return math.floor(math.sqrt((next[0] - curr[0]) ** 2 + (next[1] - curr[1]) ** 2) * 10)


def backtrackUCS(curr, InHeap):
    arr = []
    arr.append(curr)
    while (InHeap[curr][1] != None):
        arr.append(InHeap[curr][1])
        curr = InHeap[curr][1]
    return arr


def backtrackA_star(curr, M, visited):
    arr = []
    arr.append(curr)
    while (visited[(curr, M)][1] != None):
        arr.append(visited[(curr, M)][1])
        next_M = visited[(curr, M)][3]
        next_curr = visited[(curr, M)][1]
        curr = next_curr
        M = next_M
    return arr


def UCS():
    # making a list and make it a empty heap
    heap_q = []
    heapify(heap_q)
    InHeap = {}

    # add a starting node and make it 0 value node to take it first using min heap.
    heappush(heap_q, (0, startGrid))
    InHeap[startGrid] = (0, None)

    while (len(heap_q) > 0 and (None in lodges.values())):

        # take cheapest value node from heap and visit it.
        curr = heappop(heap_q)[1]
        currx = curr[0]
        curry = curr[1]

        if (curr in lodges):
            backpath = backtrackUCS(curr, InHeap)
            lodges[curr] = backpath[::-1]

        # y is first entry in index of mapgrid and x is for second one
        currVal = mapGrid[curry][currx]

        # check for all possible neighbors and add them according to requirement to the queue and make it bfs
        for i in range(len(neix)):
            nextx = currx + neix[i]
            nexty = curry + neiy[i]

            next = (nextx, nexty)
            # calculate the path value from curr to next
            val = InHeap[(currx, curry)][0] + UCSdistance(curr, next)

            # check for all constraints regarding neighbour tree and elevation and boundry etc.
            if (isValid(currVal, nexty, nextx) and ((nextx, nexty) not in InHeap)):
                # give to the queue
                heappush(heap_q, (val, (nextx, nexty)))
                InHeap[(nextx, nexty)] = (val, (currx, curry))


def heuristic(dest, next):
    return math.floor(math.sqrt((next[0] - dest[0]) ** 2 + (next[1] - dest[1]) ** 2) * 10)


def A_star():
    for dest_lodge in lodges_arr:

        # making a list and make it a empty heap
        # heapq structure (cost,normal_cost,startGrid,prev)
        heap_q = []
        heapify(heap_q)
        # visited dictionary structure
        # { (node,momentum-at-node) : (cost,normal_cost,prev) }
        visited = {}

        cost = 0
        # with heuristic value
        normal_cost = 0
        # without heuristic value

        # add a starting node and make it 0 value node to take it first using min heap.
        heappush(heap_q, (cost, normal_cost, startGrid, (None, 0)))

        while (len(heap_q) > 0):

            # take cheapest value node from heap and visit it.
            heapNode = heappop(heap_q)

            cost = heapNode[0]
            current_cost = heapNode[1]
            curr = heapNode[2]
            prev = heapNode[3][0]
            prev_M = heapNode[3][1]

            currx = curr[0]
            curry = curr[1]
            currVal = mapGrid[curry][currx]

            M = 0
            # checking whether its first node or not?
            if (prev != None):
                prevVal = mapGrid[prev[1]][prev[0]]
                M = max(0, abs(prevVal) - abs(currVal))

            if ((curr, M) in visited):
                continue

            # current_cost = normal cost of the node which we have paid in form of
            #   elevation cost+ neighbor cost + previos current cost of parent
            visited[(curr, M)] = (cost, prev, current_cost, prev_M)

            if (curr == dest_lodge):
                backpath = backtrackA_star(curr, M, visited)
                lodges[curr] = backpath[::-1]
                break

            for i in range(len(neix)):

                nextx = currx + neix[i]
                nexty = curry + neiy[i]
                next = (nextx, nexty)

                if (isValid(currVal, nexty, nextx, M)):

                    nextVal = mapGrid[nexty][nextx]
                    E_cost = 0
                    if (nextVal - currVal > M):
                        E_cost = max(0, abs(nextVal) - abs(currVal) - M)

                    normal_cost = current_cost + UCSdistance(curr, next) + E_cost
                    cost = normal_cost + heuristic(dest_lodge, next)

                    next_M = max(0, abs(currVal) - abs(nextVal))
                    if ((next, next_M) not in visited):
                        heappush(heap_q, (cost, normal_cost, next, (curr, M)))

if algoType == 'BFS':
    BFS()
if algoType == 'UCS':
    UCS()
if algoType == 'A*':
    A_star()

outStr = ''
for i,lodge_iter in enumerate(lodges_arr):
    route = lodges[lodge_iter]
    if(route == None):
        outStr += 'FAIL'
    else:
        for j,tile in enumerate(route):
            outStr += str(tile[0]) + ',' + str(tile[1])
            if(j != len(route)-1):
                outStr += ' '
    outStr += '\n'

# ******** OUTPUT DATA : START ********

outfile = open('output.txt',"w")
outfile.write(outStr)
outfile.close()
infile.close()
