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
	
	for i in range(500):
		#print "Tick: " + str(i)
		move_ants(adj_list)
	
	for node in adj_list:
		#print "Node " + str(adj_list.index(node)) + " has " + str(len(node.ants)) + " ready and " + str(len(node.delayed)) + " delayed"
		node.ants = []
		node.delayed = []
		node.new_ant()
	
	print ""
	
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
	
	for i in range(10000):
		#print lost_call_list
		
		if i % 100 == 0:
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
		
		while i in call_ends:
			index = call_ends.index(i)
			call_ends.pop(i)
			call_list.pop(i)
			end_call(call_routes.pop(i))
		
		move_ants(adj_list)

def move_ants(adj_list):
	for node in adj_list:
		migrants = node.get_migrants()
		for migrant in migrants:
			adj_list[migrant[1]].add(migrant[0])

def route_call(source, dest, adj_list):
	label = random.randint(1,1000)
	current_node = adj_list[source]
	nodes = []
	while current_node.num != dest:
		#print "call " + str(label) + ": S: " + str(source) + " D: " + str(dest) + " C: " + str(current_node.num)
		if current_node.max_load - current_node.load == 0:
			for n in nodes:
				adj_list[n].load -= 1
			
			return None
		
		nodes.append(current_node.num)
		current_node.load += 1
		current_node = adj_list[current_node.neighbors[current_node.p_table[dest].index(max(current_node.p_table[dest]))]] #def recheck this later
	
	#print "S: " + str(source) + " D: " + str(dest) + " C: " + str(current_node.num)
	if current_node.max_load - current_node.load == 0:
		for n in nodes:
			adj_list[n].load -= 1
		
		return None
	
	nodes.append(current_node.num)
	current_node.load += 1
	current_node = adj_list[current_node.neighbors[current_node.p_table[dest].index(max(current_node.p_table[dest]))]] #def recheck this later
	
	return nodes

def dijkstra_call(source, dest, adj_list, call_routes):
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
			if temp < edge_weight and edge not in nodes:
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
		if temp < edge_weight and edge not in nodes:
			edge_weight = temp
			edge = n
			
	return nodes

def start_call(tick, adj_list):
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
