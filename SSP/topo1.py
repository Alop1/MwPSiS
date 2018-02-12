from mininet.topo import Topo

class MyTopo( Topo ):

    def __init__( self ):
        "Create custom topo."
        # Initialize topology
        Topo.__init__( self )


        # Add hosts and switches
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        S1 = self.addSwitch( 's1' )
        S2 = self.addSwitch( 's2' )
        S3 = self.addSwitch( 's3' )
        S4 = self.addSwitch( 's4' )
        S5 = self.addSwitch( 's5' )

        # Add links
        self.addLink( leftHost, S1 )
        self.addLink( S1, S2 )
        self.addLink( S1, S3 )
        self.addLink( S1, S4 )
        self.addLink( S2, S3 )
        self.addLink( S2, S5 )
        self.addLink( S3, S5 )
        self.addLink( S4, S3 )
        self.addLink( S4, S5 )
        self.addLink( S5, rightHost )
        topos = { 'mytopo': ( lambda: MyTopo() ) }
