#!/usr/bin/env python
from ant import ant
from node import node
import random

"""Client code for Artificial Intelligence Final (Ant-Based Load Balancing)"""

__author__ = "Ben Wiley and Tommy Rhodes"
__email__ = "bewiley@davidson.edu, torhodes@davidson.edu"

"""
def send_ant(noise, p_table, source):
    random.seed()
    rand = random.random()
    next_node = -1
    dest = int(random.randrange(len(adj_list)))
    if rand >= noise: 
        next_node = int(random.randrange(len(adj_list[source].neighbors)))
	while next_node == source:
	    next_node = int(random.randrange(len(adj_list[source].neighbors)))
        return
    rand = random.random()
    copy = adj_list[source].p_table[dest][:]
    while dest == -1:
	if (1 - rand >= max(copy)):
	    next_node = adj_list[source].neighbors[copy.index(max(copy))]
	copy[copy.index(max(copy))] == -1
    
    return
"""

def route_call(source, dest, adj_list):
    current_node = adj_list[source]
    nodes = []
    while current_node.num != dest:
        if current_node.max_load - current_load.load == 0:
            for i in range(len(nodes)):
                adj_list[i].load -= 1
            return -1
        nodes.append(current_node.num)
        current_node.load += 1
	current_node = adj_list[current_node.neighbors[current_node.p_table[current_node.num].max(current_node.p_table[current_node.num])]] #def recheck this later
    return nodes

def start_call(tick):
    source = int(random.randrange(len(adj_list)))
    dest = source
    while dest == source:
	dest = int(random.randrange(len(adj_list)))
    length = -1
    while length < 0:
	length = random.gauss(170, 20)
    return [source, dest, length + tick]

def end_call(route):
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
	f = open("gif/graph-" + t + "t.gml", 'w')
	f.write("graph [\n")
	i = 0
	while i < len(adj_list):
		f.write("\tnode [\n")
		f.write("\t\tid " + i + "\n")
		f.write("\t\tlabel \"" + i + "\"\n")
		f.write("\t\tgraphics [\n")
		f.write("\t\t\tx " + coordinates[i][0] + "\n")
		f.write("\t\t\ty " + coordinates[i][1] + "\n")
		
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
			f.write("\t\t\tfill \"FF9999\"\n")
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
			f.write("\t\tsource " + i + "\n")
			f.write("\t\ttarget " + edge_list[i][j] + "\n")
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

def main():
    random.seed()
    
    adj_list = []
    """
    initialize graph by reading in file.
    assumes graph nodes are numbered 0, 1, ... n-1.
    line l (numbered 1, 2, ... n) contains neighbors for node l - 1.
    """
    with open('adjacency-list.txt') as f:
    	for line in f:
    		adj_list.append( Node( len( adj_list ), len( f ), tuple( line.split() ) ) )
	
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
		for node in range(len(adj_list)):
			break
		#send_ant(noise prob, node.p_table, ant.age + length)
		call_list = []
		call_ends = []
		successful_call_list = []
		lost_call_list = []
		call_routes = []
		call_prob = 0.9
		call_prob_2 = 0.5
		for i in range(10000):
			if i % 100 == 0:
				graph_out(adj_list, edge_list, coordinates, call_routes, i)
			
			if 1 - random.random() >= call_prob:
		    call = start_call()
			    result = route_call()
			    if result == -1:
					lost_call_list.append(call[0:2])
				
			    else:
					successful_call_list.append(call[0:2])
					call_list.append(call[0:2])
					call_ends.append(call[3])
					call_routes.append(result)
			
			elif 1 - random.random() >= call_prob_2:
			    for i in range(2): 
					call = start_call()
					result = route_call()
					if result == -1:
				    	lost_call_list.append(call[0:2])
					else:
				    	successful_call_list.append(call[0:2])
				    	call_list.append(call[0:2])
				    	call_ends.append(call[3])
				    	call_routes.append(result)
			
			while i in call_ends:
			    index = call_ends.index(i)
				call_ends.pop(i)
		 		call_list.pop(i)
		  		end_call(call_routes.pop(i))
		  		#send_ant(noise prob, node.p_table, ant.age + length)