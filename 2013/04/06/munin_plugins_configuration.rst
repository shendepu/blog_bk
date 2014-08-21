Munin Plugins Configuration
===========================

MySQL Configuration
-------------------

.. code-block:: bash

    # Install necessary perl packages 
    yum -y install perl-Cache-Cache

    # Add symbolic link for mysql plugin 
    ln -s /usr/share/munin/plugins/mysql_ mysql_bin_relay_log
    ln -s /usr/share/munin/plugins/mysql_ mysql_commands
    ln -s /usr/share/munin/plugins/mysql_ mysql_connections
    ln -s /usr/share/munin/plugins/mysql_ mysql_files_tables
    ln -s /usr/share/munin/plugins/mysql_ mysql_innodb_bpool
    ln -s /usr/share/munin/plugins/mysql_ mysql_innodb_bpool_act
    ln -s /usr/share/munin/plugins/mysql_ mysql_innodb_io
    ln -s /usr/share/munin/plugins/mysql_ mysql_innodb_log
    ln -s /usr/share/munin/plugins/mysql_ mysql_innodb_rows
    ln -s /usr/share/munin/plugins/mysql_ mysql_innodb_semaphores
    ln -s /usr/share/munin/plugins/mysql_ mysql_innodb_tnx
    ln -s /usr/share/munin/plugins/mysql_ mysql_myisam_indexes
    ln -s /usr/share/munin/plugins/mysql_ mysql_network_traffic
    ln -s /usr/share/munin/plugins/mysql_ mysql_qcache
    ln -s /usr/share/munin/plugins/mysql_ mysql_qcache_mem
    ln -s /usr/share/munin/plugins/mysql_ mysql_replication
    ln -s /usr/share/munin/plugins/mysql_ mysql_select_types
    ln -s /usr/share/munin/plugins/mysql_ mysql_slow
    ln -s /usr/share/munin/plugins/mysql_ mysql_sorts
    ln -s /usr/share/munin/plugins/mysql_ mysql_table_locks
    ln -s /usr/share/munin/plugins/mysql_ mysql_tmp_tables


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
    munin-run mysql_connections



Temperature Sencors Configuration
---------------------------------

.. code-block:: bash

    # Install package
    yum -y install lm_sensors 

    # Add symbolic link 
    ln -s /usr/share/munin/plugins/sensors_ sensors_temp

    # Test plugin
    cd /etc/munin/plugins
    munin-run sensors_temp


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


Tomcat plugin configuration
---------------------------

.. code-block:: bash

    # add symbolic links
    ln -s /usr/share/munin/plugins/tomcat_access tomcat_jira_access
    ln -s /usr/share/munin/plugins/tomcat_jvm tomcat_jira_jvm
    ln -s /usr/share/munin/plugins/tomcat_threads tomcat_jira_threads
    ln -s /usr/share/munin/plugins/tomcat_volume tomcat_jira_volume

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
