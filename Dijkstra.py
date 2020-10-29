# shortest distance using Dijkstra's algorithm
import heapq
from os import path
import pandas as pd  # 'pip install pandas' if you get No module named 'pandas' error
# on Python 3.9, pip install pipwin and pipwin install pandas

# loading the graph from the json file located in .\graph folder
dirName = path.dirname(__file__)
fileName = path.join(dirName, 'graph/graph.json')
graph = pd.read_json(fileName)
print('Graph has '+str(len(graph))+' nodes.')
# We only need id, neighbors, and distances columns
graph = graph[['id', 'nbrs', 'dists']]


def findDistance(src, trg):  # Dijkstra's shortest path algorithm
    success = False
    distance = -1
    vis = [False for i in range(len(graph))]  # tracks the visited nodes
    # creating and initializing the priority queue
    pq = []
    heapq.heappush(pq, (0, src))
    while (len(pq) > 0 and not success):
        cNode = heapq.heappop(pq)
        if (cNode[1] == trg):  # terminate if we reach the destination
            success = True
            distance = cNode[0]
            break
        else:
            vis[cNode[1]] = True  # setting visited to True
            nbrs = list(zip(graph.iloc[cNode[1], 1], graph.iloc[cNode[1], 2]))
            for id, dist in nbrs:  # iterate over its neighbors
                if (not vis[id]):  # only check unvisited nodes
                    nInd = isInQ(pq, id)
                    # if the new node is in the priority queue, we update its weight if the new weight is lower
                    if ((nInd[0] >= 0)):
                        if ((nInd[1] > cNode[0]+dist)):
                            pq[nInd[0]] = (cNode[0]+dist, id)
                            # if the new weight is less than the current weight, move up and swap with the parent if needed
                            heapq._siftdown(pq, 0, nInd[0])
                    else:  # if the new node is not the priority queue, we push it in
                        heapq.heappush(pq, (cNode[0]+dist, id))

    return distance

# searches the queue for an element and if available, returns the (index, weight), otherwise retuns (-1,-1)


def isInQ(q, element):
    index = 0
    while index < len(q):
        if q[index][1] == element:
            return (index, q[index][0])
        index += 1
    return (-1, -1)


# this is how to call the distance function. src and trg can be any intergers between 0 and len(graph)
print(findDistance(5273, 123))
