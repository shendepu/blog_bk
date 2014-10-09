Set Up Natural Scrolling for a Mouse in Fedora
==============================================


This configuration should work for all X11-based linux desktop.

.. code-block:: bash

    # Find your mouse device id
    xinput list

    # Find Scrolling Distance default settings that should be 1, 1, 1
    xinput list-props {device id} | grep "Scrolling Distance"

    # Add natural scrolling conf to X11 
    sudo vim /usr/share/X11/xorg.conf.d/20-natural-scrolling.conf 

    # And put configurations in the conf file
    Section "InputClass"
        Identifier "Natural Scrolling"
        MatchIsPointer "on"
        MatchDevicePath "/dev/input/event*"
        Option "VertScrollDelta" "-1"
        Option "HorizScrollDelta" "-1"
        Option "DialDelta" "-1"
    EndSection

    # Save and reboot, it will work 


.. author:: default
.. categories:: none
.. tags:: none
.. comments::
