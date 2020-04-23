from PIL import Image
from heapdict import heapdict
import sys
import math
import time

END_COLOR = (255, 0, 0)
START_COLOR = (0, 255, 0)
PATH_COLOR = (255, 255, 255)
BORDER_COLOR = (0, 0, 0)
SHORTEST_PATH_COLOR = (66, 135, 245)

class Graph:
    def __init__(self, imageWidth):
        self.edgeList = {}
        self.imageWidth = imageWidth

    def addNode (self, n):
        self.edgeList[n] = []

    def removeNode(self, n):
        connections = self.edgeList.pop(n)
        for node in connections:
            self.edgeList[node].remove(n)    

    def removeEdge(self, n1, n2):
        self.edgeList[n1].remove(n2)
        self.edgeList[n2].remove(n1)

    def addEdge(self, n1, n2):
        self.edgeList[n1].append(n2)
        self.edgeList[n2].append(n1)

    def trim(self):
        removals = -1
        toRemove = []

        # If we did not remove anything on the previous iteration we know we are done
        while removals != 0:
            removals = 0

            # find dead ends and add them to a queue to remove
            for node in self.edgeList:
                if len(self.edgeList[node]) < 2:
                    toRemove.append(node)
            
            # pop from queue and remove the dead ends
            while toRemove:
                self.removeNode(toRemove.pop())
                removals += 1 
    
    # Perform A* algorithm and return the path from start to end
    def shortestPath(self, start, end):
        def reconstructPath(predacesors, current):
            path = [current]
            while current in predacesors:
                current = predacesors[current]
                path.append(current)
            return path[::-1]

        endx, endy = convert1D(end, self.imageWidth)
        def h(n):
            # Our heuristic is the Manhattan distance
            nx, ny = convert1D(n, self.imageWidth)
            return abs(endx - nx) + abs(endy - ny)

        # Used to backtrack the best path
        predacesors = {}
        
        # Best known cost to each node
        gScores = {}
        for n in self.edgeList:
            gScores[n] = math.inf
        gScores[start] = 0

        # Based on the heuristic, what is the best possible distance
        # to get to the start
        fScores = {}
        for n in self.edgeList:
            fScores[n] = math.inf
        fScores[start] = h(start)

        # Set of nodes that may need processed
        openSet = heapdict()
        openSet[start] = fScores[start]

        while openSet:
            current = openSet.peekitem()[0]

            # Finished path
            if current == end:
                return reconstructPath(predacesors, current)

            openSet.popitem()
            for neighbor in self.edgeList[current]:
                tentativeGScore = 1 + gScores[current]
                if tentativeGScore < gScores[neighbor]:
                    predacesors[neighbor] = current
                    gScores[neighbor] = tentativeGScore
                    fScores[neighbor] = gScores[neighbor] + h(neighbor)
                    if not neighbor in openSet:
                        openSet[neighbor] = fScores[neighbor]

        # There is not path!
        return None
        

def removeAlpha(imgData):
    for i in range(len(imgData)):
        imgData[i] = imgData[i][:3]

def convert1D(i, imageWidth):
    return (i % imageWidth, i // imageWidth)

def convert2D(x, y, imageWidth):
    return x + y // imageWidth

""" Scans through imageData looking for start and end colors. Assumes only one pixel of 
    each is present, if one is not found it will be None. """
def getEndPoints(imgData, imageWidth):
    start = None
    end = None
    for i in range(len(imgData)):
        if imgData[i] == END_COLOR:
            end = i
        elif imgData[i] == START_COLOR:
            start = i
    return (start, end)

""" Returns wether or not the index in imgData is a path. """
def isPath(i, imgData, imgWidth):
    # Allow either a 1D index or a 2D index
    if type(i) == tuple:
        i = convert2D(*i, imgWidth)
    
    # Out of range is not part of the path
    if not i in range(len(imgData)):
        return False

    # Start and end are definitionally part of the path
    return imgData[i] == PATH_COLOR \
        or imgData[i] == END_COLOR \
        or imgData[i] == START_COLOR

""" Draws BORDER_COLOR over dead ends. """
def reflectTrim(image, G):
    for i in range(len(imgData)):
        if not i in G.edgeList:
            image.putpixel(convert1D(i, image.width), BORDER_COLOR)


if __name__ == "__main__":

    # Get input for maze image

    if len(sys.argv) < 2:
        fp = input("Enter a path to a maze image:")
    else:
        fp = sys.argv[1]
    

    # Different output name
    outName = "out.png"
    if "-o" in sys.argv:
        if sys.argv.index("-o")+1 < len(sys.argv):
            outName = sys.argv[sys.argv.index("-o")+1]


    image = Image.open(fp)
    if image is None:
        print("Cannot find file.")
        sys.exit()
    imgData = list(image.getdata())

    # Remove the alpha component of imgData so equalities are accurate
    removeAlpha(imgData)

    # Find start (green) and end (red) points

    print("Scanning for start and end points...", end = " ")

    start, end = getEndPoints(imgData, image.width)
    if (not start is None):
        print(f"Start found at {start}.", end = " ")
    else:
        print("Start not found, closing.")
        sys.exit()
    if (not end is None):
        print(f"End found at {end}.")
    else:
        print("End not found, closing.")
        sys.exit()

    # Build graph of maze.
    # Here each path pixel will be a node in the graph.
    
    timeStart = time.time()
    print("Creating Graph...", end=" ", flush=True)
    G = Graph(image.width)
    for i in range(len(imgData)):
        if isPath(i, imgData, image.width):
            # We add the pixel as a node and connect it to paths up and left of it
            # if they exist. This gets every connection without looking down and to the
            # right because its a non-directional graph.
            G.addNode(i)
            left = i - 1
            if isPath(left, imgData, image.width):
                G.addEdge(i, left)
            up = i - image.width
            if isPath(up, imgData, image.width):
                G.addEdge(i, up)
    print(f"Done ({(time.time() - timeStart):.2f}s)")
    
    # Get shortestPath
    timeStart = time.time()
    print("Finding shortest path...", end=" ", flush=True)
    shortestPath = G.shortestPath(start, end)
    print(f"Done ({(time.time() - timeStart):.2f}s)")

    print(f"Shortest Path Length = {len(shortestPath)}")

    # Draw shortest path onto image
    for i in shortestPath:
        image.putpixel(convert1D(i, image.width), SHORTEST_PATH_COLOR)
    
    image.putpixel(convert1D(start, image.width), START_COLOR)
    image.putpixel(convert1D(end, image.width), END_COLOR)
    
    # Output modified image

    image.save(outName, "PNG")
