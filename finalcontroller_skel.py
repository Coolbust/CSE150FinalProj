# Final Skeleton

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    # This is where you'll put your code. The following modifications have 
    # been made from Lab 3:
    #   - port_on_switch: represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet.
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
    # You should use these to determine where a packet came from. To figure out where a packet 
    # is going, you can use the IP header information.
    if switch_id != 4:
    #Untrusted Host cannot send ICMP traffic to any of the devices
    # on floor1 and floor2, or the Web Server.
    #Untrusted Host cannot send any IP traffic to the Web Server.
      if switch_id == 5 and port_on_switch == 7:
        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x0800 #ICMP
        msg.match.nw_dst = '104.24.32.100'
        out = of.OFPP_NORMAL
        msg.actions.append(of.ofp_action_output(port = out))
        self.connection.send(msg)

        # Any any arp, accept
        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x0806 #ARP
        msg.match.nw_dst = '104.24.32.100'
        out = of.OFPP_NORMAL
        msg.actions.append(of.ofp_action_output(port = out))
        self.connection.send(msg)

        #Untrust host can send to Trust host

        #Untrust host can send IP traffic but not to webserver
        # blocking IP traffic to webserver
        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x0800 #ICMP
        msg.match.nw_proto = 4
        msg.match.nw_dst = '30.1.4.66'
        self.connection.send(msg)

        #Untrust host can send IP
        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x0800 #ICMP
        msg.match.nw_proto = 4 #IP
        out = of.OFPP_NORMAL
        msg.actions.append(of.ofp_action_output(port = out))
        self.connection.send(msg)

        #any other ipv4 drop
        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x0800 
        match = of.ofp_match()
        msg.match = match
        self.connection.send(msg)

        #any other arg drop
        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x0806
        match = of.ofp_match()
        msg.match = match
        self.connection.send(msg)
        # End untrust host -----------------------------------------------

      elif switch_id == 5 and port_on_switch == 6:
        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x0800 #ICMP
        msg.match.nw_dst = '108.44.83.103'
        out = of.OFPP_NORMAL
        msg.actions.append(of.ofp_action_output(port = out))
        self.connection.send(msg)
        # Uhost can talk to Thost
        # #  End trust host -----------------------------------------------

      if switch_id == 6:
        #Web server blocks TCP from Thost
        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x0800 #ICMP
        msg.match.nw_proto = 6 #TCP
        msg.match.nw_dst = '104.24.32.100'
        self.connection.send(msg)

        # Web server blocks Thost
        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x0800 #ICMP
        msg.match.nw_dst = '104.24.32.100'
        self.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x0806 #ARP
        msg.match.nw_dst = '104.24.32.100'
        self.connection.send(msg)


      if switch_id == 1:
        # Floor 1 switch 1 blocks thost icmp
        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x0800 #ICMP
        msg.match.nw_dst = '104.24.32.100'
        self.connection.send(msg)

        # Floor 1 blocks Floor 2
        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x0800 #ICMP
        msg.match.nw_dst = '10.2.7.10'
        self.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x0800 #ICMP
        msg.match.nw_dst = '10.2.7.20'
        self.connection.send(msg)

      if switch_id == 2:
        # floor 1 switch 2 blocks switch 1
        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x0800 #ICMP
        msg.match.nw_dst = '104.24.32.100'
        self.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x0800 #ICMP
        msg.match.nw_dst = '104.24.32.100'
        self.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x0800 #ICMP
        msg.match.nw_dst = '10.2.7.10'
        self.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x0800 #ICMP
        msg.match.nw_dst = '10.2.7.20'
        self.connection.send(msg)

      if switch_id != 5 and port_on_switch != 6:
          # Blocking of untrusted host
          msg = of.ofp_flow_mod()
          msg.match.dl_type = 0x0800 #ICMP
          msg.match.nw_dst = '108.44.83.103'
          self.connection.send(msg)

          msg = of.ofp_flow_mod()
          msg.match.dl_type = 0x0806 #ARP
          msg.match.nw_dst = '108.44.83.103'
          self.connection.send(msg)
          # End of blocking of untrusted host

      # Start ping all 
      # ICMP pingall should pass
      msg = of.ofp_flow_mod()
      msg.match.dl_type = 0x0800 #ICMP
      msg.match.nw_proto = 1
      out = of.OFPP_NORMAL
      msg.actions.append(of.ofp_action_output(port = out))
      self.connection.send(msg)

      # Any any arp, accept
      msg = of.ofp_flow_mod()
      msg.match.dl_type = 0x0806 #ARP
      out = of.OFPP_NORMAL
      msg.actions.append(of.ofp_action_output(port = out))
      self.connection.send(msg)
      #End ping all

      # IP can be sent
      msg = of.ofp_flow_mod()
      msg.match.dl_type = 0x0800 #ICMP
      msg.match.nw_proto = 4 #IP
      out = of.OFPP_NORMAL
      msg.actions.append(of.ofp_action_output(port = out))
      self.connection.send(msg)

      # TCP can be sent
      msg = of.ofp_flow_mod()
      msg.match.dl_type = 0x0800 #ICMP
      msg.match.nw_proto = 6 #TCP
      msg.match.nw_dst = '104.24.32.100'
      self.connection.send(msg)

      #any other ipv4 drop
      msg = of.ofp_flow_mod()
      msg.match.dl_type = 0x0800 
      match = of.ofp_match()
      msg.match = match
      self.connection.send(msg)

    # start of secure floor communication
    if switch_id == 4:
      msg = of.ofp_flow_mod()
      msg.match.dl_type = 0x0800 #ICMP
      msg.match.nw_proto = 1
      msg.match.nw_dst = '40.2.5.10'
      out = of.OFPP_NORMAL
      msg.actions.append(of.ofp_action_output(port = out))
      self.connection.send(msg)

      # Any any arp, accept
      msg = of.ofp_flow_mod()
      msg.match.dl_type = 0x0806 #ARP
      msg.match.nw_dst = '40.2.5.10'
      out = of.OFPP_NORMAL
      msg.actions.append(of.ofp_action_output(port = out))
      self.connection.send(msg)
      #End ping all

      msg = of.ofp_flow_mod()
      msg.match.dl_type = 0x0800 #ICMP
      msg.match.nw_proto = 1
      msg.match.nw_dst = '40.2.5.0'
      out = of.OFPP_NORMAL
      msg.actions.append(of.ofp_action_output(port = out))
      self.connection.send(msg)

      # Any any arp, accept
      msg = of.ofp_flow_mod()
      msg.match.dl_type = 0x0806 #ARP
      msg.match.nw_dst = '40.2.5.0'
      out = of.OFPP_NORMAL
      msg.actions.append(of.ofp_action_output(port = out))
      self.connection.send(msg)

      msg = of.ofp_flow_mod()
      msg.match.dl_type = 0x0800 #ICMP
      msg.match.nw_proto = 1
      msg.match.nw_dst = '40.2.5.20'
      out = of.OFPP_NORMAL
      msg.actions.append(of.ofp_action_output(port = out))
      self.connection.send(msg)

      # Any any arp, accept
      msg = of.ofp_flow_mod()
      msg.match.dl_type = 0x0806 #ARP
      msg.match.nw_dst = '40.2.5.20'
      out = of.OFPP_NORMAL
      msg.actions.append(of.ofp_action_output(port = out))
      self.connection.send(msg)

      msg = of.ofp_flow_mod()
      msg.match.dl_type = 0x0800 #ICMP
      msg.match.nw_proto = 1
      msg.match.nw_dst = '40.2.5.30'
      out = of.OFPP_NORMAL
      msg.actions.append(of.ofp_action_output(port = out))
      self.connection.send(msg)

      # Any any arp, accept
      msg = of.ofp_flow_mod()
      msg.match.dl_type = 0x0806 #ARP
      msg.match.nw_dst = '40.2.5.30'
      out = of.OFPP_NORMAL
      msg.actions.append(of.ofp_action_output(port = out))
      self.connection.send(msg)

      msg = of.ofp_flow_mod()
      msg.match.dl_type = 0x0800 #ICMP
      msg.match.nw_proto = 1
      msg.match.nw_dst = '40.2.5.40'
      out = of.OFPP_NORMAL
      msg.actions.append(of.ofp_action_output(port = out))
      self.connection.send(msg)

      # Any any arp, accept
      msg = of.ofp_flow_mod()
      msg.match.dl_type = 0x0806 #ARP
      msg.match.nw_dst = '40.2.5.40'
      out = of.OFPP_NORMAL
      msg.actions.append(of.ofp_action_output(port = out))
      self.connection.send(msg)

      msg = of.ofp_flow_mod()
      msg.match.dl_type = 0x0800 #ICMP
      msg.match.nw_proto = 1
      msg.match.nw_dst = '40.2.5.50'
      out = of.OFPP_NORMAL
      msg.actions.append(of.ofp_action_output(port = out))
      self.connection.send(msg)

      # Any any arp, accept
      msg = of.ofp_flow_mod()
      msg.match.dl_type = 0x0806 #ARP
      msg.match.nw_dst = '40.2.5.50'
      out = of.OFPP_NORMAL
      msg.actions.append(of.ofp_action_output(port = out))
      self.connection.send(msg)

      #any other ipv4 drop
      msg = of.ofp_flow_mod()
      msg.match.dl_type = 0x0800 
      match = of.ofp_match()
      msg.match = match
      self.connection.send(msg)

      #any other arg drop
      msg = of.ofp_flow_mod()
      msg.match.dl_type = 0x0806
      match = of.ofp_match()
      msg.match = match
      self.connection.send(msg)


  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
