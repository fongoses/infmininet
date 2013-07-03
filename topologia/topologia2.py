"""

TOPOLOGIA 2

Topologia em Arvore

Configuracao:
* 13 switches conectados em arvore
* 2 hosts por switch

* Topologia
                  s0
                  |
    +-------------+-------------+
    |             |             |
    s1            s2            s3
    |             |             |
+---+---+     +---+---+     +---+---+
|   |   |     |   |   |     |   |   |
s11 s12 s13   s21 s22 s23   s31 s32 s33

* Hosts (identificados por 'a' e 'b'):
    * s0: ha0, hb0
        * s1: ha1, hb1
            * s11: ha11, hb11
            * s12: ha12, hb12
            * s13: ha13, hb13
        * s2: ha2, hb2
            * s21: ha21, hb21
            * s22: ha22, hb22
            * s23: ha23, hb23
        * s3: ha3, hb3
            * s31: ha31, hb31
            * s32: ha32, hb32
            * s33: ha33, hb33
"""

from mininet.topo import Topo

class Topologia2(Topo):
    "Topologia 2 (Arvore)"

    def __init__(self):
        "Topologia 2 estende Topo"

        # Initialize topology
        Topo.__init__(self)

        # Add Switches
        s0 = self.addSwitch('s0')


        s1 = self.addSwitch('s1') #s1 gera dpid 1, s2 gera dpid2, etc.
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s11 = self.addSwitch('s11')
        s12 = self.addSwitch('s12')
        s13 = self.addSwitch('s13')
        s21 = self.addSwitch('s21')
        s22 = self.addSwitch('s22')
        s23 = self.addSwitch('s23')
        s31 = self.addSwitch('s31')
        s32 = self.addSwitch('s32')
        s33 = self.addSwitch('s33')


        # Add hosts
        ha0 = self.addHost('ha0')
	#ha0.setIP('224.0.0.1')
        hb0 = self.addHost('hb0')
        ha1 = self.addHost('ha1')
        hb1 = self.addHost('hb1')

        ha2 = self.addHost('ha2')
        hb2 = self.addHost('hb2')

        ha3 = self.addHost('ha3')
        hb3 = self.addHost('hb3')

        ha11 = self.addHost('ha11')
        hb11 = self.addHost('hb11')

        ha12 = self.addHost('ha12')
        hb12 = self.addHost('hb12')

        ha13 = self.addHost('ha13')
        hb13 = self.addHost('hb13')

        ha21 = self.addHost('ha21')
        hb21 = self.addHost('hb21')

        ha22 = self.addHost('ha22')
        hb22 = self.addHost('hb22')

        ha23 = self.addHost('ha23')
        hb23 = self.addHost('hb23')

        ha31 = self.addHost('ha31')
        hb31 = self.addHost('hb31')

        ha32 = self.addHost('ha32')
        hb32 = self.addHost('hb32')

        ha33 = self.addHost('ha33')
        hb33 = self.addHost('hb33')


        # Add links

        # s0
        self.addLink(s0, s1)
        self.addLink(s0, s2)
        self.addLink(s0, s3)
        self.addLink(s0,ha0)
        self.addLink(s0,hb0)

        # s1
        self.addLink(s1, s11)
        self.addLink(s1, s12)
        self.addLink(s1, s13)
        self.addLink(s1, ha1)
        self.addLink(s1, hb1)

        # s2
        self.addLink(s2, s21)
        self.addLink(s2, s22)
        self.addLink(s2, s23)
        self.addLink(s2, ha2)
        self.addLink(s2, hb2)

        # s3
        self.addLink(s3, s31)
        self.addLink(s3, s32)
        self.addLink(s3, s33)
        self.addLink(s3, ha3)
        self.addLink(s3, hb3)

        # s11
        self.addLink(s11, ha11)
        self.addLink(s11, hb11)

        # s12
        self.addLink(s12, ha12)
        self.addLink(s12, hb12)

        # s13
        self.addLink(s13, ha13)
        self.addLink(s13, hb13)

        # s21
        self.addLink(s21, ha21)
        self.addLink(s21, hb21)

        # s22
        self.addLink(s22, ha22)
        self.addLink(s22, hb22)

        # s23
        self.addLink(s23, ha23)
        self.addLink(s23, hb23)

        # s31
        self.addLink(s31, ha31)
        self.addLink(s31, hb31)

        # s32
        self.addLink(s32, ha32)
        self.addLink(s32, hb32)

        # s33
        self.addLink(s33, ha33)
        self.addLink(s33, hb33)


topos = { 'topologia2': (lambda: Topologia2()) }
