"""Custom topology example
Two directly connected switches plus a host for each switch:

	host --- switch --- switch --- host
	
Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):
	"Simple topology example."
	
	def __init__( self ):
		"Create custom topo."
		
		# Initialize topology
		Topo.__init__( self )
		
		# Add hosts and switches
		leftHost = self.addHost( 'h1' )
		rightHost = self.addHost( 'h2' )
		R1 = self.addSwitch( 'r1' )
		R2 = self.addSwitch( 'r2' )
		R3 = self.addSwitch( 'r3' )
		R4 = self.addSwitch( 'r4' )
		R5 = self.addSwitch( 'r5' )
		
		# Add links
		self.addLink( leftHost, R1 )
		self.addLink( R1, R2 )
		self.addLink( R1, R3 )
		self.addLink( R1, R4 )
		self.addLink( R2, R5 )
		self.addLink( R2, R3 )
		self.addLink( R3, R5 )
		self.addLink( R3, R4 )
		self.addLink( R4, R5 )
		self.addLink( R5, rightHost )
		
topos = { 'mytopo': ( lambda: MyTopo() ) }