from PIL import Image

END_COLOR = (255, 0, 0)
START_COLOR = (0, 255, 0)
PATH_COLOR = (255, 255, 255)
BORDER_COLOR = (0, 0, 0)

class Graph:
    pass

class Node:
    pass

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
            end = convert1D(i, imageWidth)
        elif imgData[i] == START_COLOR:
            start = convert1D(i, imageWidth)
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
    return imgData[i] == PATH_COLOR 
        or imgData[i] == END_COLOR 
        or imgData[i] == START_COLOR


if __name__ == "__main__":

    # Get input for maze image

    fp = input("Enter path to maze to be solved: ")
    image = Image.open(fp)
    if image is None:
        print("Cannot find file.")
    sys.exit()
    imgData = list(image.getdata())

    # Find start (green) and end (red) points

    print("Scanning for start and end points...", end = " ")

    start, end = getEndPoints(imgData, image.width)
    if (start):
        print(f"Start found at {start}.", end = " ")
    else:
        print("Start not found, closing.")
        sys.exit()
    if (end):
        print(f"End found at {end}.")
    else:
        print("End not found, closing.")
        sys.exit()

    # Build graph of maze.
    # Here each path pixel will be a node in the graph

    

    # Output modified image

    image.save("out.png", "PNG")
