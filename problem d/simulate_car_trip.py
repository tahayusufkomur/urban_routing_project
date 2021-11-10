import collections
import heapq
import random
from numpy import inf
import sys
from datetime import datetime


def shortestPath(edges, source, sink):
    # create a weighted DAG - {node:[(cost,neighbour), ...]}
    graph = collections.defaultdict(list)
    for l, r, c, d in edges:
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
def print_path(path):
    st_path = ""

    for p in path[1]:
            st_path = st_path+'->'+p
    return st_path

if __name__ == "__main__":

    edges = []
    streets = {}
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
        temp_list.append(source+target)
        edges.append(temp_list)
        streets[source+target] = weight
    file.close()

source = sys.argv[1]
target = sys.argv[2]
seed = sys.argv[3]
random.seed(seed)
time = 0

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
dt_string = dt_string.replace(' ','-')
dt_string = dt_string.replace('/','-')
dt_string = dt_string.replace(':','-')

file = open('trip-'+dt_string+'.txt','w')

while source != target:
    
    path = shortestPath(edges, source, target)
    
    if(path == inf):
        print("Unfortunately there is no new path, you need to wait until the way is opened.")
        break
    path_st = print_path(path)
    st = "t= "+str(time)+" c= "+str(source)+" p= "+path_st
    print(st)
    file.write('\n')
    file.write(st+'\n\n')
    
    #for p in path[1]:
     #   print(p, end=' ')

    length = len(path[1])
    for i in range(length):
        
        #print("\ncurrent node is:",source)
        
        if source == target:
            print("\nCongratulations!!! You are at the destination point")
            break

        if(random.random()>0.98):
            hashed_string = source+path[1][i+1]
            for e in edges:
                if e[3]==hashed_string:
                    edges.remove(e)
                    print("\n",e[1]," is closed, looking for a new path \n")
                    time = time + 1
            break;
        
        else:
            source = path[1][i+1]
            time = time+1
            path_st = print_path(path)
            st = "t= "+str(time)+" c= "+str(source)+" p= "+path_st
            print(st)
            file.write('\n')
            file.write(st+'\n\n')
file.close()
