# Final Skeleton
#
# Hints/Reminders from Lab 3:
#
# To check the source and destination of an IP packet, you can use
# the header information... For example:
#
# ip_header = packet.find('ipv4')
#
# if ip_header.srcip == "1.1.1.1":
#   print "Packet is from 1.1.1.1"
#
# Important Note: the "is" comparison DOES NOT work for IP address
# comparisons in this way. You must use ==.
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

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
        print("Switch 5 port 7")
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

        #any other ipv4 drop
        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x0800 
        match = of.ofp_match()
        msg.match = match
        self.connection.send(msg)

        #any other ipv4 drop
        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x0806
        match = of.ofp_match()
        msg.match = match
        self.connection.send(msg)
        # End untrust host -----------------------------------------------

      elif switch_id == 5 and port_on_switch == 6:
        print("Switch 5 port 6")
        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x0800 #ICMP
        msg.match.nw_dst = '108.44.83.103'
        out = of.OFPP_NORMAL
        msg.actions.append(of.ofp_action_output(port = out))
        self.connection.send(msg)

        # Any any arp, accept
        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x0806 #ARP
        msg.match.nw_dst = '108.44.83.103'
        out = of.OFPP_NORMAL
        msg.actions.append(of.ofp_action_output(port = out))
        self.connection.send(msg)
        #  End trust host -----------------------------------------------
      elif port_on_switch != 6 and port_on_switch !=7:
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

      #any other ipv4 drop
      msg = of.ofp_flow_mod()
      msg.match.dl_type = 0x0800 
      match = of.ofp_match()
      msg.match = match
      self.connection.send(msg)

    # Secure Floor Flow Table ---------------------------------
    if switch_id == 4 and port_on_switch == 1:
      # Start ping all 
      # ICMP pingall should pass
      # print("In switch 4 port 1")
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


    if switch_id == 4 and port_on_switch == 2:
      # Start ping all 
      # ICMP pingall should pass
      # print("In switch 4 port 2")
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
      #End ping all
    # End Secure Floor -------------------------------------------------

    # ------------------------------
    




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
