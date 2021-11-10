# VeNIT Lab Challenges for Candidates

#### ***This repository includes the environment for completing tasks requested to be done by VeNIT Lab candidates.***

The document includes the information related to current content and tasks related to this content. You can find  requested tasks below, also please note the following statements.
* The items starting by *[CAUTION]* indicates important points.

* The items starting by *[OUTPUT]* indicates the software's output.

* The items starting by *[DELIVERY]* indicates the files to be delivered.


## Question 1 - Urban Routing in Bilecik

For this challenge, an OSM ("OpenStreetMap") file named "bilecik_modified.osm" is provided for you to work on. OSM is a file format for representing maps. It is originally an XML file which contains ways, buildings, railways etc. To gain insight about how OSM files work, you can use "JOSM" to open the provided file.

***[CAUTION]*** In the remaining part we will use the following abbreviations to describe the challenge:
* ***Node*** for representing the properties named as "node" in the OSM file 
* ***Way*** for representing the properties named as "way" in the OSM file
* ***Checkpoint*** for representing the nodes selected as a vertice of graph.
* ***Tag*** for representing the properties named as "tag" in the OSM file.

***[CAUTION]***  Also note that tags have two values inside: "k" and "v"; where "k" stands for "key" and "v" stands for "value".


**a)** Write a program that generates a graph from the given OSM file.

*The vertices of the graph will be the checkpoints, vertice IDs will be same as checkpoint IDs. Select checkpoints according to the following conditions:*
* Include the nodes that belongs to the ways having 'highway' as a tag (key).
* Exclude the nodes in ways having the tag (value) 'footway'
* Include the nodes at the beginning and end of the ways.
* Include the nodes at the intersection of 2 or more ways.
* Ignore any other nodes which are not mentioned above.

*Edges must be as follows:*
* Edges represent the ways between the checkpoints.
* Edge weights are the length of the ways between the checkpoints.
* Note that the ways between the nodes are straight but ways between the checkpoints may not.

***[CAUTION]*** Check "checkpoints.png" to gain a better understanding of the difference between checkpoints and nodes.

***[OUTPUT]*** The program must output a file that textually represents the graph. How you put the format is up to you. However note that your textual representation may change according to subsection b. Describe your textual representation format in the document.

***[DELIVERY]*** The source code of the program that generates the graph file.

***[DELIVERY]*** Description of the graph generator's usage.

**b)** Write a program to draw your graph. You can use any programming language and libraries/tools to draw your graph.

***[DELIVERY]*** Graph drawer's source code.

***[DELIVERY]*** Description of the graph drawer's usage.

**c)** Write a code in C/C++ which finds the shortest path between two checkpoints. ***Do not use libraries to implement your algorithm. But you can use libraries for other operations.*** The inputs of the code will be:
* Starting checkpoint ID
* Destination checkpoint ID

***[OUTPUT]*** A file that represents the shortest path.

***[DELIVERY]*** Description of the format that represents the shortest path.

***[DELIVERY]*** Shortest path finder's source code.

***[DELIVERY]*** Description of the shortest path finder's usage.

***[DELIVERY]*** Description of your approach for finding the shortest route.

**d)** You will write another program in C/C++ which includes your shortest path finding code. This program will simulate the following scenario:

An autonomous car starts from checkpoint X at time t=0 (t is an integer) and calculates the shortest path to checkpoint Y (Y is the destination). Then it proceeds to the next checkpoint according to its calculation.

At time t > 0, with some probability p, the next road that it wants to use can be closed. If the road is **not** closed, it can proceed to the next checkpoint. However if it is closed, the car should re-calculate the shortest path to its destination. After that it can proceed to the next checkpoint.

When the car is at the last checkpoint before the destination and the road to destination is closed; the program ends.

The inputs for the program must be:
* Starting checkpoint ID
* Destination checkpoint ID
* Random number generator seed. (For generating p)

***[CAUTION]*** You have to calculate p in each t. However you must feed the seed to the generator only once at the beginning. Not at each t.


***[OUTPUT]*** A file. A single line of the file will be in the following format:

```Text
t=T c=C r=R

Where T is the time, C (Checkpoint ID) is the checkpoint the car stays on at that time and R (list) is the route that the car calculated at that time. R must be the route calculated after the decision for closing the road is done. If the road is closed when the car is at the last checkpoint before the destination, then R must be "NONE"
```

***[DELIVERY]*** Source code.

***[DELIVERY]*** Description of the usage.


**e)** ***(BONUS TASK)*** Enhance your graph drawer so it can show the shortest path you found in subsection c.

***[DELIVERY]*** Source code.

***[DELIVERY]*** Description of the usage.