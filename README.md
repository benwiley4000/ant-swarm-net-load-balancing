# ant-swarm-net-load-balancing

## Implementing an Ant Swarm Intelligence-Based Approach to Balancing Communication Network Loads

By [Ben Wiley](https://github.com/benwiley4000) and [Tommy Rhodes](https://github.com/tommifier)

*May 6, 2015*

The purpose of this project is to implement a swarm intelligence
algorithm in order to solve load balancing in
communications networks. We aim to reproduce the experiments
of [Schoonderwoerd et al.](AntBasedLoadBalancing.pdf), and compare their
decentralized call routing algorithms performance with
routing using a shortest path (breadth-first search) algorithm
and a minimum-weight algorithm (Dijkstras
Algorithm). The decentralized algorithm mimics the
swarm behavior of an ant colony, and uses roaming,
ant-like agents which drop probability pheromones on
nodes in order to influence the travel behavior of fellow
ants and to regulate the paths of calls made across the
network. Each algorithm is evaluated on the basis of
the number of calls dropped. Ignoring time complexity,
Dijkstra performed best, followed by the ant-based
algorithm and then breadth-first search.

### Running
```sh
python client.py
```
[client.py](client.py) outputs [gml files](gml-technical-report.pdf) representing networking loads across a series of ticks as a breadth-first-search (BFS) algorithm is used to distribute network signals. The gml files can be rendered as colored graphs using [Cytoscape](http://www.cytoscape.org/). Dijkstra's algorithm our our ant-based balancing algorithm can be used instead by changing comments in the file.

If this all sounds esoteric and hard to follow, it's because it is. If you just want to see the results of our study, you'd probably rather...

### [View paper](Ant-Based TeX/main.pdf)

### [View poster](poster.jpg)
Presented at May 6, 2015 Davidson College Math & Science Poster Fair

### View GIFS of load balancing in action
* [Ant swarm](ant-animation.gif)
* [Breadth-First Search](bfs-animation.gif)
* [Dijkstra's Algorithm](dijkstra.gif)
