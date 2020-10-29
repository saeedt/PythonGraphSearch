# Multi Threaded Dijkstra's (MTD) algorithm
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


def findMedian(nodes, weights):  # MTD algorithm
    success = False
    bestDist = float('inf')
    bestId = -1
    # for each node, we use a bit to represent its visited status in each thread
    vis = [0 for i in range(len(graph))]
    # stores distance of the nodes from each of the demand points
    dists = [[0 for i in range(len(nodes))] for j in range(len(graph))]
    maxVis = pow(2, len(nodes))-1  # constant used to verify a node is visited in all threads
    # creating and initializing the priority queue
    pq = []
    index = 0
    for node in nodes:
        heapq.heappush(pq, (0, index, node))
        index += 1
    while (len(pq) > 0 and not success):
        cNode = heapq.heappop(pq)
        vis[cNode[2]] |= pow(2, cNode[1])  # Setting the node visited in its thread
        dists[cNode[2]][cNode[1]] = cNode[0]  # storing the weighted distance
        if (vis[cNode[2]] == maxVis):  # if the node is visited in all threads
            if (sum(dists[cNode[2]]) < bestDist):
                bestDist = sum(dists[cNode[2]])
                bestId = cNode[2]
        if bestDist < cNode[0]:  # optimality criteria
            success = True
            break
        else:
            nbrs = list(zip(graph.iloc[cNode[2], 1], graph.iloc[cNode[2], 2]))
            for id, dist in nbrs:  # iterate over its neighbors
                if (((vis[id] & (pow(2, cNode[1]))) >> cNode[1]) == 0):  # only check unvisited nodes
                    #print([cNode[1], id])
                    nInd = isInQ(pq, cNode[1], id)
                    # if the new node is in the priority queue, we update its weight if the new weight is lower
                    if ((nInd[0] >= 0)):
                        if ((nInd[1] > cNode[0]+weights[cNode[1]]*dist)):
                            pq[nInd[0]] = (cNode[0]+weights[cNode[1]]*dist, cNode[1], id)
                            # if the new weight is less than the current weight, move up and swap with the parent if needed
                            heapq._siftdown(pq, 0, nInd[0])
                    else:  # if the new node is not the priority queue, we push it in
                        heapq.heappush(pq, (cNode[0]+weights[cNode[1]]*dist, cNode[1], id))
    return (bestId, bestDist, dists[bestId])

# searches the queue for an element and if available, returns the (index, weight), otherwise retuns (-1,-1)


def isInQ(q, thread, element):
    index = 0
    while index < len(q):
        if (q[index][1] == thread) and (q[index][2] == element):
            return (index, q[index][0])
        index += 1
    return (-1, -1)


# this is how to call the median function
print(findMedian([0, 4, 2], [1, 1, 1]))
