#!/usr/bin/env python
#import ant
#import node
import random

"""Client code for Artificial Intelligence Final (Ant-Based Load Balancing)"""

__author__ = "Ben Wiley and Tommy Rhodes"
__email__ = "bewiley@davidson.edu, torhodes@davidson.edu"

def send_ant(noise, p_table, dest):
    random.seed()
    rand = random.random()
    if rand >= noise: 
        next_node = int(random.randrange(len(
        return
    rand = random.random()
    #select node from values in p_table
    #update p_table
    return

def route_call(source, dest, adj_list):
    current_node = adj_list[source]
    nodes = []
    while current_node.num != dest:
        current_node = adj_list[current_node.neighbors[current_node.p_table[current_node.num].max(current_node.p_table[current_node.num])]] #def recheck this later
        if current_node.max_load - current_load.load == 0:
            for i in range(len(nodes)):
                adj_list[i].load -= 1
            return -1
        nodes.append(current_node.num)
        current_node.load += 1
    return [source, dest]

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
    		adj_list.append( Node( len( adj_list ), len( f ), line.split() )
	
    
    #iterate through initialization and nodes
        #send_ant(noise prob, node.p_table, ant.age + length)
            #this updates p_table
    call_list = []
    successful_call_list = []
    lost_call_list = []
    for ("""iterate"""):
        #randomly add calls
        if random.random() >= .9:
            a = int(random.randrange(len(adj_list)) + 1)
            b = int(random.randrange(len(adj_list)) + 1)
            call = route_call(a, b, adj_list)
        #send_ant(noise, node.p_table, dest)
        #track lost calls
        #when calls end, add to successful_call_list
