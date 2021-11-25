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
        #self.addLink(f1sw1,laptop, port1=1,port2=0)
    #self.addLink(f1sw1,labmachine,port1=2,port2=0)
  
    # ------------------------------------------ Creating and testing floor 1
    # Setting up floor 1 devices

    f1sw1 = self.addSwitch('s1')

    laptop  = self.addHost('laptop',mac='00:00:00:00:00:01',ip='20.2.1.10', defaultRoute="laptop-eth0")
    labmachine = self.addHost('lbmachine',mac='00:00:00:00:00:02',ip='20.2.1.20', defaultRoute="lbmachine-eth0")

    self.addLink(laptop,f1sw1)
    self.addLink(labmachine,f1sw1)

    # Floor 1 switch 2
    #setting up floor 2 devices connected to switch 2
    device1 = self.addHost('device1',mac='00:00:00:00:00:03',ip='20.2.1.30/24', defaultRoute="device1-eth0")
    device2 = self.addHost('device2',mac='00:00:00:00:00:04',ip='20.2.1.40/24', defaultRoute="device2-eth0")

    #floor 1 switch 2 for device1 and device 2
    f1sw2 = self.addSwitch('s2')

    self.addLink(device1,f1sw2)
    self.addLink(device2,f1sw2)


    #-----------------------------------------------------end floor 1
    
    #setting up floor 2 hosts
    host1 = self.addHost('host1',mac='00:00:00:00:00:05',ip='10.2.7.10', defaultRoute="host1-eth0")
    host2 = self.addHost('host2',mac='00:00:00:00:00:06',ip='10.2.7.20', defaultRoute="host2-eth0")

    #floor 2 switch 1 for h1 and h2
    f2sw1 = self.addSwitch('s3')

    self.addLink(host1,f2sw1)
    self.addLink(host2,f2sw1)

    #setting up air-gapped floor
    secureclient1 = self.addHost('sec1',mac='00:00:00:00:00:07',ip='40.2.5.0',defaultRoute="sec1-eth0")
    secureclient2 = self.addHost('sec2',mac='00:00:00:00:00:11',ip='40.2.5.10',defaultRoute="sec2-eth0")
    secureclient3 = self.addHost('sec3',mac='00:00:00:00:00:12',ip='40.2.5.20',defaultRoute="sec3-eth0")
    secureclient4 = self.addHost('sec4',mac='00:00:00:00:00:13',ip='40.2.5.30',defaultRoute="sec4-eth0")
    secureclient5 = self.addHost('sec5',mac='00:00:00:00:00:14',ip='40.2.5.40',defaultRoute="sec5-eth0")
    secureclient6 = self.addHost('sec6',mac='00:00:00:00:00:15',ip='40.2.5.50',defaultRoute="sec6-eth0")

    #switch for airgapped floor
    agfsw1 = self.addSwitch('s4')

    self.addLink(agfsw1,secureclient1,port1=1,port2=0)
    self.addLink(agfsw1,secureclient2,port1=2,port2=0)
    self.addLink(agfsw1,secureclient3,port1=3,port2=0)
    self.addLink(agfsw1,secureclient4,port1=4,port2=0)
    self.addLink(agfsw1,secureclient5,port1=5,port2=0)
    self.addLink(agfsw1,secureclient6,port1=6,port2=0)

    #---------------------------------------------------end floor 2 and agf
    
    #setting up webserver and data center switch
    webserver = self.addHost('webserver',mac='00:00:00:00:00:08',ip='30.1.4.66',defaultRoute="webserver-eth0")

    #date center switch
    datasw = self.addSwitch('s6')

    self.addLink(webserver,datasw)

    #Trusted Host 
    thost = self.addHost('thost',mac='00:00:00:00:00:09',ip='104.24.32.100',defaultRoute="thost-eth0")

    #Untrusted Host
    uhost = self.addHost('unthost',mac='00:00:00:00:00:10',ip='108.44.83.103',defaultRoute="unthost-eth0")


    # testing core 

    core = self.addSwitch('s5')

    self.addLink(core, f1sw1)
    self.addLink(core, f1sw2)
    self.addLink(core,f2sw1)
    self.addLink(core,agfsw1)
    self.addLink(core,datasw)
    self.addLink(core,thost, port1=6,port2=0)
    self.addLink(core,uhost, port1=7,port2=0)

def configure():
  topo = final_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  net.start()
  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()
