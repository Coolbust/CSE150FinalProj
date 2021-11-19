#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):
    # Examples!
    # Create a host with a default route of the ethernet interface. You'll need to set the
    # default gateway like this for every host you make on this assignment to make sure all 
    # packets are sent out that port. Make sure to change the h# in the defaultRoute area
    # and the MAC address when you add more hosts!
    # h1 = self.addHost('h1',mac='00:00:00:00:00:01',ip='1.1.1.1/24', defaultRoute="h1-eth0")
    # h2 = self.addHost('h2',mac='00:00:00:00:00:02',ip='2.2.2.2/24', defaultRoute="h2-eth0")

    # Create a switch. No changes here from Lab 1.
    # s1 = self.addSwitch('s1')

    # Connect Port 8 on the Switch to Port 0 on Host 1 and Port 9 on the Switch to Port 0 on 
    # Host 2. This is representing the physical port on the switch or host that you are 
    # connecting to.
    #
    # IMPORTANT NOTES: 
    # - On a single device, you can only use each port once! So, on s1, only 1 device can be
    #   plugged in to port 1, only one device can be plugged in to port 2, etc.
    # - On the "host" side of connections, you must make sure to always match the port you 
    #   set as the default route when you created the device above. Usually, this means you 
    #   should plug in to port 0 (since you set the default route to h#-eth0).
    #
    # self.addLink(s1,h1, port1=8, port2=0)
    # self.addLink(s1,h2, port1=9, port2=0)

    print "Delete me!"

    # Setting up floor 1 devices
    laptop  = self.addHost('laptop',mac='00:00:00:00:00:01',ip='20.2.1.10/24')
    labmachine = self.addHost('lab machine',mac='00:00:00:00:00:02',ip='20.2.1.20/24')

    #floor 1 switch one for the laptop and lab machine
    floor1switch1 = self.addSwitch('f1s1')

    #setting up floor 2 devices connected to switch 2
    device1 = self.addHost('device1',mac='00:00:00:00:00:03',ip='20.2.1.30/24')
    device2 = self.addHost('device2',mac='00:00:00:00:00:04',ip='20.2.1.40/24')

    #floor 1 switch 2 for device1 and device 2
    floor1switch2 = self.addSwitch('f1s2')

    #-----------------------------------------------------end floor 1
    
    #setting up floor 2 hosts
    host1 = self.addHost('h1',mac='00:00:00:00:00:05',ip='10.2.7.10/24')
    host2 = self.addHost('h2',mac='00:00:00:00:00:06',ip='10.2.7.20/24')

    #floor 2 switch 1 for h1 and h2
    floor2switch1 = self.addSwitch('f2s1')

    #setting up air-gapped floor
    secureclients = self.addHost('h1',mac='00:00:00:00:00:07',ip='40.2.5.0/29')

    #switch for airgapped floor
    agfswitch1 = self.addSwitch('agfs1')

    #---------------------------------------------------end floor 2 and agf
    
    #setting up webserver and data center switch
    webserver = self.addHost('webserver',mac='00:00:00:00:00:08',ip='30.1.4.66/24')

    #date center switch
    dataswitch = self.addSwitch('datacs')


    #Trusted Host 
    thost = self.addHost('trusted host',mac='00:00:00:00:00:09',ip='104.24.32.100/24')

    #Untrusted Host
    uhost = self.addHost('untrusted host',mac='00:00:00:00:00:10',ip='108.44.83.103/24')

    #---------------------------------------------------end devices

    #Creating core switch

    core = self.addSwitch('core')
    
    # Switch Connecting ---------------------------------------------------

    #Connecting switches

    #Floor 1 part 1
    self.addLink(laptop,floor1switch1)
    self.addLink(labmachine,floor1switch1)
    
    #Floor 1 part 2
    self.addLink(device1,floor1switch2)
    self.addLink(device2,floor1switch2)

    #Floor 2
    self.addLink(host1,floor2switch1)
    self.addLink(host2,floor2switch1)

    #Floor agf
    self.addLink(secureclients, agfswitch1)

    #Web server switch
    self.addLink(webserver,dataswitch)

    #connecting the switches to the core
    self.addLink(floor1switch1,core)
    self.addLink(floor1switch2,core)
    self.addLink(floor2switch1,core)
    self.addLink(agfswitch1,core)
    self.addLink(dataswitch,core)

    #connecting the hosts directly
    self.addLink(thost,core)
    self.addLink(uhost,core)

    #end topo


def configure():

  topo = final_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  net.start()

  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()
