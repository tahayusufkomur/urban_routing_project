import collections
import heapq
import sys
from datetime import datetime

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

if __name__ == "__main__":

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
    output =shortestPath(edges, sys.argv[1], sys.argv[2])
    
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    dt_string = dt_string.replace(' ','-')
    dt_string = dt_string.replace('/','-')
    dt_string = dt_string.replace(':','-')
    
    file = open('shortest_path-'+dt_string+'.txt','w')
    
    for ou in output[1]:
    	file.write('->'+ou)
    
    file.write('\n')
    file.write("Distance is: "+str(output[0])+'\n')
    file.close()