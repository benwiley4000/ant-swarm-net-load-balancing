"""Code for Node class of Ant-Based Load Balancing."""

import random
import math
from ant import Ant

__author__ = "Ben Wiley and Tommy Rhodes"
__email__ = "bewiley@davidson.edu, torhodes@davidson.edu"

class Node:
    """
    A network node to be traversed by ants and calls.
    """
    
    MAX_LOAD = 40
    NOISE = .05
    
    def __init__(self, num, net_size, neighbors):
        """
        Node Constructor.
        
        Parameters:
            num - int - which number node this is in the network
            net_size - int - number of nodes present in network
            neighbors - seq of ints - adjacent nodes in network
            
        Returns:
            New Node with load of 0 and a single Ant
        """
        
        self.num = num
        self.net_size = net_size
        
        i = 0
        while i < len(neighbors):
        	neighbors[i] = int(neighbors[i])
        	i += 1
        
        self.neighbors = neighbors
        
        self.max_load = Node.MAX_LOAD
        self.load = 0
        self.ants = []
        self.delayed = []
        
        self.p_table = []
        for i in range(0, net_size):
            self.p_table.append([1.0/len(neighbors),] * len(neighbors))
        
        self.new_ant()
        
        self.dead_ants = 0
        self.dead_age = 0
        
        #self.init_phase = True
    
    def add(self, ant):
    	"""
    	Accepts an ant and either adds it to the list of current ants
        or to the list of delayed ants waiting to drop pheromones.
	
    	Parameters:
    		ant - Ant - Ant to be added
	
    	Returns:
    		None
    	"""
        
        delay = int(math.floor(80 * math.exp(-.075 * (self.max_load - self.load))))
        
        if delay == 0:
            
            print "wow got here!! impossible"
            self.add_ant(ant)
            
        else:
            
            self.delayed.append([ant, delay])
    
    def add_ant(self, ant):
    	"""
    	Adds ant to list for this Node and changes probability tables.
	
    	Parameters:
    		ant - Ant - Ant to be added
	
    	Returns:
    		None
    	"""
        
        """ modify p_table """
        delta_p = 0.08 / ant.age + 0.005
        i = ant.source
        j = self.neighbors.index(ant.prev)
        
        #if i == 27 and (self.num == 2 or self.num == 3 or ant.prev == 2 or ant.prev == 3):
			#print "Ant from " + str(ant.prev) + " to " + str(self.num) + " goes from " + str(self.p_table[i][j]) + " to " + str((self.p_table[i][j] + delta_p) / (1.0 + delta_p))
        
        """ increase p for previous node """
        self.p_table[i][j] = (self.p_table[i][j] + delta_p) / (1.0 + delta_p)
        
        """ decrease p for others """
        for k in range(0, j):
            self.p_table[i][k] = (self.p_table[i][k]) / (1.0 + delta_p)
            
        for k in range(j+1, len(self.neighbors)):
            self.p_table[i][k] = (self.p_table[i][k]) / (1.0 + delta_p)
        
        """ set ant's last visted node to current """
        ant.prev = self.num
        
        """ add the ant to this node's ant list, unless arrived.. then kill it. """
        if self.num != ant.dest:
			self.ants.append(ant)
		
        else:
			self.dead_ants += 1
			self.dead_age += ant.age
    
    def new_ant(self):
    	"""
    	Creates new ant and adds it to the Node's ant list.
	
    	Parameters:
    		None
	
    	Returns:
    		None
    	"""
        
        ant = Ant(self.num, random.randint(0, self.net_size - 2))
        
        if ant.dest >= self.num:
            ant.dest += 1
        
        ant.prev = self.num
        
        self.ants.append(ant)
    
    def get_migrants(self):
    	"""
    	Causes time to tick once, and pops list of ants ready to migrate.
        Also adds delayed ants to Node ant list if ready.
	
    	Parameters:
    		None
	
    	Returns:
    		migrants - list of (Ant, int) tuples - each tuple contains
            an Ant and the node it intends to travel to next.
    	"""
        
        """ make all ants in ant list and delay list age by 1 """
        self.tick()
        
        migrants = []
        
        while self.ants:
            
            ant = self.ants.pop()
            
            n = 0
            
            if random.random() < Node.NOISE:# or self.init_phase:
                
                n = self.neighbors[random.randint(0, len(self.neighbors) - 1)]
            
            else:
                
                """
                cumulative = 0.0
                rand = random.random()
                done = False
                
                for i in range(0, len(self.neighbors) - 1):
                    
                    cumulative += self.p_table[ant.dest][i]
                    
                    if rand < cumulative:
                        
                        done = True
                        n = self.neighbors[i]
                
                if not done:
                    
                    n = self.neighbors[-1]
                """
                
                rand = random.random()
                
                for i in range(0, len(self.neighbors)):
                	rand -= self.p_table[ant.dest][i]
                	if rand <= 0:
                		n = self.neighbors[i]
                		break
            
            
            migrants.append((ant, n))
        
        """ migrant set done. refill ant list w/ 0-delay ants before return """
        i = len(self.delayed) - 1
        
        while i >= 0:
            
            if self.delayed[i][1] == 0:
				self.add_ant(self.delayed.pop(i)[0])
			
            i -= 1
                
        self.new_ant()
        
        return migrants
    
    def tick(self):
    	"""
    	Ticks time one interval and marks down delay.
	
    	Parameters:
    		None
	
    	Returns:
    		None
    	"""
        
        for ant in self.ants:
            ant.age += 1
        
        for a in self.delayed:
            """ age ant """
            a[0].age += 1
            """ count down delay by 1 """
            a[1] -= 1
