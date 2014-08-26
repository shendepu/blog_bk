MySQL/MariaDB Installation and Configuration
============================================

MariaDB Installtion
-------------------

Edit **/etc/my.cnf**

.. code-block:: cfg

    [mysqld]
    datadir=/var/lib/mysql
    socket=/var/lib/mysql/mysql.sock
    # Disabling symbolic-links is recommended to prevent assorted security risks
    symbolic-links=0
    # Settings user and group are ignored when systemd is used.
    # If you need to run mysqld under a different user or group,
    # customize your systemd unit file for mariadb according to the
    # instructions in http://fedoraproject.org/wiki/Systemd

    character-set-server = utf8
    max_allowed_packet=41943040

    [mysqld_safe]
    log-error=/var/log/mariadb/mariadb.log
    pid-file=/var/run/mariadb/mariadb.pid

    #
    # include all files from the config directory
    #
    !includedir /etc/my.cnf.d

    [client]
    socket="/var/lib/mysql/mysql.sock"

    [mysqladmin]
    socket="/var/lib/mysql/mysql.sock"


.. code-block:: bash

    # Install MariaDB
    sudo groupadd mysql
    sudo useradd -g mysql mysql
    tar -xf mariadb-10.0.12-linux-glibc_214-x86_64.tar
    sudo mv mariadb-10.0.12-linux-x86_64 /usr/local/mariadb-10.0.12
    cd /usr/local
    sudo ln -s mariadb-10.0.12 mysql
    cd mysql
    chown -R mysql:mysql .
    sudo ./scripts/mysql_install_db --user=mysql

    # Add /usr/local/mysql/bin to PATH variable
    vim ~/.bash_profile 

    PATH=$PATH:/usr/local/mysql/bin; export PATH

    source ~/.bash_profile

    mysqladmin -u root password 'PASSWORD'

    # Add mysqld service 
    sudo cp support-files/mysql.server /etc/init.d/mysqld

    sudo vim /etc/init.d/mysqld
     
    # basedir='/usr/local/mysql'
    # datadir='/var/lib/mysql'

    sudo service mysqld start
    sudo chkconfig mysqld on

    # Run mysql_secure_installtion to add more security 
    sudo ln -s /var/lib/mysql/mysql.sock /tmp/mysql.sock

    sudo mysql_secure_installation





.. author:: default
.. categories:: none
.. tags:: none
.. comments::
