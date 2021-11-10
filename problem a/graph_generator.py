#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 01:54:45 2021

@author: duma
"""

import numpy as np
import pandas as pd
import regex as re
from math import radians, cos, sin, asin, sqrt
import networkx as nx
import matplotlib.pyplot as plt


graph = {}
vertices_no = 0

### A function to calculate distance between 2 cordinates on earth ###
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

### A function to add vertices to the graph
def add_vertex(v):
  global graph
  global vertices_no
  if v in graph:
    pass
  else:
    vertices_no = vertices_no + 1
    graph[v] = []

# A function adds an edge between vertex v1 and v2 with weight
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
def print_graph():
  global graph
  for vertex in graph:
    for edges in graph[vertex]:
      print(vertex, " -> ", edges[0], " edge weight: ", edges[1])
      
def write_edges_file(file_name):
    global graph
    with open(file_name, 'w') as f:
        for vertex in graph:
            for edges in graph[vertex]:
                line = vertex+' '+str(edges[0])+' '+str(edges[1])+'\n'
                f.write(line)
    f.close()


file = open('bilecik_modified.osm')
lines = file.readlines()

nodes = {} ## a list to hold nodes
way = [] ## a list to hold nodes of ways
ways = {} ## a list to hold ways
checkpoints = [] ## a list to hold checkpoints

way_flag = 0 ## to understand <way is closed by </way>
save_flag = 0 ## to save 

## parsing the file to include only highways
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
            
write_edges_file('graph.txt') ## write the graph into a file