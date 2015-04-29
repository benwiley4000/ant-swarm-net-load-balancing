#!/usr/bin/env python

"""Client code for Artificial Intelligence Final (Ant-Based Load Balancing)"""

from ant import Ant
from node import Node
import random

__author__ = "Ben Wiley and Tommy Rhodes"
__email__ = "bewiley@davidson.edu, torhodes@davidson.edu"

def main():
	random.seed()
	
	adj_list = []
	
	"""
	initialize graph by reading in file.
	assumes graph nodes are numbered 0, 1, ... n-1.
	line l (numbered 1, 2, ... n) contains neighbors for node l - 1.
	"""
	with open('adjacency-list.txt') as f:
		lines = f.readlines()
		for line in lines:
			adj_list.append( Node( len( adj_list ), len( lines ), line.split() ) )
	
	coordinates = open("coordinates.txt").readlines()
	i = 0
	while i < len(coordinates):
		coordinates[i] = str(coordinates[i]).split()
		i += 1
	
	#create adjacency list without duplicates
	
	edge_list = []
	
	for node in adj_list:
		edge_list.append( list( node.neighbors ) )
	
	i = 0
	while i < len(edge_list):
		for n in edge_list[i]:
			edge_list[n].remove(i)
		
		i += 1
		
	adj_list[0].load += 1
	adj_list[1].load += 1
	adj_list[13].load += 1
	adj_list[14].load += 1
	results = get_dijkstra_graph(0, adj_list, [[0, 1], [13, 14]])
	print results[0]
	print results[1]
		
def edge_load(a, b, call_routes):
	load = 0
	for call in call_routes:
		prev = call[0]
		i = 1
		while i < len(call):
			if (a == prev and b == call[i]) or (b == prev and a == call[i]):
				load += 1
			
			prev = call[i]
			i += 1
	
	return load


def get_dijkstra_graph(source, adj_list, call_routes):
	nodes = []
	visited = {source: 0}
	distances = {}
	path = {}
	for n in range(len(adj_list)):
		nodes.append(n)
	for n in range(len(adj_list)):
		weights = {}
		for i in adj_list[n].neighbors:
			weights[i] = edge_load(n, i, call_routes)
		distances[n] = weights
	
	while len(nodes) > 0:
		min_node = None
		for node in nodes:
			if node in visited:
				if min_node is None:
					min_node = node
				elif visited[node] < visited[min_node]:
					min_node = node
		
		if min_node is None:
			break
		
		nodes.remove(min_node)
		current_weight = visited[min_node]
		for edge, weight in distances[min_node].iteritems():
			weight = current_weight + weight
			if edge not in visited or weight < visited[edge]:
				visited[edge] = weight
				path[edge] = min_node
	return [visited, path] #path is dijk_graph in route_djikstra
	
def route_dijkstra(source, dest, adj_list, call_routes):
	dijk_graph = get_dijkstra_graph(source, adj_list, call_routes)
	current_node = adj_list[source]
	nodes = []
	while current_node.num != dest:
		if current_node.max_load - current_node.load == 0:
			for n in nodes:
				adj_list[n].load -= 1
				
			return None
	
		nodes.append(current_node.num)
		current_node.load += 1
		current_node = adj_list[dijk_graph[current_node.num]]
	if current_node.max_load - current_node.load == 0:
		for n in nodes:
			adj_list[n].load -= 1
			
		return None
	
	nodes.append(current_node.num)
	current_node.load += 1		
	return nodes

if __name__ == "__main__":
	main()