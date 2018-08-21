# Kristen Harrison, CS325 HW5

from collections import deque
import sys


# each vertex is initialized with name, undiscovered status,
# no team, and empty rivals list
class Wrestler:
    def __init__(self, name):
        self.name = name
        self.color = "WHITE"
        self.team = -1
        self.rivals = []


# a graph instance tracks a vertices list and can add a
# vertex or edge
class Graph:
    def __init__(self):
        # list of wrestlers
        self.vertices = []

    # creates a new vertex and adds it to the graph's vertices list
    def add_wrestler(self, name):
        self.vertices.append(Wrestler(name))

    # creates a new edge by adding the rivalry to both vertices
    def add_rivalry(self, name, rival):
        for x in self.vertices:
            if x.name == name:
                # add to x.rivals
                for y in self.vertices:
                    if y.name == rival:
                        x.rivals.append(y)
                        y.rivals.append(x)



# conducts a modified breadth-first search to check if the vertices
# can be divided into two sets, with only cross edges between them
def bfs_bipartite(wrestlers):
    queue = deque([])
    babyfaces = []
    heels = []

    # loop through all vertices in case graph is disconnected
    for i in range(len(wrestlers)):

        # already processed nodes are skipped;
        # otherwise set source node to babyface team
        if wrestlers[i].color == "WHITE":
            s = wrestlers[i]
            s.color = "GREY"
            s.team = 0
            babyfaces.append(s.name)
            queue.append(s)

            # process all neighboring nodes
            while len(queue) > 0:
                u = queue.popleft()
                for v in u.rivals:
                    # undiscovered nodes are set to opposing side
                    if v.color == "WHITE":
                        if u.team == 0:
                            v.team = 1
                            heels.append(v.name)
                        else:
                            v.team = 0
                            babyfaces.append(v.name)
                        v.color = "GREY"
                        queue.append(v)
                    # otherwise check for conflict
                    elif v.color == "GREY":
                        if v.team == u.team:
                            return("No")
                u.color = "BLACK"

    # all wrestlers processed without conflicts; graph is bipartite
    return("Yes", babyfaces, heels)


# input file is last in command line args
filename = sys.argv[-1]
file_in = open(filename, 'r')

# add wrestlers to graph as vertices
wrestlerCount = int(file_in.readline())
wrestlerList = Graph()

for i in range(wrestlerCount):
    nextLine = file_in.readline().strip()
    wrestlerList.add_wrestler(nextLine)

# add rivalries to graph as edges
rivalries = int(file_in.readline())

for i in range(rivalries):
    nextLine = file_in.readline().strip()
    arr = list(map(str, nextLine.split()))
    wrestlerList.add_rivalry(arr[0], arr[1])


# check whether bipartite and output results
status = bfs_bipartite(wrestlerList.vertices)

if status[0] == "Yes":
    print(status[0])
    print("Babyfaces:", ' '.join(status[1]))
    print("Heels:", ' '.join(status[2]))
else:
    print(status)


file_in.close()

