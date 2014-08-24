Munin Plugins Configuration
===========================

MySQL Configuration
-------------------

.. code-block:: bash

    # Install necessary perl packages 
    sudo yum -y install perl-Cache-Cache

    # Add symbolic link for mysql plugin 
    sudo ln -s /usr/share/munin/plugins/mysql_ mysql_bin_relay_log
    sudo ln -s /usr/share/munin/plugins/mysql_ mysql_commands
    sudo ln -s /usr/share/munin/plugins/mysql_ mysql_connections
    sudo ln -s /usr/share/munin/plugins/mysql_ mysql_files_tables
    sudo ln -s /usr/share/munin/plugins/mysql_ mysql_innodb_bpool
    sudo ln -s /usr/share/munin/plugins/mysql_ mysql_innodb_bpool_act
    sudo ln -s /usr/share/munin/plugins/mysql_ mysql_innodb_io
    sudo ln -s /usr/share/munin/plugins/mysql_ mysql_innodb_log
    sudo ln -s /usr/share/munin/plugins/mysql_ mysql_innodb_rows
    sudo ln -s /usr/share/munin/plugins/mysql_ mysql_innodb_semaphores
    sudo ln -s /usr/share/munin/plugins/mysql_ mysql_innodb_tnx
    sudo ln -s /usr/share/munin/plugins/mysql_ mysql_myisam_indexes
    sudo ln -s /usr/share/munin/plugins/mysql_ mysql_network_traffic
    sudo ln -s /usr/share/munin/plugins/mysql_ mysql_qcache
    sudo ln -s /usr/share/munin/plugins/mysql_ mysql_qcache_mem
    sudo ln -s /usr/share/munin/plugins/mysql_ mysql_replication
    sudo ln -s /usr/share/munin/plugins/mysql_ mysql_select_types
    sudo ln -s /usr/share/munin/plugins/mysql_ mysql_slow
    sudo ln -s /usr/share/munin/plugins/mysql_ mysql_sorts
    sudo ln -s /usr/share/munin/plugins/mysql_ mysql_table_locks
    sudo ln -s /usr/share/munin/plugins/mysql_ mysql_tmp_tables


Add file **/etc/munin/plugin-conf.d/mysql**

.. code-block:: ini

    [mysql*]
    env.mysqlconnection DBI:mysql:mysql;host=192.168.0.11;port=3306
    env.mysqluser munin
    env.mysqlpassword munin_db_password


Create mysql user munin and grant permissions 

.. code-block:: mysql

    create user munin@localhost identified by munin_db_password;
    grant process, super on *.* to 'munin'@'localhost';
    grant select on mysql.* to 'munin'@'localhost';
    flush privileges;


Test plugin

.. code-block:: bash

    cd /etc/munin/plugins
    sudo munin-run mysql_connections



Temperature Sencors Configuration
---------------------------------

.. code-block:: bash

    # Install package
    sudo yum -y install lm_sensors 

    # Add symbolic link 
    sudo ln -s /usr/share/munin/plugins/sensors_ sensors_temp

    # Test plugin
    cd /etc/munin/plugins
    sudo munin-run sensors_temp


Diskstats Inlcusion or Exclusion Configuration
----------------------------------------------

If there are some disk volumes dynamically created and removed, or only the raw disk is desired to be monitored, you may configure diskstats plugin. 

.. attention:: either **include_only** and **exclude** environment is used, both can't be used together. diskstats plugin filter disks from output of **cat /proc/diskstats** 


.. code-block:: ini

    [diskstats]
    env.exclude dm-

or use include-only

.. code-block:: ini

    [diskstats]
    env.include_only sda 


Nginx plugin configuration
--------------------------

.. code-block:: bash

    # install necessary packages (ubuntu)
    sudo apt-get install libwww-perl

    # add symbolic links
    sudo ln -s /usr/share/munin/plugins/nginx_request nginx_request
    sudo ln -s /usr/share/munin/plugins/nginx_status nginx_status


Tomcat plugin configuration
---------------------------

.. code-block:: bash

    # add symbolic links
    sudo ln -s /usr/share/munin/plugins/tomcat_access tomcat_jira_access
    sudo ln -s /usr/share/munin/plugins/tomcat_jvm tomcat_jira_jvm
    sudo ln -s /usr/share/munin/plugins/tomcat_threads tomcat_jira_threads
    sudo ln -s /usr/share/munin/plugins/tomcat_volume tomcat_jira_volume

Add file **/etc/munin/plugin-conf.d/tomcat**

.. code-block:: ini

    [tomcat_jira*]
    env.host localhost
    env.ports 9989
    env.user munin
    env.password munin_tomcat_password
    env.connector "http-bio-9999"

configure tomcat-user.xml 


configure server.xml




.. author:: default
.. categories:: none
.. tags:: none
.. comments::
