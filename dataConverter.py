# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 12:45:06 2020

@author: ma076216
"""

# Read a csv file with source, target, and length and generate a standard graph
import csv
import json
from os import path

graph = []
nodes = []
dFile = []

# loading the graph from the json file located in .\graph folder
#dirName = path.dirname(__file__)
dirName = "C:/Users/ma076216/Desktop/PhD/research paper/python_code"
fileName = path.join(dirName, 'graph/graph_avg.csv')

# open the CSV input file
with open(fileName, newline='') as csvfile:
    dFile = list(csv.DictReader(csvfile, delimiter=',', quotechar='|'))
    # read the nodes and add them to nodes list
    for row in dFile:
        if (int(row['source']) not in nodes):
            nodes.append(int(row['source']))
        if (int(row['target']) not in nodes):
            nodes.append(int(row['target']))

    # sort the nodes list and initialize the graph
    nodes.sort()
    index = 0
    while index < len(nodes):
        graph.append({'id': index, 'gid': nodes[index],
                      'lat': 0, 'lon': 0, 'nbrs': [], 'dists': [],'TT':[],'bike':[],'walk':[]})
        index += 1

    # update the neighbor nodes in the graph
    for row in dFile:
        s = nodes.index(int(row['source']))
        t = nodes.index(int(row['target']))
        graph[s]['lat'] = float(row['y1'])
        graph[s]['lon'] = float(row['x1'])
        graph[t]['lat'] = float(row['y2'])
        graph[t]['lon'] = float(row['x2'])
        if (t != s):  # edges starting and ending at the same node are useless
            if (t not in graph[s]['nbrs']):
                graph[s]['nbrs'].append(t)
                graph[s]['dists'].append(float(row['length_m']))
            if (s not in graph[t]['nbrs']):
                graph[t]['nbrs'].append(s)
                graph[t]['dists'].append(float(row['length_m']))
                graph[t]['TT'].append(float(row['tt_thodaysec']))
                graph[t]['bike'].append(float(row['Biking travel time']))
                graph[t]['walk'].append(float(row['walking travel time_sec']))

# stroing graph.json file in the graph folder. It will overwrite existing files
fileName = path.join(dirName, 'graph/graph1.json')
with open(fileName, 'w') as fp:
    json.dump(graph, fp)