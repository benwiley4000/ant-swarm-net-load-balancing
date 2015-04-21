#!/usr/bin/env python

"""Code for Node class of Ant-Based Load Balancing."""

""" imports here? """

__author__ = "Ben Wiley and Tommy Rhodes"
__email__ = "bewiley@davidson.edu, torhodes@davidson.edu"

class Node:
    """
    A network node to be traversed by ants and calls.
    """
    
    MAX_LOAD = 30
    NOISE = .05
    
    def __init__(self, num, *neighbors, net_size):
        
        self.num = num
        self.net_size = net_size
        self.neighbors = neighbors
        self.max_load = Node.MAX_LOAD
        self.current = 0
        self.ants = []
        
        self.p_table = []
        
        for i in range(0, net_size):
            
            p_table.append((1.0/len(neighbors),) * len(neighbors))
    
    def add(self, ant):
        
        if self.num != ant.dest:
            
            self.ants.append(ant)
            
            """
            modify p_table
            """
    
    def new_ant(self):
        
        ant = Ant(self.num, random.randint(0, net_size - 2))
        
        if ant.dest == self.num:
            
            ant.dest += 1
        
        self.ants.append(ant)
    
    def get_migrants(self):
        
        migrants = []
        
        i = len(self.ants) - 1
        
        while(i >= 0):
            
            """
            if no delay:
            """
            ant = self.ants.pop(i)
            
            n = 0
            
            if random.random() < Node.NOISE:
                
                n = self.neighbors[random.randint(0, len(self.neighbors) - 1)]
            
            else:
                
                cumulative = 0.0
                rand = random.random()
                done = False
                
                for j in range(0, len(self.neighbors) - 2):
                    
                    cumulative += self.p_table[ant.dest][j]
                    
                    if rand < cumulative:
                        
                        done = True
                        n = self.neighbors[j]
                
                if not done:
                    
                    n = self.neighbors[-1]
            
            migrants.append((ant, n))
        
        return migrants
    
    