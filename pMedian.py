# Multi Threaded Dijkstra's (MTD) algorithm
import heapq
from os import path
from operator import itemgetter
from math import radians, sin, cos, asin, sqrt
import pandas as pd  # 'pip install pandas' if you get No module named 'pandas' error
# on Python 3.9, pip install pipwin and pipwin install pandas

# loading the graph from the json file located in .\graph folder
dirName = path.dirname(__file__)
fileName = path.join(dirName, 'graph/graph.json')
graph = pd.read_json(fileName)
print('Graph has '+str(len(graph))+' nodes.')
graph = graph[['id', 'nbrs', 'dists', 'lat', 'lon']]


def findCluster(nodes, weights, p, pec, maxItr=1000):
    pec = int(pec*p)
    dps = list(zip(nodes, weights))  # make a tuple from the demand points
    dps.sort(key=itemgetter(1), reverse=False)  # sorting the demand points in ascending order
    clusters = []  # initializing the clusters
    for i in range(p):
        point = dps.pop()  # remove the last item in the list (highest weight)
        cluster = {'id': i, 'median': (graph['lon'][point[0]],
                                       graph['lat'][point[0]]), 'dps': [point]}
        clusters.append(cluster)
    while len(dps) > 0:
        bestDist = float('inf')
        bestId = -1
        src = dps.pop()
        for cluster in clusters:
            dist = findSDist((graph['lon'][src[0]], graph['lon'][src[0]]), cluster['median'])
            if dist < bestDist:
                bestDist = dist
                bestId = cluster['id']
        clusters[bestId]['dps'].append(src)  # add the node to the closest cluster
        clusters[bestId]['median'] = findCOM(clusters[bestId]['dps'])  # update the center of mass

        distMat = [[0 for i in range(p)] for j in range(p)]  # initialize the distance matrix
        for (i, j) in [(i, j) for i in range(3) for j in range(3)]:
            if i < j:
                distMat[i][j] = distMat[j][i] = findSDist(
                    clusters[i]['median'], clusters[j]['median'])
        # Exchange stage
        Itr = 0
        exchange = True
        while (Itr < maxItr and exchange):
            exchange = False
            for cluster in clusters:
                if len(cluster['dps']) < 2:  # skip clusters with one point
                    continue
                pq = []  # create a list of nearby clusters
                for j in range(p):
                    if cluster['id'] != j:
                        heapq.heappush(pq, (distMat[cluster['id']][j], j))
                bestMove = {'src': -1, 'dst': -1, 'dp': -1, 'costDiff': 0}
                for i in range(len(cluster['dps'])):
                    while j < pec:
                        tmpSrc = (graph['lon'][cluster['dps'][i][0]],
                                  graph['lat'][cluster['dps'][i][0]])
                        tmpDst = heapq.heappop(pq)
                        # weighted distance between the demand point and new cluster median
                        newCost = findDist(
                            tmpSrc, clusters[tmpDst[1]]['median']) * cluster['dps'][i][1]
                        # weighted distance between the demand point and curretn cluster median
                        curCost = findDist(tmpSrc, cluster['median']) * cluster['dps'][i][1]
                        # update bestMove if we have a cost saving move
                        if bestMove['costDiff'] < curCost - newCost:
                            bestMove = {'src': cluster['id'], 'dst': tmpDst[1],
                                        'dp': cluster['dps'][i], 'costDiff': curCost - newCost}
                        j += 1
                if bestMove['costDiff'] > 0:  # if we have a cost saving move, do it!
                    exchange = True
                    clusters[bestMove['src']]['dps'].remove(
                        bestMove['dp'])  # remove the dp from the src cluster
                    clusters[bestMove['dst']]['dps'].append(
                        bestMove['dp'])  # append the dp to the dst clusters
                    # update the center of mass of the src cluster
                    clusters[bestMove['src']]['median'] = findCOM(clusters[bestMove['src']]['dps'])
                    # update the center of mass of the dst cluster
                    clusters[bestMove['dst']]['median'] = findCOM(clusters[bestMove['dst']]['dps'])
            Itr += 1
    return (clusters, Itr)


def findSDist(src, trg):  # finds the src to trg distance in m using haversine formula
    lon1, lat1, lon2, lat2 = map(radians, [src[0], src[1], trg[0], trg[1]])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * 6371 * 1000 * asin(sqrt(a))


def findCOM(nodes):  # finds the geometric center of mas of a set of graph nodes
    x = y = w = 0
    for i, j in nodes:
        x += j*graph['lon'][i]
        y += j*graph['lat'][i]
        w += j
    return (x/w, y/w)


# this is how to call the clustering algorithm
print(findCluster([1453, 10, 456, 178, 876, 8743], [1, 2, 3, 4, 5, 6], 3, .5))
