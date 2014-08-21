************************
Openstack Configurations
************************

iptables configuration
======================

Controller Node
---------------

.. code-block:: bash

    iptables -I INPUT 4 -d 192.168.0.11 -p tcp -m tcp --dport 80 -j ACCEPT
    iptables -I INPUT 4 -d 192.168.0.11 -p tcp -m tcp --dport 443 -j ACCEPT
    iptables -I INPUT 4 -d 192.168.0.11 -p tcp -m tcp --dport 873 -j ACCEPT
    iptables -I INPUT 4 -d 192.168.0.11 -p tcp -m tcp --dport 3306 -j ACCEPT
    iptables -I INPUT 4 -d 192.168.0.11 -p tcp -m tcp --dport 35357 -j ACCEPT
    iptables -I INPUT 4 -d 192.168.0.11 -p tcp -m tcp --dport 3260 -j ACCEPT
    iptables -I INPUT 4 -d 192.168.0.11 -p tcp -m tcp --dport 5000 -j ACCEPT
    iptables -I INPUT 4 -d 192.168.0.11 -p tcp -m tcp --dport 5672 -j ACCEPT
    iptables -I INPUT 4 -d 192.168.0.11 -p tcp -m tcp --dport 6080 -j ACCEPT
    iptables -I INPUT 4 -d 192.168.0.11 -p tcp -m tcp --dport 6081 -j ACCEPT
    iptables -I INPUT 4 -d 192.168.0.11 -p tcp -m tcp --dport 6082 -j ACCEPT
    iptables -I INPUT 4 -d 192.168.0.11 -p tcp -m tcp --dport 8773 -j ACCEPT
    iptables -I INPUT 4 -d 192.168.0.11 -p tcp -m tcp --dport 8774 -j ACCEPT
    iptables -I INPUT 4 -d 192.168.0.11 -p tcp -m tcp --dport 8775 -j ACCEPT
    iptables -I INPUT 4 -d 192.168.0.11 -p tcp -m tcp --dport 8776 -j ACCEPT
    iptables -I INPUT 4 -d 192.168.0.11 -p tcp -m tcp --dport 9191 -j ACCEPT
    iptables -I INPUT 4 -d 192.168.0.11 -p tcp -m tcp --dport 9292 -j ACCEPT
    iptables -I INPUT 4 -d 192.168.0.11 -p tcp -m tcp --dport 9696 -j ACCEPT
    iptables -I INPUT 4 -d 192.168.0.11 -p tcp -m tcp --dport 1111 -j ACCEPT
    iptables -I INPUT 4 -d 192.168.0.11 -p tcp -m tcp --dport 5353 -j ACCEPT
    iptables -I INPUT 4 -d 192.168.0.11 -p tcp -m tcp --dport 9697 -j ACCEPT 
    iptables -I INPUT 4 -p udp --dport 67:68 -j ACCEPT
    iptables -I INPUT 4 -p udp -m udp --dport 53 -j ACCEPT
    iptables -I INPUT 4 -p tcp -m tcp --dport 53 -j ACCEPT
    iptables -A INPUT -j REJECT --reject-with icmp-host-prohibited


Compute Node
------------

.. code-block:: bash

  	iptables -I INPUT 4 -p tcp -m tcp -d 192.168.0.31 --dport 5900:5999 -j ACCEPT



Failures and Solutions
======================

Metadata proxy
--------------

**Accessing http://169.254.169.254 get http 500 error while namesapce is set True**

Check the log if there is something like 
::

    type=AVC msg=audit(1407815941.057:41925): avc:  denied  { connectto } for  
    pid=3307 comm="neutron-ns-meta" path="/var/lib/neutron/metadata_proxy" 
    scontext=system_u:system_r:neutron_t:s0 tcontext=system_u:system_r:neutron_t
    :s0 tclass=unix_stream_socket

if so, there is issue with SELiinx policy, refer to https://bugzilla.redhat.com/show_bug.cgi?id=1110263. 

Before new openstack-selinux package available, it can be solved by change selinux mode to permissive.


DHCP agent
----------

**VM can't get IP**

The VM NIC's MTU should be less than 1454 if GRE is configured on neutron network. GRE add extra header to tcp package. 

Interesting thoughts? (has not bee tested yet): increase the MTU to 9046 on NIC of host which is used for instance tunnel on both network node and compute node, then set VM NIC's MTU to 9000. But how to deal with MTU on external network? 


Cinder Volumes
--------------

**cinder Failed to create iscsi target for volume** 

stop tgtd service 


.. author:: default
.. categories:: none
.. tags:: none
.. comments::
