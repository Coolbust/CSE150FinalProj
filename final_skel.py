#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):


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
    # Mininet and Python prefers the use of names without underscores
    # Named as clear as I could.

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
    # ports auto asssigned so nameing each port pair not necessasary

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
