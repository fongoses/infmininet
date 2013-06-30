from pox.core import core
from pox.lib.addresses import EthAddr, IPAddr
from pox.lib.util import dpid_to_str 
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt # POX convention
log = core.getLogger()
 
class MyComponent (object):
  def __init__ (self):
    core.openflow.addListeners(self)
 
  #cria e envia um pacote 'msg' (mensagem OpenFlow) que configura uma entrada na tabela  de um determinado switch.
  #Essa entrada sera responsavel em rotear determinados tipos de pacotes que elas especificam
  #A mensagem openflow atinge todos os switches, e eh enviada atraves do metodo connection.send(..) 
  def send_meu_pacoteip(self,event):
    
      # Traffic to 192.168.101.101:80 should be sent out switch port 4    
      self.porta=of.OFPP_FLOOD
      #self.porta=4
     
       # One thing at a time...
      msg = of.ofp_flow_mod() #mensagem flow_mod especifica alteracao na tabela de um switch
      msg.priority = 42 #prioridade. Maior o valor, maior a prioridade.
      msg.match.dl_type = 0x800 #tipo do protocolo do nivel de enlace (datalink). 0x80: 802.3
      msg.match.nw_dst = IPAddr("10.0.0.1") #ip em questao
      #msg.match.tp_dst = 80 #porta em questao
      msg.actions.append(of.ofp_action_output(port=self.porta)) #dados do ip/porta em questao serao encaminhados na(s) porta(s) 'port'
      event.connection.send(msg) #envia mensagem openflow para todos os switches
      print "Mensagem OFP enviada"
    
  #semelhante ao metodo anterior, porem trabalho com endereco mac 
  def send_meu_pacote_eth(self,event):
      #self.porta=4
      self.porta=of.OFPP_FLOOD
      
      # One thing at a time...
      msg = of.ofp_flow_mod() #mensagem flow_mod especifica alteracao na tabela de um switch
      msg.priority = 42 #prioridade. Maior o valor, maior a prioridade.
      #msg.match.dl_type = 0x800 #tipo do protocolo do nivel de enlace (datalink). 0x80: 802.3
      msg.match.dl_dst = EthAddr("ff:ff:ff:ff:ff:ff") #mac em questao
      msg.actions.append(of.ofp_action_output(port=self.porta)) #dados do ip/porta em questao serao encaminhados na(s) porta(s) 'port'
      event.connection.send(msg) #envia mensagem openflow para todos os switches
      print "Mensagem OFP enviada"



  def _handle_ConnectionUp (self, event):
    print 'Switch '+dpid_to_str(event.dpid)+' Conectado' 
    log.debug("Switch %s has come up.", dpid_to_str(event.dpid))
    self.send_meu_pacote_eth(event)
def launch ():
  core.registerNew(MyComponent)
  












#o metodo abaixo envia uma mensagem OpenFlow a um determinado switch
def send_packet (self, buffer_id, raw_data, out_port, in_port):
   """
   Descricao da mensagem:
   Sends a packet out of the specified switch port.
   If buffer_id is a valid buffer on the switch, use that.  Otherwise,
   send the raw data in raw_data.
   The "in_port" is the port number that packet arrived on.  Use
   OFPP_NONE if you're generating this packet.
   """
   msg = of.ofp_packet_out() #instancia/cria mensagem do tipo 'packet out', que instrui um determinado switch a enviar um pacote,
   #seja esse pacote criado pelo proprio switch, ou pelo controlador, ou armazenado no buffer, etc.

   msg.in_port = in_port #switch ira enviar o pacote de acordo com a porta in_port. Caso nao desejes especificar a porta,
   #sete-a com OFPP_NONE (nenhuma porta de entrada especificada)

   if buffer_id != -1 and buffer_id is not None:
     # We got a buffer ID from the switch; use that
     msg.buffer_id = buffer_id #caso a mensagem esteja no buffer, enviaremos ela. O buffer_id especifica qual eh o buffer que contem
     #essa mensagem
   else:
     # No buffer ID from switch -- we got the raw data
     if raw_data is None:
       # No raw_data specified -- nothing to send!
       return
     msg.data = raw_data #se a mensagem nao esta no buffer (ou seja, eh uma mensagem construida), seta os bytes da mensagem criada.
   
   action = of.ofp_action_output(port = out_port) #define a action relacionada(action_output, que especifica uma porta de saida para mensagem)
   #em geral, 
   msg.actions.append(action)
   
   # Send message to switch
   self.connection.send(msg)



