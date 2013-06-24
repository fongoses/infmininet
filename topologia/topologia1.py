"""

TOPOLOGIA 1

Topologia em Grafo

Configuração:
* 27 switches conectados em um Grafo
* 2 hosts por switch

* Topologia

* Hosts (identificados por 'a' e 'b'):
    * s0: ha0, hb0
    * s1: ha1, hb1
    * s2: ha2, hb2
    * s3: ha3, hb3
    * s4: ha4, hb4
    * s5: ha5, hb5
    * s6: ha6, hb6
    * s7: ha7, hb7
    * s8: ha8, hb8
    * s9: ha9, hb9
    * s10: ha10, hb10
    * s11: ha11, hb11
    * s12: ha12, hb12
    * s13: ha13, hb13
    * s14: ha14, hb14
    * s15: ha15, hb15
    * s16: ha16, hb16
    * s17: ha17, hb17
    * s18: ha18, hb18
    * s19: ha19, hb19
    * s20: ha20, hb20
    * s21: ha21, hb21
    * s22: ha22, hb22
    * s23: ha23, hb23
    * s24: ha24, hb24
    * s25: ha25, hb25
    * s26: ha26, hb26
"""

from mininet.topo import Topo

class Topologia1(Topo):
    "Topologia 1 (Grafo)"

    def __init__(self):
        "Topologia 1 estende Topo"

        # Initialize topology
        Topo.__init__(self)

        # Add Switches
        s0 = self.addSwitch('s0')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        s7 = self.addSwitch('s7')
        s8 = self.addSwitch('s8')
        s9 = self.addSwitch('s9')
        s10 = self.addSwitch('s10')
        s11 = self.addSwitch('s11')
        s12 = self.addSwitch('s12')
        s13 = self.addSwitch('s13')
        s14 = self.addSwitch('s14')
        s15 = self.addSwitch('s15')
        s16 = self.addSwitch('s16')
        s17 = self.addSwitch('s17')
        s18 = self.addSwitch('s18')
        s19 = self.addSwitch('s19')
        s20 = self.addSwitch('s20')
        s21 = self.addSwitch('s21')
        s22 = self.addSwitch('s22')
        s23 = self.addSwitch('s23')
        s24 = self.addSwitch('s24')
        s25 = self.addSwitch('s25')
        s26 = self.addSwitch('s26')


        # Add hosts
        ha0 = self.addHost('ha0')
        hb0 = self.addHost('hb0')

        ha1 = self.addHost('ha1')
        hb1 = self.addHost('hb1')

        ha2 = self.addHost('ha2')
        hb2 = self.addHost('hb2')

        ha3 = self.addHost('ha3')
        hb3 = self.addHost('hb3')

        ha4 = self.addHost('ha4')
        hb4 = self.addHost('hb4')

        ha5 = self.addHost('ha5')
        hb5 = self.addHost('hb5')

        ha6 = self.addHost('ha6')
        hb6 = self.addHost('hb6')

        ha7 = self.addHost('ha7')
        hb7 = self.addHost('hb7')

        ha8 = self.addHost('ha8')
        hb8 = self.addHost('hb8')

        ha9 = self.addHost('ha9')
        hb9 = self.addHost('hb9')

        ha10 = self.addHost('ha10')
        hb10 = self.addHost('hb10')

        ha11 = self.addHost('ha11')
        hb11 = self.addHost('hb11')

        ha12 = self.addHost('ha12')
        hb12 = self.addHost('hb12')

        ha13 = self.addHost('ha13')
        hb13 = self.addHost('hb13')

        ha14 = self.addHost('ha14')
        hb14 = self.addHost('hb14')

        ha15 = self.addHost('ha15')
        hb15 = self.addHost('hb15')

        ha16 = self.addHost('ha16')
        hb16 = self.addHost('hb16')

        ha17 = self.addHost('ha17')
        hb17 = self.addHost('hb17')

        ha18 = self.addHost('ha18')
        hb18 = self.addHost('hb18')

        ha19 = self.addHost('ha19')
        hb19 = self.addHost('hb19')

        ha20 = self.addHost('ha20')
        hb20 = self.addHost('hb20')

        ha21 = self.addHost('ha21')
        hb21 = self.addHost('hb21')

        ha22 = self.addHost('ha22')
        hb22 = self.addHost('hb22')

        ha23 = self.addHost('ha23')
        hb23 = self.addHost('hb23')

        ha24 = self.addHost('ha24')
        hb24 = self.addHost('hb24')

        ha25 = self.addHost('ha25')
        hb25 = self.addHost('hb25')

        ha26 = self.addHost('ha26')
        hb26 = self.addHost('hb26')


        # Add links

        # s0
        self.addLink(s0, s1)
        self.addLink(s0, s2)
        self.addLink(s0, ha0)
        self.addLink(s0, hb0)

        # s1
        self.addLink(s1, s4)
        self.addLink(s1, ha1)
        self.addLink(s1, hb1)

        # s2
        self.addLink(s2, s4)
        self.addLink(s2, s7)
        self.addLink(s2, ha2)
        self.addLink(s2, hb2)

        # s3
        self.addLink(s3, s4)
        self.addLink(s3, s5)
        self.addLink(s3, s9)
        self.addLink(s3, ha3)
        self.addLink(s3, hb3)

        # s4
        self.addLink(s4, s6)
        self.addLink(s4, s14)
        self.addLink(s4, ha4)
        self.addLink(s4, hb4)

        # s5
        self.addLink(s5, s15)
        self.addLink(s5, ha5)
        self.addLink(s5, hb5)

        # s6
        self.addLink(s6, s9)
        self.addLink(s6, s15)
        self.addLink(s6, s22)
        self.addLink(s6, ha6)
        self.addLink(s6, hb6)

        # s7
        self.addLink(s7, s26)
        self.addLink(s7, ha7)
        self.addLink(s7, hb7)

        # s8
        self.addLink(s8, s9)
        self.addLink(s8, s10)
        self.addLink(s8, s26)
        self.addLink(s8, ha8)
        self.addLink(s8, hb8)

        # s9
        self.addLink(s9, s13)
        self.addLink(s9, ha9)
        self.addLink(s9, hb9)

        # s10
        self.addLink(s10, ha10)
        self.addLink(s10, hb10)

        # s11
        self.addLink(s11, s12)
        self.addLink(s11, s26)
        self.addLink(s11, ha11)
        self.addLink(s11, hb11)

        # s12
        self.addLink(s12, ha12)
        self.addLink(s12, hb12)

        # s13
        self.addLink(s13, ha13)
        self.addLink(s13, hb13)

        # s14
        self.addLink(s14, ha14)
        self.addLink(s14, hb14)

        # s15
        self.addLink(s15, s16)
        self.addLink(s15, ha15)
        self.addLink(s15, hb15)

        # s16
        self.addLink(s16, s17)
        self.addLink(s16, ha16)
        self.addLink(s16, hb16)

        # s17
        self.addLink(s17, s18)
        self.addLink(s17, ha17)
        self.addLink(s17, hb17)

        # s18
        self.addLink(s18, s19)
        self.addLink(s18, s20)
        self.addLink(s18, ha18)
        self.addLink(s18, hb18)

        # s19
        self.addLink(s19, s24)
        self.addLink(s19, ha19)
        self.addLink(s19, hb19)

        # s20
        self.addLink(s20, s21)
        self.addLink(s20, ha20)
        self.addLink(s20, hb20)

        # s21
        self.addLink(s21, s22)
        self.addLink(s21, ha21)
        self.addLink(s21, hb21)

        # s22
        self.addLink(s22, s23)
        self.addLink(s22, ha22)
        self.addLink(s22, hb22)

        # s23
        self.addLink(s23, s24)
        self.addLink(s23, ha23)
        self.addLink(s23, hb23)

        # s24
        self.addLink(s24, s25)
        self.addLink(s24, ha24)
        self.addLink(s24, hb24)

        # s25
        self.addLink(s25, ha25)
        self.addLink(s25, hb25)

        # s26
        self.addLink(s26, ha26)
        self.addLink(s26, hb26)


topos = { 'topologia1': (lambda: Topologia1()) }
