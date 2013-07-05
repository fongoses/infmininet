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
roteadorMulticast = None
tree = None
#A cada pacote recebido, realiza o roteamento. Ora chamamos de switch multicast, ora de roteador multicast
class RoteadorMulticast(object):
	#controllerConnection = None
	def __init__ (self,connection):
		
		#guarda referencia da conexao para futuras referencias nos envios de novas mensagens openflow para esse switch multicast		
		self.controllerConnection = connection

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
				if isinstance(packet_linklayer,pkt.arp):
					print "Pacote ARp"
				if isinstance(packet_linklayer, pkt.ipv4):
					packet_transportlayer=packet_nwlayer.payload				
					if isinstance(packet_transportlayer, pkt.tcp):
						if packet_transportlayer.dstport == 554:
							core.RTSPMulticast.packetlist.append(packet_transportlayer)
							self.tabelaMulticast[packet_nwlayer.ipsrc] == Grupo #nessa nossa implementacao ha apenas o grupo identificado por 1
							print "Inscrito no grupo"
													
							
					
		registraNoGrupo(packet_ll,1)
		def encaminhaPacote(Packet,Grupo):
			foo=1
			#Grupo
			#for ip in self.tabelaMulticast
			#    pacoteMulticast = of.ofp_packet_out() #evento para encaminhamento de pacote

class RTSPMulticast(object):
	global roteadorMulticast
	packetlist = []
	#tree = None

	macToPort = {}
	print "OI eu sou RTSPMulticast"
	def __init__(self):
		core.openflow.addListeners(self) #a propria classe que implementa eh um listener que trabalha com a interface _handle_ConnectionUp    
         
	def _handle_ConnectionUp (self, event):
		global roteadorMulticast
		self.DPID = dpid_to_str(event.dpid)
		#print dir(self)
		log.debug("Switch %s has come up.", self.DPID)
		if(self.DPID == "00-00-00-00-00-01"):
			roteadorMulticast = RoteadorMulticast(event.connection) #salvei a referencia do switch multicast para poder acessar sua tabela no interpretador ( por core.RTSPMulticast.RoteadorMulticast.tabelaMulticast ) 		
			print 'Switch Multicast [ '+self.DPID+' ] Conectado'
			print roteadorMulticast
		else:
			l2.LearningSwitch(event.connection,transparent=False)
			print 'Switch l2 [ '+self.DPID+' ] Conectado'
			#print roteadorMulticast


#Envia mensagem openflow 'flow_mod' para encaminhamento dos pacotes arps no switch multicast
def encaminhaARP(SwitchMulticast):
	msg = of.ofp_flow_mod() #mensagem flow_mod especifica alteracao na tabela de um switch

	#msg.priority = 42 #prioridade. Maior o valor, maior a prioridade.
	msg.match.dl_type = pkt.ethernet.ARP_TYPE#0x806 tipo do protocolo do nivel de rede. ARP
	msg.match.nw_dst = IPAddr("10.0.0.1")
	msg.actions.append(of.ofp_action_output(port=1)) #dados do ip/porta em questao serao encaminhados na(s) porta(s) 'port'
	print "Connection"
	
	if SwitchMulticast:
		SwitchMulticast.controllerConnection.send(msg)
	else:
		print "Null Multicast"
			
	#mensagem que indica ao switch para encaminhar pacotes com origem no servidor para o destino ao qual ele busca
	msg2 = of.ofp_flow_mod() #mensagem flow_mod especifica alteracao na tabela de um switch
	msg2.priority = 42 #prioridade. Maior o valor, maior a prioridade.
	msg2.match.dl_type = pkt.ethernet.ARP_TYPE#0x806 tipo do protocolo do nivel de rede. ARP
	msg2.match.nw_src = IPAddr("10.0.0.1")
	msg2.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD)) #dados do ip/porta em questao serao encaminhados na(s) porta(s) 'port'
	if SwitchMulticast:
		SwitchMulticast.controllerConnection.send(msg2)
	else:
		print "Null Multicast"

#Envia mensagem openflow 'flow_mod' para encaminhamento dos pacotes ICMP no switch multicast
def encaminhaICMP(SwitchMulticast):
	msg = of.ofp_flow_mod() #mensagem flow_mod especifica alteracao na tabela de um switch

	#msg.priority = 42 #prioridade. Maior o valor, maior a prioridade.
	msg.match.dl_type = pkt.ethernet.IP_TYPE#0x800 tipo do protocolo do nivel de rede. IP
	msg.match.nw_type = pkt.ipv4.ICMP_PROTOCOL
	msg.match.nw_dst = IPAddr("10.0.0.1")
	msg.actions.append(of.ofp_action_output(port=1)) #dados do ip/porta em questao serao encaminhados na(s) porta(s) 'port'
	print "Connection"
	
	if SwitchMulticast:
		SwitchMulticast.controllerConnection.send(msg)
	else:
		print "Null Multicast"
			
	#mensagem que indica ao switch para encaminhar pacotes com origem no servidor para o destino ao qual ele busca
	msg2 = of.ofp_flow_mod() #mensagem flow_mod especifica alteracao na tabela de um switch
	#msg2.priority = 42 #prioridade. Maior o valor, maior a prioridade.
	msg2.match.dl_type = pkt.ethernet.IP_TYPE
	msg2.match.nw_type = pkt.ipv4.ICMP_PROTOCOL
	msg2.match.nw_src = IPAddr("10.0.0.1")
	msg2.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD)) #dados do ip/porta em questao serao encaminhados na(s) porta(s) 'port'
	if SwitchMulticast:
		SwitchMulticast.controllerConnection.send(msg2)
	else:
		print "Null Multicast"


