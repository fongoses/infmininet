# Copyright 2011 James McCauley
#
# This file is part of POX.
#
# POX is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# POX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with POX.  If not, see <http://www.gnu.org/licenses/>.

"""
An L2 learning switch.

This has per-switch config stored in a config file.
Each switch can create "flood groups" of ports, and can be configured to
drop packets with specific IPs/subnets or with specific TCP/UDP ports.

Uses a config file in JSON form.  For example, name this switches.json:
{
  "00-00-00-00-00-01":
  {
     'port_groups' : [[1,2],[3,4,5]],
     'banned_ips'  : ["192.168.1.0/24", "192.168.2.1"],
     'banned_ports': [80]
  },
  "00-00-00-00-00-02":
  {
     'banned_ports': [80]
  },
  "00-00-00-00-00-03":
  {
     'banned_ports': [80,53]
  }
}

Invoke POX like:
./pox.py log.level --DEBUG l2_port_slicer --config=switches.json
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str
from pox.lib.util import str_to_bool
from pox.lib.util import initHelper
from pox.lib.addresses import parse_cidr
import json
import time

log = core.getLogger()

# We don't want to flood immediately when a switch connects.
# Can be overriden on commandline.
_flood_delay = 2

class PortSliceSwitch (object):
  """
  The learning switch "brain" associated with a single OpenFlow switch.

  When we see a packet, we'd like to output it on a port which will
  eventually lead to the destination.  To accomplish this, we build a
  table that maps addresses to ports.

  We populate the table by observing traffic.  When we see a packet
  from some source coming from some port, we know that source is out
  that port.

  When we want to forward traffic, we look up the desintation in our
  table.  If we don't know the port, we simply send the message out
  all ports except the one it came in on.  (In the presence of loops,
  this is bad!).

  In short, our algorithm looks like this:

  For each packet from the switch:
  1) Use source address and switch port to update address/port table
  2) Is transparent = False and either Ethertype is LLDP or the packet's
     destination address is a Bridge Filtered address?
     Yes:
        2a) Drop packet -- don't forward link-local traffic (LLDP, 802.1x)
            DONE
  3) Is destination multicast?
     Yes:
        3a) Flood the packet
            DONE
  4) Port for destination address in our address/port table?
     No:
        4a) Flood the packet
            DONE
  5) Is output port the same as input port?
     Yes:
        5a) Drop packet and similar ones for a while
  6) Install flow table entry in the switch so that this
     flow goes out the appopriate port
     6a) Send the packet out appropriate port
  """
  def __init__ (self, connection, config):
    # Switch we'll be adding L2 learning switch capabilities to
    self.transparent = not not config["transparent"]  #declara e inicializa var/atributo 'transparent' dessa classe
    self.banned_ports = set(config["banned_ports"])
    self.banned_ips = [parse_cidr(ip, infer=False)
                       for ip in config['banned_ips']]
    
    # Make port groups easy to look up by port number
    # port_groups[some_port] -> tuple of all ports in same group
    self.port_groups = {}
    groups = config["port_groups"]
    groups = [tuple(sorted(list(set(g)))) for g in groups]
    for group in groups:
      for port in group:
        self.port_groups[port] = group

    self.connection = connection

    # Our table
    self.macToPort = {}

    # We want to hear PacketIn messages, so we listen
    # to the connection
    connection.addListeners(self)

    # We just use this to know when to log a helpful message
    self.hold_down_expired = _flood_delay == 0

  def _handle_PacketIn (self, event):
    """
    Handle packet in messages from the switch to implement above algorithm.
    """

    packet = event.parsed

    def drop (duration = None):
      """
      Drops this packet and optionally installs a flow to continue
      dropping similar ones for a while
      """
      if duration is not None:
        if not isinstance(duration, tuple):
          duration = (duration,duration)
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.idle_timeout = duration[0]
        msg.hard_timeout = duration[1]
        msg.buffer_id = event.ofp.buffer_id
        self.connection.send(msg)
      elif event.ofp.buffer_id is not None:
        msg = of.ofp_packet_out()
        msg.buffer_id = event.ofp.buffer_id
        msg.in_port = event.port
        self.connection.send(msg)

    group = self.port_groups.get(event.port)
    if group is None:
      log.debug("Dropping packets from non-grouped port %s.%i", 
                dpid_to_str(event.dpid), event.port)
      drop(5)
      return

    def flood (message = None):
      """ Floods the packet """
      msg = of.ofp_packet_out()
      if time.time() - self.connection.connect_time >= _flood_delay:
        # Only flood if we've been connected for a little while...

        if self.hold_down_expired is False:
          # Oh yes it is!
          self.hold_down_expired = True
          log.info("%s: Flood hold-down expired -- flooding",
              dpid_to_str(event.dpid))

        if message is not None: log.debug(message)

        # Send to all other ports in this group
        for p in group:
          msg.actions.append(of.ofp_action_output(port = p))
      else:
        pass
        #log.info("Holding down flood for %s", dpid_to_str(event.dpid))
      msg.data = event.ofp
      msg.in_port = event.port
      self.connection.send(msg)

    self.macToPort[packet.src] = event.port # 1

    # Check if it's filtered
    ipp = packet.find('ipv4')
    if ipp is not None:
      # It's IP
      for ip_range in self.banned_ips:
        if ipp.srcip.inNetwork(ip_range):
          log.debug("Banned IP: %s", ipp.srcip)
          drop(5)
          return
        if ipp.dstip.inNetwork(ip_range):
          log.debug("Banned IP: %s", ipp.dstip)
          drop(5)
          return

      tpp = ipp.find('tcp') or ipp.find('udp')
      if tpp:
        # It's TCP or UDP
        if tpp.srcport in self.banned_ports:
          log.debug("Banned TCP/UDP port: %i", tpp.srcport)
          drop(5)
          return
        if tpp.dstport in self.banned_ports:
          log.debug("Banned TCP/UDP port: %i", tpp.dstport)
          drop(5)
          return

    if not self.transparent: # 2
      if packet.type == packet.LLDP_TYPE or packet.dst.isBridgeFiltered():
        drop() # 2a
        return

    if packet.dst.is_multicast:
      flood() # 3a
    else:
      if packet.dst not in self.macToPort: # 4
        flood("Port for %s unknown -- flooding" % (packet.dst,)) # 4a
      else:
        port = self.macToPort[packet.dst]
        if port == event.port: # 5
          # 5a
          log.warning("Same port for packet from %s -> %s on %s.%s.  Drop."
              % (packet.src, packet.dst, dpid_to_str(event.dpid), port))
          drop(10)
          return
        # 6
        log.debug("installing flow for %s.%i -> %s.%i" %
                  (packet.src, event.port, packet.dst, port))
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet, event.port)
        msg.idle_timeout = 10
        msg.hard_timeout = 30
        msg.actions.append(of.ofp_action_output(port = port))
        msg.data = event.ofp # 6a
        self.connection.send(msg)


class PortSlicer (object):
  """
  Waits for OpenFlow switches to connect and makes them learning switches.
  """
  def __init__ (self, config_file):
    core.openflow.addListeners(self) #add listeners para os switches
    self.configs = json.load(file(config_file)) #var 'configs' armazena o dicionario com os dados doarquivo json que possui as config.

  def _handle_ConnectionUp (self, event):
    dpid = dpid_to_str(event.dpid)
    config = { #var config passada no init da classe PortSlicerSwitch
     'transparent' : False,
     'port_groups' : [[]], # List of lists of ports
     'banned_ips'  : [[]],   # List of IPs or CIDR subnets
     'banned_ports': [],   # List of TCP/UDP port numbers
    }
    
    # Fill in default port group with all normal ports
    for p in event.connection.ports:
      if p >= of.OFPP_MAX: continue #percorre todas as portas da conexao atual. Se o valor da porta eh maior que o max ignora voltando ao inicio do laco, senao da um append
      config['port_groups'][0].append(p) #adiciona porta na lista de portas envolvidas.


    if dpid not in self.configs: #caso porta nao esteja envolvida, exibe alerta
      log.warning("No config for %i port switch %s",
                  len(event.connection.ports), dpid)
    config.update(self.configs.get(dpid, {})) #get, com 2 parametros, obtem o valor no dicionario referenciado pela chave 'dpid', se nao ha valor retorna '{}' 

    log.debug("Connection %s" % (event.connection,)) #debuga
    PortSliceSwitch(event.connection, config) #inicializa switch



#Metodo Launch eh o primeiro a ser executado.
#'config' eh o path para o arquivo json
def launch (config, hold_down=_flood_delay):
  try:
    global _flood_delay
    _flood_delay = int(str(hold_down), 10)
    assert _flood_delay >= 0
  except:
    raise RuntimeError("Expected hold-down to be a number")
  #registra controlador
  core.registerNew(PortSlicer, config) #registra controlador PortSlicer, passando parametro de configuracao declarado com seu construtor '__init__

