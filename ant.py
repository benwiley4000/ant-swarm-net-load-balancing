"""Code for Ant class of Ant-Based Load Balancing."""

""" imports here? """

__author__ = "Ben Wiley and Tommy Rhodes"
__email__ = "bewiley@davidson.edu, torhodes@davidson.edu"

class Ant:
    """
    An ant-like agent which traverses the network.
    """
    
    def __init__(self, source, dest):
        """
        Ant Constructor.
        
        Parameters:
            source - int - number corresponding to source node
            dest - int - number corresponding to destination node
            
        Returns:
            New ant with age of 0
        """
        
        self.source = source
        self.dest = dest
        self.prev = None
        self.age = 0
    
    