RRDTool Basis
=============

Terminologies
-------------

* Data Source (DS)
  

* heartbeat
   

* Date Source Type (DST)

* Round Robin Archive (RRA)

* Consolidation Function (CF)

Example: 

.. code-block:: bash

     rrdtool create target.rrd \
         --start 1023654125 \
         --step 300 \
         DS:mem:GAUGE:600:0:671744 \
         RRA:AVERAGE:0.5:12:24 \
         RRA:AVERAGE:0.5:288:31



























.. author:: default
.. categories:: none
.. tags:: none
.. comments::
