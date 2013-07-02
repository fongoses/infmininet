from pox.core import core
from pox.lib.addresses import EthAddr, IPAddr
from pox.lib.util import dpid_to_str 
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt # POX convention
import pox.openflow.l2_learning as l2
log = core.getLogger()

#A cada pacote recebido, realiza o roteamento 
class RoteadorMulticast(object): 
  
    
    def __init__ (self,connection):
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
   
        packet=event.parsed #obtem pacote 
       
        #Registra pacote atual no grupo
        def registraNoGrupo(Packet,Grupo): 
            #Faz um match, testando se a porta eh 554

            #se deu match, registra ip de origem na tabela multicast
            #formato da tabela: 
            #   ---------------------------------------
            #   |IP_DO_HOST | IDENTIFICADOR/IP_DO_GRUPO|
            #   ----------------------------------------
            self.tabelaMulticast[Packet.src] == Grupo #nessa nossa implementacao ha apenas o grupo identificado por 1

        def encaminhaPacote(Packet,Grupo):
            foo=1
            #Grupo
            #for ip in self.tabelaMulticast
            #    pacoteMulticast = of.ofp_packet_out() #evento para encaminhamento de pacote
                
class RTSPMulticast(object):
   
    def __init__(self):
        core.openflow.addListeners(self) #a propria classe que implementa eh um listener que trabalha com a interface _handle_ConnectionUp
         
    def _handle_ConnectionUp (self, event):
        self.DPID = dpid_to_str(event.dpid)
        log.debug("Switch %s has come up.", self.DPID)
        if(self.DPID == "00-00-00-00-00-01"):
            RoteadorMulticast(event.connection)            
            print 'Switch Multicast [ '+self.DPID+' ] Conectado' 
        else:
            l2.LearningSwitch(event.connection,transparent=False)
            print 'Switch l2 [ '+self.DPID+' ] Conectado'
        #self.send_meu_pacote_eth(event)



def launch ():
    core.registerNew(RTSPMulticast)








