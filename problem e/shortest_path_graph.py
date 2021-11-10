#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 01:54:45 2021

@author: duma
"""
import collections
import heapq
import sys
from matplotlib import pyplot
from math import radians, cos, sin, asin, sqrt
import networkx as nx
import numpy as np
import pandas as pd
import regex as re
from math import radians, cos, sin, asin, sqrt
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

graph = {}
vertices_no = 0

def haversine_distance(lon1, lat1, lon2, lat2, unit_m=True):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    default unit : km
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of the Earth in kilometers. Use 3956 for miles
    if unit_m:
        r *= 1000
    return c * r

def add_vertex(v):
  global graph
  global vertices_no
  if v in graph:
    pass
  else:
    vertices_no = vertices_no + 1
    graph[v] = []

# Add an edge between vertex v1 and v2 with edge weight e
def add_edge(v1, v2, e):
  global graph
  # Check if vertex v1 is a valid vertex
  if v1 not in graph:
    pass
  # Check if vertex v2 is a valid vertex
  elif v2 not in graph:
    pass
  else:
    # Since this code is not restricted to a directed or 
    # an undirected graph, an edge between v1 v2 does not
    # imply that an edge exists between v2 and v1
    temp = [v2, e]
    graph[v1].append(temp)


# Print the graph
      
def write_edges_file(file_name):
    global graph
    with open(file_name, 'w') as f:
        for vertex in graph:
            for edges in graph[vertex]:
                line = vertex+' '+str(edges[0])+' '+str(edges[1])+'\n'
                f.write(line)
    f.close()
    
def shortestPath(edges, source, sink):
    # create a weighted DAG - {node:[(cost,neighbour), ...]}
    graph = collections.defaultdict(list)
    for l, r, c in edges:
        graph[l].append((c,r))
    # create a priority queue and hash set to store visited nodes
    queue, visited = [(0, source, [])], set()
    heapq.heapify(queue)
    # traverse graph with BFS
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        # visit the node if it was not visited before
        if node not in visited:
            visited.add(node)
            path = path + [node]
            # hit the sink
            if node == sink:
                return (cost, path)
            # visit neighbours
            for c, neighbour in graph[node]:
                if neighbour not in visited:
                    heapq.heappush(queue, (cost+c, neighbour, path))
    return float("inf")



if __name__ == '__main__':

    if(len(sys.argv)<3):
        print("Correct usage is: python3 shortest_path_graph.py source target")
        sys.exit()


    file = open('bilecik_modified.osm')
    lines = file.readlines()

    nodes = {}
    way = []
    ways = {}
    checkpoints = []

    way_flag = 0 ## to understand <way is closed by </way>
    save_flag = 0 ## to save

    for line in lines: ## iterate over the osm file 

        if (way_flag == 1):

            if(line.find("k=\'highway\'") != -1): ## if highway
                if(line.find("v=\'footway\'") == -1): ## if not footway
                    save_flag = 1 ## save it when find /way
                    continue
                continue
            
            elif(line.find("</way>")) != -1:

                way_flag = 0
                if(save_flag == 1): ## if we found way closing tag and its highway not footway save
                    ways[way[0]] = way[1:]
                    save_flag = 0
                way = []

            elif(line.find("<nd ref")) != -1:
                
                x = re.findall(r'\d+.\d+',line) ## extract digits from the string
                way.append(x[0])
                if x[0] in nodes.keys():
                    node = nodes[x[0]]
                    node[2] = node[2]+1
                    node.append(way[0])

            
        ## NODE ADDING ##
        elif (line.find("<node id=") != -1): ## if the line starts with <node id

            node = [] 
            x = re.findall(r'\d+.\d+',line) ## extract digits from the string
            node.append(x[-2]) ## lat
            node.append(x[-1]) ## lon
            node.append(0)
            nodes[x[0]] = node ## add to nodes list
        
        ## WAY ID ADDING ##
        elif (line.find("<way id=") != -1 and way_flag == 0): ## if the line starts with <way id    
            x = re.findall(r'\d+.\d+',line)
            way.append(x[0])
            way_flag = 1
            continue

    ## FILL CHECKPOINTS

    checkpoints = []
    for key, value in nodes.items():
        if value[2]>1:
            checkpoints.append(key)
    for key, value in ways.items():
        if len(value) > 0:
            checkpoints.append(value[0])
            checkpoints.append(value[-1])
    myset = set(checkpoints)
    checkpoints = list(myset)
    checkpoints.sort()
    with open('checkpoints.txt', 'w') as f:
        for c in checkpoints:
            f.write(c+'\n')
    f.close()

            
    ## Creating new vertices and edges based on checkpoints
    for key, value in ways.items():
        distance = 0
        length = len(value)
        
        if length < 2: ## means there is a problem with ways list
            continue
        
        start_node = value[0]
        
        if length == 2:
            lat1 = float(nodes[value[0]][0])
            lon1 = float(nodes[value[0]][1])
            lat2 = float(nodes[value[1]][0])
            lon2 = float(nodes[value[1]][1])
            distance = haversine_distance(lon1,lat1,lon2,lat2)
            add_vertex(start_node)
            add_vertex(value[1])
            add_edge(start_node,value[1],distance)
            continue

        for i in range(1,length): ## sum distance between x and x+1, iterate over the list to the end or a checkpoint

            lat1 = float(nodes[value[i-1]][0])
            lon1 = float(nodes[value[i-1]][1])
            lat2 = float(nodes[value[i]][0])
            lon2 = float(nodes[value[i]][1])
            distance += haversine_distance(lon1,lat1,lon2,lat2)
            
            if value[i] in checkpoints:
                add_vertex(start_node)
                add_vertex(value[i])
                add_edge(start_node,value[i],distance)
                distance = 0
                start_node = value[i]
                continue
            elif value[i] == value[-1]:
                add_vertex(start_node)
                add_vertex(value[i])
                add_edge(start_node,value[i],distance)
                continue
                      
    write_edges_file('edges.txt')

    edges = []
    file = open('edges.txt')
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        line = line.split(' ')
        source = str(line[0])
        target = str(line[1])
        weight = int(float(line[2]))
        temp_list = []
        temp_list.append(source)
        temp_list.append(target)
        temp_list.append(weight)
        edges.append(temp_list)
    file.close()

    source = '2024879246'
    target = '8982649767'

    output =shortestPath(edges, sys.argv[1], sys.argv[2])
    if(output == inf):
        print("Unfortunately there is no new path, you need to wait until the way is opened.")
        break
    G=nx.Graph()

    file = open('edges.txt')
    lines = file.readlines()
    for line in lines:
        line = line.split(' ')

        lat1 = nodes[line[0]][0]
        lon1 = nodes[line[0]][1]
        lat2 = nodes[line[1]][0]
        lon2 = nodes[line[1]][1]
        
        G.add_node(line[0],pos=(lat1,lon1))
        G.add_node(line[1],pos=(lat2,lon2))
        if line[0] not in output[1]:
            G.add_edge(line[0],line[1],color='b',weight=1)
        else:
            pass
        
    file.close()


    for i in range(len(output[1])-1):
        G.add_edge(output[1][i],output[1][i+1],color='r',weight=20)

    colors = nx.get_edge_attributes(G,'color').values()
    weights = nx.get_edge_attributes(G,'weight').values()

    my_pos = nx.spring_layout(G, seed = 2) ## seed to keep graph same.
    plt.figure(figsize=(25,25))
    nx.draw(G,my_pos,width=list(weights),edge_color=colors)

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    dt_string = dt_string.replace(' ','-')
    dt_string = dt_string.replace('/','-')
    dt_string = dt_string.replace(':','-')
    print(dt_string)
    plt.savefig(dt_string+'.png')
