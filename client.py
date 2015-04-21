#!/usr/bin/env python
#import ant
#import node
import random

"""Client code for Artificial Intelligence Final (Ant-Based Load Balancing)."""

__author__ = "Ben Wiley and Tommy Rhodes"
__email__ = "bewiley@davidson.edu, torhodes@davidson.edu"

def send_ant(noise, p_table, age):
    random.seed()
    rand = random.random()
    if rand >= noise: 
        #select random node
        return
    rand = random.random()
    #select node from values in p_table
    #update p_table
    return

def main():
    adj_list = []
    #initialize graph
    #iterate through initialization and nodes
        #send_ant(noise prob, node.p_table, ant.age + length)
            #this updates p_table
    call_list = []
    successful_call_list = []
    lost_call_list = []
    #iterate
        #randomly add calls
        #send_ant(noise prob, node.p_table, ant.age + length)
        #track lost calls
        #when calls end, add to successful_call_list
