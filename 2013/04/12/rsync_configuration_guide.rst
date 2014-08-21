Rsync Configuration Guide
=========================

Configuring Server
------------------

Edit /etc/rsyncd.conf

.. code-block:: ini

    uid =root
    gid =root
    use chroot=no
    log file=/var/log/rsyncd.log
    pid file=/var/run/rsyncd.pid
    lock file=/var/run/rsyncd.lock

    [jira-data]
    path=/var/atlassian/application-data/jira
    comment=jira home folder
    ignore errors
    read only=yes
    list=no
    auth users=rsync
    secrets file=/etc/rsyncd.scrt

Add file /etc/rsyncd.scrt 

.. code-block:: cfg

    rsync:password

Add user rsync

.. code-block:: bash

    useradd rsync

Change permission of /etc/rsyncd.scrt to 0600 

.. code-block:: bash

    chmod 0600 /etc/rsyncd.scrt

Start rsync as daemon service 

.. code-block:: bash

    rsync --daemon 



Configuring Client
------------------

Assuming user jira already exist.

Add file /etc/rsync-jira.password, and fill in password

.. code-block:: cfg

    password

Change owner and permission of /etc/rsync-jira.password

.. code-block:: bash

    chown jira /etc/rsync-jira.password
    chmod 0600 /etc/rsync-jira.password

Add filter for rsync /etc/rsync-jiradata.filter

.. code-block:: cfg

    - /caches/
    - /export/
    - /import/
    - /log/
    - /monitor/
    - /tmp/
    - /dbconfig.xml - /.*
    +*

Only allow user jira to /etc/rsync-jiradata.filter

.. code-block:: bash

    chmod 0600 /etc/rsync-jiradata.filter

Add a cron job for user jira 

.. code-block:: bash

    vim /etc/cron.d/jira

    # Add cron job to run every five minutes
    */5 * * * * jira /usr/bin/rsync -vzrtopg --delete \
    	--password-file=/etc/rsync.password \
    	--include-from=/etc/rsync-jiradata.filter \
    	rsync@192.168.188.146::jira-data /var/atlassian/jira

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
