Ubuntu Change Keyboard Layout
=============================

Switch Super and Alt, and make Super L behaving like Control, so the keyboard layout works more like Mac.

.. code-block:: ini

    clear control
    clear mod4 
    clear mod1

    ! ------------------------
    ! left side
    ! ------------------------
    ! key code 64 is the left alt key
    keycode 64 = Super_L

    ! key code 133 is the left command key
    keycode 133 = Alt_L Meta_L

    ! ------------------------
    ! right side 
    ! ------------------------
    ! key code 134 is the right command key 
    keycode 134 = Alt_R Meta_R

    ! key code 108 is the right alt key
    keycode 108 = Super_R

    ! key code 135 is the context menu key
    keycode 135 = Alt_R Meta_R

    add mod4 = Super_R
    add mod1 = Alt_L Meta_L
    add mod1 = Alt_R Meta_R

    keysym Super_L = Control_L
    add Control = Control_L Control_R



.. author:: default
.. categories:: none
.. tags:: none
.. comments::
