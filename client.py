#!/usr/bin/env python

"""Client code for Artificial Intelligence Final (Ant-Based Load Balancing)"""

from ant import Ant
from node import Node
import random
import sys

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
	
	for i in range(500):
		#print "Tick: " + str(i)
		move_ants(adj_list)
	
	total_ants = 0
	total_dead = 0
	total_age = 0
	for node in adj_list:
		print "Node " + str(adj_list.index(node)) + " has " + str(len(node.ants)) + " ready and " + str(len(node.delayed)) + " delayed"
		total_ants += len(node.ants) + len(node.delayed)
		total_dead += node.dead_ants
		total_age += node.dead_age
		node.ants = []
		node.delayed = []
		node.new_ant()
	
	print "Total current ants: " + str(total_ants)
	print "Average lifespan: " + str(total_age / total_dead)
	
	for node in adj_list:
		print "NODE " + str(adj_list.index(node))
		k = 0
		while k < len(node.p_table):
			print str(k) + " " + str(node.p_table[k])
			k += 1
		
		print ""
	
	call_list = []
	call_ends = []
	successful_call_list = []
	lost_call_list = []
	call_routes = []
	call_prob = 0.9
	call_prob_2 = 0.5
	
	f_lost = open("ant-lost.txt", 'w')
	
	for i in range(10001):
		#print lost_call_list
		
		if i % 1 == 0: #was i % 100
			graph_out(adj_list, edge_list, coordinates, call_routes, i)
		
		if random.random() < call_prob:
			call = start_call(i, adj_list)
			
			source = random.randint(0, len(adj_list) - 1)
			dest = source
			while dest == source:
				dest = random.randint(0, len(adj_list) - 1)
			
			result = route_call(source, dest, adj_list)
			if result:
				successful_call_list.append(call[0:2])
				call_list.append(call[0:2])
				call_ends.append(call[2])
				#print "I am appending " + str(result) + " (" + str(source) + ", " + str(dest) + ")"
				call_routes.append(result)
			
			else:
				lost_call_list.append(call[0:2])
				#print "Call lost at " + str(i) + " ticks."
				f_lost.write(str(i) + "\n")
		
		elif random.random() < call_prob_2:
			for k in range(2): 
				call = start_call(i, adj_list)
				
				source = random.randint(0, len(adj_list) - 1)
				dest = source
				while dest == source:
					dest = random.randint(0, len(adj_list) - 1)
				
				result = route_call(source, dest, adj_list)
				if result:
					successful_call_list.append(call[0:2])
					call_list.append(call[0:2])
					call_ends.append(call[2])
					#print "I am appending " + str(result) + " (" + str(source) + ", " + str(dest) + ")"
					call_routes.append(result)
				
				else:
					lost_call_list.append(call[0:2])
					f_lost.write(str(i) + "\n")
					#print "Call lost at " + str(i) + " ticks."
			
		
		while i in call_ends:
			index = call_ends.index(i)
			call_ends.pop(index)
			call_list.pop(index)
			end_call(call_routes.pop(index), adj_list)
		
		move_ants(adj_list)
	
	f_lost.close()
    
	print "Number of successful calls: " + str(len(successful_call_list))
	print "Number of lost calls: " + str(len(lost_call_list))
	print "Total number of calls: " + str(len(successful_call_list) + len(lost_call_list))
	
def move_ants(adj_list):
	for node in adj_list:
		migrants = node.get_migrants()
		for migrant in migrants:
			adj_list[migrant[1]].add(migrant[0])

def route_call(source, dest, adj_list):
	#label = random.randint(1,1000)
	current_node = adj_list[source]
	nodes = []
	while current_node.num != dest:
		#print "call " + str(label) + ": S: " + str(source) + " D: " + str(dest) + " C: " + str(current_node.num)
		if current_node.max_load - current_node.load == 0:
			#print "Source: " + str(source) + ", Dest: " + str(dest)
			#print nodes
			for n in nodes:
				adj_list[n].load -= 1
			
			return None
		
		nodes.append(current_node.num)
		current_node.load += 1
		current_node = adj_list[current_node.neighbors[current_node.p_table[dest].index(max(current_node.p_table[dest]))]] #def recheck this later
	
	#print "S: " + str(source) + " D: " + str(dest) + " C: " + str(current_node.num)
	if current_node.max_load - current_node.load == 0:
		#print "Source: " + str(source) + ", Dest: " + str(dest)
		#print nodes
		for n in nodes:
			adj_list[n].load -= 1
		
		return None
	
	nodes.append(current_node.num)
	current_node.load += 1
	current_node = adj_list[current_node.neighbors[current_node.p_table[dest].index(max(current_node.p_table[dest]))]] #def recheck this later
	
	return nodes

"""
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
	
def not_dijkstra(source, dest, adj_list, call_routes):
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

def min_in_q(dist, q):
    d = dist[:]
    u = d.index(min(d))
    while u not in q:
        d[u] = sys.maxint
        u = d.index(min(d))
    
    return u
"""

