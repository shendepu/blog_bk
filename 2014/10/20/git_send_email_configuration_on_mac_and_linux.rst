git send-email Configuration on Mac and Linux
=============================================

Some web interface of git, like github, stash, helps users easily manage pull requests, however pure distributed teams who may have problem to centralize operation may utilize git built-in patch and send-email functions to collaborate via email. 

To enable *git send-email*, the sendmail/postfix client need to be configured. 

Mac OS X
--------

.. code-block:: bash

    # Configure postfix 
    sudo vim /etc/postfix/main.cf

    # Add content in /etc/postfix/main.cf
    relayhost = [smtp.live.com]:587
    smtp_tls_loglevel=1
    smtp_tls_security_level=encrypt
    smtp_sasl_auth_enable=yes
    smtp_sasl_password_maps=hash:/etc/postfix/sasl_passwd
    smtp_sasl_security_options = noanonymous

    # Add file /etc/postfix/sasl_passwd with content
    [smtp.live.com]:587 <email_account>:<password>

    # Update sasl_passwd
    sudo postmap /etc/postfix/sasl_passwd 

    # Re-start postfix daemon
    sudo launchctl stop org.postfix.master
    sudo launchctl start org.postfix.master

Linux
-----

.. code-block:: bash

    # Edit /etc/ssmtp
    sudo vim /etc/ssmtp/ssmtp.conf

    # Edit below content
    mailHub=smtp.live.com:587
    AuthUser=<email_account>
    AuthPass=<password>

    RewriteDomain=hotmail.com
    Hostname=localhost

    FromLineOverride=Yes
    UseTLS=yes
    UseSTARTTLS=yes

Configure *~/.gitconfig*
------------------------

.. code-block:: conf

    [sendmail]
        smtpencryption = tls
        smtpserver = smtp.live.com
        smtpuser = <email_account>
        smtpserverport = 587


Test
----

.. code-block:: bash

    # Create a patch with last commit 
    git format-patch HEAD~ test.patch

    # Send it via email 
    git send-email --to to@email.com --cc cc@email.com test.patch 

    # Save the received email as plain text, apply it
    git am test.patch 



.. author:: default
.. categories:: none
.. tags:: none
.. comments::
