from graphics import *
from random import randint, choice
from math import sqrt
from sys import maxsize

nodes = [] # global nodes array
finalDistance = 0
finalSequence = []
width, height = 1000, 500
win = GraphWin('Pathfind', width, height) # create window

class Node :
    def __init__(self, name, edges, x, y):
        self.name = name
        self.edges = edges
        self.x = x
        self.y = y
        self.distance = None  # distance from node to initial node is set to None
        self.tentative = None
        self.unvisited = True
        self.color = 'red'

class Edge :
    def __init__(self, length, endpoints):
        self.length = length
        self.endpoints = endpoints
        self.considered = False
        self.line = Line(Point(0,0), Point(0,0))
        self.color = 'black'

def initGraph(minNodes, maxNodes) :
    # Dynamic Definition
    for n in range(randint(minNodes,maxNodes)):
        xValues, yValues = [], []

        x = randint(width // 5, 4 * width // 5) # x b/w 1/5 and 4/5 of the width
        y = randint(height // 5, 4 * height // 5) # y b/w 1/5 and 4/5 of the height

        xValues.append(x)
        yValues.append(y)

        for xval in xValues :
            if abs(xval - x) <= 10 :
                x += 10
        for yval in yValues :
            if abs(yval - y) <= 10 :
                y += 10
        
        nodes.append(Node(n, [], x, y)) # new node

    for node in nodes :     # for each node
        numEdges = randint(1, 2)        # select random number of edges
        connected = nodes.copy()         # list of nodes that this node is connecting to

        for e in range(numEdges) :       # for each of the random num of edges           
            randomNode = choice(connected)

            xsquared = (node.x - randomNode.x) ** 2
            ysquared = (node.y - randomNode.y) ** 2
            distance = int(sqrt(xsquared + ysquared)) # calculate distance between the two nodes

            edge = Edge(distance, [node, randomNode]) # creat new edge with length distance and endpoints

            node.edges.append(edge) # add edge to node edges list
            randomNode.edges.append(edge) # add edge to randNode edges list

            connected.remove(randomNode) # remove from connected list so it can't be chosen again

def findSequence(initial, destination) :
    current = destination         # start from destination node
    connectionDistances = []      # list to store each node's connection's distances
    sequence = [destination.name] # start the sequence with the destination

    while current is not initial : # repeat until initial node is reached
        for edge in current.edges : # for each edge connected to current
            for endpoint in edge.endpoints :
                if endpoint is not current : # for each endpoint to that edge
                    connectionDistances.append(endpoint.distance) # add that endpoint's distance to list
        
        ## we now have a list of all the distances from the initial node of all connections to current

        for node in nodes : # find the node with the minimum distance to initial
            if node.distance is not None and node.distance == min(connectionDistances) :
                for edge in node.edges :
                    for endpoint in edge.endpoints :
                        if endpoint is current :
                            edge.color = 'blue'
                current = node # set that node to current
                current.color = 'green'
                sequence.append(current.name) # add it to list
                break
    
    initial.color = 'blue'
    sequence.reverse() # reverse list to start from initial
    return sequence
    
def dijkstra(initial, destination) :
    unvisited = nodes.copy() # the unvisited set is initially all nodes
    initial.distance = 0     # set initial node's distance to zero
    current = initial        # set the current node to initial
    sequence = []
    
    while(True) :
        for edge in current.edges : # for edges in current node
            for endpoint in edge.endpoints : # for each endpoint on each edge
                if endpoint is not current and endpoint.unvisited :  # find an unvisited neighbor node
                    endpoint.tentative = current.distance + edge.length # calculate tentative distance of endpoint through current
                    
                    if endpoint.distance is None :        # if node's distance has not yet been calculated
                        endpoint.distance = endpoint.tentative  # set it to tentative
                    elif endpoint.tentative < endpoint.distance : # compare tentative to actual
                        endpoint.distance = endpoint.tentative  # change if tentative is less

        current.unvisited = False
        unvisited.remove(current) 

        if not destination.unvisited :  # if destination has been visited  
            destination.color = 'blue' 
            return destination.distance, findSequence(initial, destination)
        else :                          # else select next current node
            minTentative = maxsize
            for node in unvisited :
                # find the lowest tentative distance
                if node.tentative is not None and node.tentative <= minTentative :  
                    current = node
    
def display(circleSize) :
    for node in nodes : # draw all edges first
        for edge in node.edges :
            edge.line = Line(Point(edge.endpoints[0].x, edge.endpoints[0].y),Point(edge.endpoints[1].x, edge.endpoints[1].y))
            edge.line.setFill(edge.color)
            edge.line.draw(win)

    for node in nodes : # draw all circles
        circle = Circle(Point(node.x, node.y), circleSize)
        circle.setFill(node.color)
        circle.draw(win)

        name = Text(Point(node.x, node.y), node.name)
        name.draw(win)
    
    distanceText = Text(Point(width // 8, height // 8), 'Path Distance: ' + str(finalDistance))
    sequenceText = Text(Point(width // 5, (height // 8) + 20), 'Sequence: ' + str(finalSequence))

    distanceText.setSize(16)
    sequenceText.setSize(16)
    distanceText.draw(win)
    sequenceText.draw(win)

    win.getMouse() # Pause to view result
    win.close()
                    
initGraph(10, 12) # inputs : min nodes, max nodes
finalDistance, finalSequence = dijkstra(choice(nodes), choice(nodes))
display(15) # inputs: size of circles

