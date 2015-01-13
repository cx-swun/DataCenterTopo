"""
Data center topology example

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology.Enables each one to pass in '--topo=<key>' from the command line.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.node import Controller,Node                                                                    

import os          


class Fat_tree( Topo ):
      """
      A fat tree topology built using k-port switches can support up to 
      :math:`(k^3)/4` hosts. This topology comprises k pods with two layers of 
      :math:`k/2` switches each. In each pod, each aggregation switch is
      connected to all the :math:`k/2` edge switches and each edge switch is
      connected to :math:`k/2` hosts. There are :math:`(k/2)^2` core switches,
      each of them connected to one aggregation switch per pod.
      Parameters
      ----------
      k : int
          The number of ports of the switches
      """
	
    def __init__( self , k=2 ):
        "Create custom topo."

	c = []
        a = []
        e = []
	s = []
        # Initialize topology
        Topo.__init__( self )

	k=int(k)
	# validate input arguments
    	if k < 1 or k % 2 == 1:
        	raise ValueError('k must be a positive even integer')

    	# Create core nodes
    	n_core = (k//2)**2
	for i in range(n_core):
		sw=self.addSwitch( 'c{}'.format( i ) )
		c.append( sw )
		s.append( sw )

    	# Create aggregation and edge nodes and connect them
    	for pod in range(k):
        	aggr_start_node = self.g.__len__()
        	aggr_end_node = aggr_start_node + k//2
        	edge_start_node = aggr_end_node
        	edge_end_node = edge_start_node + k//2
        	aggr_nodes = range(aggr_start_node, aggr_end_node)
        	edge_nodes = range(edge_start_node, edge_end_node)
		for i in aggr_nodes:
        		sw=self.addSwitch( 'a{}'.format( i ) )
			a.append( sw )
			s.append( sw )
		for j in edge_nodes:
        		sw=self.addSwitch( 'e{}'.format( j ) )
			e.append( sw )
			s.append( sw )
		for aa in aggr_nodes: 
			for ee in edge_nodes:
 				self.addLink(s[aa], s[ee]) 
    	# Connect core switches to aggregation switches
    	for core_node in range(n_core):
        	for pod in range(k):
        	    aggr_node = n_core + (core_node//(k//2)) + (k*pod)
        	    self.addLink(s[core_node], s[aggr_node])
    	# Create hosts and connect them to edge switches
    	count = 0
        for sw in e:
                for i in range(k/2):
                	host = self.addHost( 'h{}'.format( count ) )
                	self.addLink( sw, host )
                	count += 1
   
topos = { 'fattree': Fat_tree }
   