def encaminhaUDP(SwitchMulticast):
	msg = of.ofp_flow_mod() #mensagem flow_mod especifica alteracao na tabela de um switch
	msg.priority = 42 #prioridade. Maior o valor, maior a prioridade.
	msg.match.dl_type = pkt.ethernet.IP_TYPE #0x800 = IPv4
	msg.match.nw_proto = pkt.ipv4.UDP_PROTOCOL
	msg.match.nw_dst = IPAddr("10.0.0.1")
	msg.actions.append(of.ofp_action_output(port=1)) #dados do ip/porta em questao serao encaminhados na(s) porta(s) 'port'

	if SwitchMulticast:
		SwitchMulticast.controllerConnection.send(msg)
	else:
		print "Null Multicast"

	#mensagem que indica ao switch para encaminhar pacotes com origem no servidor para o destino ao qual ele busca
	#Verificar tabela Multicast e encaminhar o pacote para as portas correspondentes a cada um dos grupos
	msg2 = msg = of.ofp_flow_mod() #mensagem flow_mod especifica alteracao na tabela de um switch
	msg2.priority = 42 #prioridade. Maior o valor, maior a prioridade.
	msg2.match.dl_type = pkt.ethernet.ARP_TYPE#0x806 tipo do protocolo do nivel de rede. ARP
	msg2.match.nw_src = IPAddr("10.0.0.1")
	msg2.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD)) #dados do ip/porta em questao serao encaminhados na(s) porta(s) 'port'

	if SwitchMulticast:
		SwitchMulticast.controllerConnection.send(msg2)
	else:
		print "Null Multicast"



def encaminhaTCP(SwitchMulticast):
	msg = of.ofp_flow_mod() #mensagem flow_mod especifica alteracao na tabela de um switch
	msg.priority = 42 #prioridade. Maior o valor, maior a prioridade.
	msg.match.dl_type = pkt.ethernet.IP_TYPE #0x800 = IPv4
	msg.match.nw_proto = pkt.ipv4.TCP_PROTOCOL
	msg.match.nw_dst = IPAddr("10.0.0.1")
	msg.actions.append(of.ofp_action_output(port=1)) #dados do ip/porta em questao serao encaminhados na(s) porta(s) 'port'
	
	msg2 = msg = of.ofp_flow_mod() #mensagem flow_mod especifica alteracao na tabela de um switch
	msg2.priority = 42 #prioridade. Maior o valor, maior a prioridade.
	msg2.match.dl_type = pkt.ethernet.IP_TYPE
	msg2.match.nw_proto = pkt.ipv4.TCP_PROTOCOL
	msg2.match.nw_src = IPAddr("10.0.0.1")
	msg2.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD)) #dados do ip/porta em questao serao encaminhados na(s) porta(s) 'port'



#cria evento que enviara mensagens openflow aos switches logo que a arvore estiver pronta
#class  eventoSetaSwtich(EventMixin):
#  def __init__(self):
   # Listen to events sourced by pox.core
#   pox.core.addListeners(self)
#   self.listenTo(pox.core)

#  def _handle_ComponentRegistered (self, event):
    # The name of this method has a special meaning to addListeners().
    # If a method name starts with _handle_ and ends with the name of
    # an event that the source publishes, the method is automatically
    # registered as an event handler.
    #  
    # This method will now be called whenever pox.core triggers a 
    # ComponentRegistered event.

    # Most event handlers are passed an event object as a parameter (though
    # individual Event classes can override this behavior by altering their
    # _invoke() method).
#    component = event.component
#    name = event.name
#	tree= core.RTSPMulticast.roteadorMulticast #Obtem arvore calculada em launch
#	roteadorMulticast = core.RTSPMulticast.roteadorMulticast
#    print("I see you,", name, "!")

#	def _handle_arvorePronta(self, event):			
#		self.setSWMulticast(tree,roteadorMulticast)

#	def setSwitchMulticast(tree,SWMulticast):
#		print 'Configurando Switches...'
	
#		encaminhaARP(SWMulticast)
#		encaminhaUDP(SWMulticast)
#		encaminhaTCP(SWMulticast)

def setSwitchMulticast():
		global roteadorMulticast
		SWMulticast = roteadorMulticast
		spanningTree = tree
		print 'Configurando Switches...'
		print SWMulticast		
		encaminhaARP(SWMulticast)
		encaminhaICMP(SWMulticast)
		encaminhaUDP(SWMulticast)
		encaminhaTCP(SWMulticast)

#Seta algoritmo de spanning tree nos outros switches
#def setOutrosSwitches():
	




def launch ():
	global tree
	core.registerNew(RTSPMulticast)
	dscv.launch()	
	spat.launch() #launch spanning tree module
	print 'Spanning tree gerada'
	tree = spat._calc_spanning_tree() #calcula arvore armazenando-a no atributo da classe RTSPMulticast. Esse atributo pode ser acessado
	core.callDelayed(10,setSwitchMulticast) #espera 10s ateh spanning tree ser calculada	
	#core.callDelayed(10,setOutrosSwitches) #Fazer essa funcao que aplica a spanning tree nos outros switches
	#print dir(tree)


