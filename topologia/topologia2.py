"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class topoLuciano1( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        h11 = self.addHost( 'h11' )
        h12 = self.addHost( 'h12' )
        h13 = self.addHost( 'h13' )
        h21 = self.addHost( 'h21' )
        h22 = self.addHost( 'h22' )
        h23 = self.addHost( 'h23' )
	h31 = self.addHost( 'h31' )
        h32 = self.addHost( 'h32' )
        h33 = self.addHost( 'h33' )

	s1 = self.addSwitch( 's3' )
	s2 = self.addSwitch( 's3' )
	s3 = self.addSwitch( 's3' )

        # Add links
        self.addLink( h11, s1 )
        self.addLink( h12, s1 )
        self.addLink( h13, s1 )
        self.addLink( h21, s2 )
        self.addLink( h22, s2 )
        self.addLink( h23, s2 )
        self.addLink( h31, s3 )
        self.addLink( h32, s3 )
        self.addLink( h33, s3 )



topos = { 'topoluciano1': ( lambda: topoLuciano1() ) }