def route_dijkstra(source, dest, adj_list):
    # MODIFIED VERSION OF DIJKSTRA: uses v.load rather than load(u, v)
    # Node loads are more useful metric here than edge weight
    dist = [sys.maxint] * len(adj_list) # all (except S) start w/ infinite dist
    dist[source] = 0 # distance for source node is 0
    prev = [None] * len(adj_list) # all previous nodes are initially undefined
    q = range(0, len(adj_list)) # add all nodes initially
    
    while q:
        u = min_in_q(dist, q)
        if u == dest:
            break
        
        q.remove(u)
        
        for v in adj_list[u].neighbors:
            if v in q:
                alt = dist[u] + adj_list[v].load
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
    
    path = []
    u = dest
    while prev[u] or prev[u] == 0:
        path = [u] + path
        u = prev[u]
    
    for n in path:
        if adj_list[n].max_load <= adj_list[n].load:
            print "Call lost at node: " + str(n) + " with load " + str(adj_list[n].load)
            return None
    
    for n in path:
        adj_list[n].load += 1
    
    return path

def backtrace(source, dest, parent):
	path = [dest]
	while path[-1] != source:
		path.append(parent[path[-1]])
	path.reverse()
	return path

def bfs(source, dest, adj_list):
	parent = {}
	queue = []
	visited = []
	queue.append(source)
	visited.append(source)
	while len(queue) > 0:
		node = queue.pop(0)
		if node == dest:
			path = backtrace(source, dest, parent)
			for n in path:
				if adj_list[n].max_load - adj_list[n].load == 0:
					return None
			for n in path:
				adj_list[n].load += 1
			return path
		for n in adj_list[node].neighbors:
			if n not in visited:
				parent[n] = node
				queue.append(n)
				visited.append(n)
	return None

"""
def other_routing(source, dest, adj_list, call_routes):
	current_node = adj_list[source]
	nodes = []
	while current_node.num != dest:
		if current_node.max_load - current_node.load == 0:
			for n in nodes:
				adj_list[n].load -= 1
				
			return None
		
		nodes.append(current_node.num)
		current_node.load += 1
		edge_weight = 1000
		edge = None
		for n in current_node.neighbors:
			temp = edge_load(current_node.num, n, call_routes)
			if temp < edge_weight and n not in nodes:
				edge_weight = temp
				edge = n
		current_node = adj_list[n]
	if current_node.max_load - current_node.load == 0:
		for n in nodes:
			adj_list[n].load -= 1
			
		return None
	
	nodes.append(current_node.num)
	current_node.load += 1
	edge_weight = 1000
	edge = None
	for n in current_node.neighbors:
		temp = edge_load(current_node.num, n, call_routes)
		if temp < edge_weight and n not in nodes:
			edge_weight = temp
			edge = n
			
	return nodes
"""

def start_call(tick, adj_list):
	source = int(random.randrange(len(adj_list)))
	dest = source
	while dest == source:
		dest = int(random.randrange(len(adj_list)))
		length = -1
	while length < 0:
		length = int(random.gauss(170, 20))
	return [source, dest, length + tick]

def end_call(route, adj_list):
	for i in route:
		adj_list[i].load -= 1

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

def graph_out(adj_list, edge_list, coordinates, call_routes, t):
	f = open("gif/graph-" + str(t) + "t.gml", 'w')
	f.write("graph [\n")
	i = 0
	while i < len(adj_list):
		f.write("\tnode [\n")
		f.write("\t\tid " + str(i) + "\n")
		f.write("\t\tlabel \"" + str(i) + "\"\n")
		f.write("\t\tgraphics [\n")
		f.write("\t\t\tx " + str(coordinates[i][0]) + "\n")
		f.write("\t\t\ty " + str(coordinates[i][1]) + "\n")
		
		if adj_list[i].load < 10:
			#green
			f.write("\t\t\tfill \"#CCFF99\"\n")
		elif adj_list[i].load < 20:
			#yellow
			f.write("\t\t\tfill \"#FFFF66\"\n")
		elif adj_list[i].load < 30:
		#orange
			f.write("\t\t\tfill \"#FFCC66\"\n")
		elif adj_list[i].load < 40:
			#red
			f.write("\t\t\tfill \"#FF9999\"\n")
		else:
			#violet
			f.write("\t\t\tfill \"#FF99FF\"\n")
		
		f.write("\t\t\tw 40.0000\n")
		f.write("\t\t\th 40.0000\n")
		f.write("\t\t\ttype \"Ellipse\"\n")
		f.write("\t\t\tnodeFontSize 22\n")
		f.write("\t\t\toutline \"#000000\"\n")
		f.write("\t\t\tnodeLabelColor \"#000000\"\n")
		f.write("\t\t]\n")
		f.write("\t]\n")
		i += 1
	
	i = 0
	while i < len(edge_list):
		j = 0
		while j < len(edge_list[i]):
			f.write("\tedge [\n")
			f.write("\t\tsource " + str(i) + "\n")
			f.write("\t\ttarget " + str(edge_list[i][j]) + "\n")
			f.write("\t\tgraphics [\n")
			
			load = edge_load(i, edge_list[i][j], call_routes)
			
			if load < 10:
				#green
				f.write("\t\t\tfill \"#CCFF99\"\n")
			elif load < 20:
				#yellow
				f.write("\t\t\tfill \"#FFFF66\"\n")
			elif load < 30:
				#orange
				f.write("\t\t\tfill \"#FFCC66\"\n")
			elif load < 40:
				#red
				f.write("\t\t\tfill \"#FF9999\"\n")
			else:
				#violet
				f.write("\t\t\tfill \"#FF99FF\"\n")
			
			f.write("\t\t]\n")
			f.write("\t]\n")
			j += 1
		
		i += 1
	
	f.write("]")
	f.close()
	print("Wrote to gif/graph-" + str(t) + "t.gml!")

if __name__ == "__main__":
	main()
