from PIL import Image
import sys
import math
import time

END_COLOR = (255, 0, 0)
START_COLOR = (0, 255, 0)
PATH_COLOR = (255, 255, 255)
BORDER_COLOR = (0, 0, 0)
SHORTEST_PATH_COLOR = (252, 232, 3)

class Graph:
    def __init__(self):
        self.edgeList = {}

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
    
    # Perform Dijkstra's algorithm and return the path from start to end
    def shortestPath(self, start, end):
        
        # Set up distances, which records the current best way to get to each node
        distances = {}
        for node in self.edgeList:
            distances[node] = math.inf 
        distances[start] = 0

        # Set up processed, which records if a node's shortest path has been determined
        processed = {}
        for node in self.edgeList:
            processed[node] = False

        # Set up processed, which records the node used to get to node, 
        # in its shortest path
        predecessors = {}
        for node in self.edgeList:
            predecessors[node] = -1 

        # Define a local function to pick the next node to process
        def selectNextNode():
            minDistance, minNode = math.inf, -1
            for node in self.edgeList:
                if distances[node] < minDistance and not processed[node]:
                    minDistance, minNode = distances[node], node

            return minNode
        
        # Perform Dijkstra's
        current = selectNextNode()
        while current != -1:
            for node in self.edgeList[current]:
                if distances[current] + 1 < distances[node]:
                    distances[node] = distances[current] + 1
                    predecessors[node] = current
                processed[current] = True

            current = selectNextNode()

        # backtrack and return shortest path
        path = []
        node = end
        while node != -1:
            path.append(node)
            node = predecessors[node]
        
        return path

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

    showTrim = False
    if "--show-trim" in sys.argv:
        showTrim = True
    

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
    G = Graph()
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

    # Hack: put a fake edge connection for start and end nodes so that
    # trim doesn't remove them.
    G.edgeList[start].append(-1)
    G.edgeList[end].append(-1)

    # Trim the graph to remove all dead ends speed up our search.
    timeStart = time.time()
    print("Trimming...", end=" ", flush=True)
    G.trim()
    print(f"Done ({(time.time() - timeStart):.2f}s)")

    # Now that it is trimmed, remove the dummy connections.
    G.edgeList[start].remove(-1)
    G.edgeList[end].remove(-1)

    # Cut out dead ends in final image.
    if showTrim:
        reflectTrim(image, G)
    
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

    image.save("out.png", "PNG")
