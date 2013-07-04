from pox.core import core
from pox.lib.addresses import EthAddr, IPAddr
from pox.lib.util import dpid_to_str 
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt # POX convention
import pox.openflow.l2_learning as l2
import pox.openflow.spanning_tree as spat
import pox.openflow.discovery as dscv
log = core.getLogger()
#lista de testes

teste =1
#A cada pacote recebido, realiza o roteamento. Ora chamamos de switch multicast, ora de roteador multicast
class RoteadorMulticast(object):
	controllerConnection = {}
	def __init__ (self,connection):
		
		#guarda referencia da conexao para futuras referencias nos envios de novas mensagens openflow para esse switch multicast		
		controllerConnection = connection

		#connection representa o switch sobre o qual serah criado o controle multicast
		core.openflow.addListeners(self)

		#Tabela de Ips Multicast
		self.tabelaMulticast = {}

		

		#adiciona Listener (essa propria classe)  sobre a conexao.
		#O listener serah disparado a cada novo pacote
		connection.addListeners(self)
		  
	#As acoes do listener sao descritas atraves do metodo definido na interface
	#para tratamento de pacotes de entrada. Esse metodo eh o descrito abaixo:
	#_handle_PacketIn
	def _handle_PacketIn(self,event):
		
		packet_ll=event.parsed #obtem pacote 
		#core.RTSPMulticast.packetlist.append(packet_ll)
		
		#Registra pacote atual no grupo
		def registraNoGrupo(Packet,Grupo): 
			#Faz um match, testando se a porta eh 554

			#se deu match, registra ip de origem na tabela multicast
			#formato da tabela: 
			#   ---------------------------------------
			#   |IP_DO_HOST | IDENTIFICADOR/IP_DO_GRUPO|
			#   ----------------------------------------
			packet_linklayer = Packet
			if isinstance(packet_linklayer, pkt.ethernet):
				packet_nwlayer = packet_linklayer.payload
				if isintance(packet_linklayer,pkt.arp):
					print "Pacote ARp"
				if isinstance(packet_linklayer, pkt.ipv4):
					packet_transportlayer=packet_nwlayer.payload				
					if isinstance(packet_transportlayer, pkt.tcp):
						if packet_transportlayer.dstport == 554:
							core.RTSPMulticast.packetlist.append(packet_transportlayer)
							self.tabelaMulticast[packet_nwlayer.ipsrc] == Grupo #nessa nossa implementacao ha apenas o grupo identificado por 1
													
							
					
		registraNoGrupo(packet_ll,1)
		def encaminhaPacote(Packet,Grupo):
			foo=1
			#Grupo
			#for ip in self.tabelaMulticast
			#    pacoteMulticast = of.ofp_packet_out() #evento para encaminhamento de pacote

class RTSPMulticast(object):
	packetlist = []
	RoteadorMulticast = {}
	macToPort = {}
	
	def __init__(self):
		core.openflow.addListeners(self) #a propria classe que implementa eh um listener que trabalha com a interface _handle_ConnectionUp
        
    
     
	def _handle_ConnectionUp (self, event):
		self.DPID = dpid_to_str(event.dpid)
		#print dir(self)
		log.debug("Switch %s has come up.", self.DPID)
		if(self.DPID == "00-00-00-00-00-01"):
			RoteadorMulticast = RoteadorMulticast(event.connection) #salvei a referencia do switch multicast para poder acessar sua tabela no interpretador ( por core.RTSPMulticast.RoteadorMulticast.tabelaMulticast )   
			print 'Switch Multicast [ '+self.DPID+' ] Conectado' 
		else:
			l2.LearningSwitch(event.connection,transparent=False)
			print 'Switch l2 [ '+self.DPID+' ] Conectado'


def setSwitchMulticast(tree,SWMulticast):
	print 'Configurando Switches...'
	
	encaminhaARP(SWMulticast)
	encaminhaUDP(SWMulticast)
	encaminhaTCP(SWMulticast)

	
		

#Envia mensagem openflow 'flow_mod' para encaminhamento dos pacotes arps no switch multicast
def encaminhaARP(SwitchMulticast):

	msg = of.ofp_flow_mod() #mensagem flow_mod especifica alteracao na tabela de um switch
	msg.priority = 42 #prioridade. Maior o valor, maior a prioridade.
	msg.match.dl_type = pkt.ethernet.ARP_TYPE#0x806 tipo do protocolo do nivel de rede. ARP
	msg.match.nw_dst = "10.0.0.1/24"
	msg.actions.append(of.ofp_action_output(port=1)) #dados do ip/porta em questao serao encaminhados na(s) porta(s) 'port'
	
	#mensagem que indica ao switch para encaminhar pacotes com origem no servidor para o destino ao qual ele busca
	msg2 = of.ofp_flow_mod() #mensagem flow_mod especifica alteracao na tabela de um switch
	msg.priority = 42 #prioridade. Maior o valor, maior a prioridade.
	msg.match.dl_type = pkt.ethernet.ARP_TYPE#0x806 tipo do protocolo do nivel de rede. ARP
	msg.match.nw_src = "10.0.0.1/24"
	msg.actions.append(of.ofp_action_output(port=1)) #dados do ip/porta em questao serao encaminhados na(s) porta(s) 'port'


	
def encaminhaUDP(SwitchMulticast):
	msg = of.ofp_flow_mod() #mensagem flow_mod especifica alteracao na tabela de um switch
	msg.priority = 42 #prioridade. Maior o valor, maior a prioridade.
	msg.match.dl_type = pkt.ethernet.IP_TYPE #0x800 = IPv4
	msg.match.nw_proto = pkt.ipv4.UPD_PROTOCOL
	msg.match.nw_dst = "10.0.0.1/24"
	msg.actions.append(of.ofp_action_output(port=1)) #dados do ip/porta em questao serao encaminhados na(s) porta(s) 'port'

	#mensagem que indica ao switch para encaminhar pacotes com origem no servidor para o destino ao qual ele busca
	#Verificar tabela Multicast e encaminhar o pacote para as portas correspondentes a cada um dos grupos
	msg2 = msg = of.ofp_flow_mod() #mensagem flow_mod especifica alteracao na tabela de um switch
	msg.priority = 42 #prioridade. Maior o valor, maior a prioridade.
	msg.match.dl_type = pkt.ethernet.ARP_TYPE#0x806 tipo do protocolo do nivel de rede. ARP
	msg.match.nw_src = "10.0.0.1/24"
	msg.actions.append(of.ofp_action_output(port=1)) #dados do ip/porta em questao serao encaminhados na(s) porta(s) 'port'




def encaminhaTCP(SwitchMulticast):
	msg = of.ofp_flow_mod() #mensagem flow_mod especifica alteracao na tabela de um switch
	msg.priority = 42 #prioridade. Maior o valor, maior a prioridade.
	msg.match.dl_type = pkt.ethernet.IP_TYPE #0x800 = IPv4
	msg.match.nw_proto = pkt.ipv4.UPD_PROTOCOL
	msg.match.nw_dst = "10.0.0.1/24"
	msg.actions.append(of.ofp_action_output(port=1)) #dados do ip/porta em questao serao encaminhados na(s) porta(s) 'port'


def launch ():
	core.registerNew(RTSPMulticast)
	dscv.launch()
	spat.launch() #launch spanning tree module
	print 'Spanning tree gerada'
	tree = spat._calc_spanning_tree()
	setSwitchMulticast(tree,RTSPMulticast.RoteadorMulticast)
	#print dir(tree)


