Nginx Server Best Security Practices
====================================

Nginx is a lightweight, high performance web server/reverse proxy and e-mail (IMAP/POP3) proxy. It runs on UNIX, GNU/Linux, BSD variants, Mac OS X, Solaris, and Microsoft Windows. According to Netcraft, 6% of all domains on the Internet use nginx webserver. Nginx is one of a handful of servers written to address the C10K problem. Unlike traditional servers, Nginx doesn't rely on threads to handle requests. Instead it uses a much more scalable event-driven (asynchronous) architecture. Nginx powers several high traffic web sites, such as WordPress, Hulu, Github, and SourceForge. This page collects hints how to improve the security of nginx web servers running on Linux or UNIX like operating systems.

Default Config Files and Nginx Port
-----------------------------------

* **/usr/local/nginx/conf/** - The nginx server configuration directory and /usr/local/nginx/conf/nginx.conf is main configuration file.
* **/usr/local/nginx/html/** - The default document location.
* **/usr/local/nginx/logs/** - The default log file location.
* **Nginx HTTP default port** : TCP 80
* **Nginx HTTPS default port** : TCP 443

  
You can test nginx configuration changes as follows:

.. code-block:: bash

    /usr/local/nginx/sbin/nginx -t

Sample outputs:

::

    the configuration file /usr/local/nginx/conf/nginx.conf syntax is ok
    configuration file /usr/local/nginx/conf/nginx.conf test is successful

To load config changes, type:

.. code-block:: bash

    /usr/local/nginx/sbin/nginx -s reload

To stop server, type:

.. code-block:: bash

    /usr/local/nginx/sbin/nginx -s stop

#1: Turn On SELinux
-------------------

Security-Enhanced Linux (SELinux) is a Linux kernel feature that provides a mechanism for supporting access control security policies which provides great protection. It can stop many attacks before your system rooted. See how to turn on `SELinux for CentOS or RHEL`_ based systems.

.. _SELinux for CentOS or RHEL: http://www.cyberciti.biz/faq/rhel-fedora-redhat-selinux-protection/ 

Do Boolean Lockdown
^^^^^^^^^^^^^^^^^^^

Run the getsebool -a command and lockdown system:

.. code-block:: bash

    getsebool -a | less
    getsebool -a | grep off
    getsebool -a | grep o

To secure the machine, look at settings which are set to 'on' and change to 'off' if they do not apply to your setup with the help of setsebool command. Set correct SE Linux booleans to maintain functionality and protection. Please note that SELinux adds 2-8% overheads to typical RHEL or CentOS installation.

#2: Allow Minimal Privileges Via Mount Options
----------------------------------------------

Server all your webpages / html / php files via separate partitions. For example, create a partition called /dev/sda5 and mount at the /nginx. Make sure /nginx is mounted with **noexec, nodev and nosetuid** permissions. Here is my /etc/fstab entry for mounting /nginx:

.. code-block:: cfg

    LABEL=/nginx   /nginx  ext3   defaults,nosuid,noexec,nodev 1 2

Note you need to create a new partition using `fdisk and mkfs.ext3`_ commands.

.. _fdisk and mkfs.ext3: http://www.cyberciti.biz/faq/redhat-centos-linux-ext3-filesystem-format-command/  

#3: Linux /etc/sysctl.conf Hardening
------------------------------------

You can control and configure Linux kernel and networking settings via **/etc/sysctl.conf**.

.. code-block:: cfg

    # Avoid a smurf attack
    net.ipv4.icmp_echo_ignore_broadcasts = 1
 
    # Turn on protection for bad icmp error messages
    net.ipv4.icmp_ignore_bogus_error_responses = 1
 
    # Turn on syncookies for SYN flood attack protection
    net.ipv4.tcp_syncookies = 1
 
    # Turn on and log spoofed, source routed, and redirect packets
    net.ipv4.conf.all.log_martians = 1
    net.ipv4.conf.default.log_martians = 1
 
    # No source routed packets here
    net.ipv4.conf.all.accept_source_route = 0
    net.ipv4.conf.default.accept_source_route = 0
 
    # Turn on reverse path filtering
    net.ipv4.conf.all.rp_filter = 1
    net.ipv4.conf.default.rp_filter = 1
 
    # Make sure no one can alter the routing tables
    net.ipv4.conf.all.accept_redirects = 0
    net.ipv4.conf.default.accept_redirects = 0
    net.ipv4.conf.all.secure_redirects = 0
    net.ipv4.conf.default.secure_redirects = 0
 
    # Don't act as a router
    net.ipv4.ip_forward = 0
    net.ipv4.conf.all.send_redirects = 0
    net.ipv4.conf.default.send_redirects = 0
 
 
    # Turn on execshild
    kernel.exec-shield = 1
    kernel.randomize_va_space = 1
 
    # Tuen IPv6
    net.ipv6.conf.default.router_solicitations = 0
    net.ipv6.conf.default.accept_ra_rtr_pref = 0
    net.ipv6.conf.default.accept_ra_pinfo = 0
    net.ipv6.conf.default.accept_ra_defrtr = 0
    net.ipv6.conf.default.autoconf = 0
    net.ipv6.conf.default.dad_transmits = 0
    net.ipv6.conf.default.max_addresses = 1
 
    # Optimization for port usefor LBs
    # Increase system file descriptor limit
    fs.file-max = 65535
 
    # Allow for more PIDs (to reduce rollover problems); may break some programs 32768
    kernel.pid_max = 65536
 
    # Increase system IP port limits
    net.ipv4.ip_local_port_range = 2000 65000
 
    # Increase TCP max buffer size setable using setsockopt()
    net.ipv4.tcp_rmem = 4096 87380 8388608
    net.ipv4.tcp_wmem = 4096 87380 8388608
 
    # Increase Linux auto tuning TCP buffer limits
    # min, default, and max number of bytes to use
    # set max to at least 4MB, or higher if you use very high BDP paths
    # Tcp Windows etc
    net.core.rmem_max = 8388608
    net.core.wmem_max = 8388608
    net.core.netdev_max_backlog = 5000
    net.ipv4.tcp_window_scaling = 1

See also:

* `Linux Tuning The VM`_  (memory) Subsystem
* `Linux Tune Network Stack`_  (Buffers Size) To Increase Networking Performance

.. _Linux Tune Network Stack: http://www.cyberciti.biz/faq/linux-tcp-tuning/ 

.. _Linux Tuning The VM: http://www.cyberciti.biz/faq/linux-kernel-tuning-virtual-memory-subsystem/ 

#4: Remove All Unwanted Nginx Modules
-------------------------------------

You need to minimizes the number of modules that are compiled directly into the nginx binary. This minimizes risk by limiting the capabilities allowed by the webserver. You can configure and install nginx using only required modules. For example, disable SSI and autoindex module you can type:

.. code-block:: bash

    ./configure --without-http_autoindex_module \
                --without-http_ssi_module
    make
    make install

Type the following command to see which modules can be turn on or off while compiling nginx server:

.. code-block:: bash

    ./configure --help | less

Disable nginx modules that you don't need.

(Optional) Change Nginx Version Header
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Edit **src/http/ngx_http_header_filter_module.c**, enter:

.. code-block:: bash

    vi +48 src/http/ngx_http_header_filter_module.c

Find line

.. code-block:: c

    static char ngx_http_server_string[] = "Server: nginx" CRLF;
    static char ngx_http_server_full_string[] = "Server: " NGINX_VER CRLF;

Change them as follows:

.. code-block:: c

    static char ngx_http_server_string[] = "Server: Ninja Web Server" CRLF;
    static char ngx_http_server_full_string[] = 
                              "Server: Ninja Web Server" CRLF;

Save and close the file. Now, you can compile the server. Add the following in nginx.conf to turn off nginx version number displayed on all auto generated error pages:

.. code-block:: nginx

    server_tokens off

#5: Use mod_security (only for backend Apache servers)
------------------------------------------------------

mod_security provides an application level firewall for Apache. Install `mod_security for all backend`_ Apache web servers. This will stop many injection attacks.

.. _mod_security for all backend: http://www.cyberciti.biz/faq/rhel-fedora-centos-httpd-mod_security-configuration/

#6: Install SELinux Policy To Harden The Nginx Webserver
--------------------------------------------------------

By default SELinux will not protect the nginx web server. However, you can install and compile protection as follows. First, install required SELinux compile time support:

.. code-block:: bash

    yum -y install selinux-policy-targeted selinux-policy-devel

Download targeted SELinux policies to harden the nginx webserver on Linux servers from the `nginx selinux project home`_ page:

.. _nginx selinux project home: http://sourceforge.net/projects/selinuxnginx/

.. code-block:: bash

    cd /opt
    wget 'http://downloads.sourceforge.net/project/selinuxnginx/se-ngix_1_0_10.tar.gz?use_mirror=nchc'

    # Untar the same:
    tar -zxvf se-ngix_1_0_10.tar.gz
    
    # Compile the same
    cd se-ngix_1_0_10/nginx
    make

Sample outputs:

::

    Compiling targeted nginx module
    /usr/bin/checkmodule:  loading policy configuration from tmp/nginx.tmp
    /usr/bin/checkmodule:  policy configuration loaded
    /usr/bin/checkmodule:  writing binary representation (version 6) to tmp/nginx.mod
    Creating targeted nginx.pp policy package
    rm tmp/nginx.mod.fc tmp/nginx.mod

Install the resulting nginx.pp SELinux module:

.. code-block:: bash

    /usr/sbin/semodule -i nginx.pp

#7: Restrictive Iptables Based Firewall
---------------------------------------

The following firewall script blocks everything and only allows:

* Incoming HTTP (TCP port 80) requests
* Incoming ICMP ping requests
* Outgoing ntp (port 123) requests
* Outgoing smtp (TCP port 25) requests

.. code-block:: bash

    #!/bin/bash
    IPT="/sbin/iptables"
 
    #### IPS ######
    # Get server public ip 
    SERVER_IP=$(ifconfig eth0 | grep 'inet addr:' | awk -F'inet addr:' '{ print $2}' | awk '{ print $1}')
    LB1_IP="204.54.1.1"
    LB2_IP="204.54.1.2"
 
    # Do some smart logic so that we can use damm script on LB2 too
    OTHER_LB=""
    SERVER_IP=""
    [[ "$SERVER_IP" == "$LB1_IP" ]] && OTHER_LB="$LB2_IP" || OTHER_LB="$LB1_IP"
    [[ "$OTHER_LB" == "$LB2_IP" ]] && OPP_LB="$LB1_IP" || OPP_LB="$LB2_IP"
 
    ### IPs ###
    PUB_SSH_ONLY="122.xx.yy.zz/29"
 
    #### FILES #####
    BLOCKED_IP_TDB=/root/.fw/blocked.ip.txt
    SPOOFIP="127.0.0.0/8 192.168.0.0/16 172.16.0.0/12 10.0.0.0/8 169.254.0.0/16 0.0.0.0/8 240.0.0.0/4 255.255.255.255/32 168.254.0.0/16 224.0.0.0/4 240.0.0.0/5 248.0.0.0/5 192.0.2.0/24"
    BADIPS=$( [[ -f ${BLOCKED_IP_TDB} ]] && egrep -v "^#|^$" ${BLOCKED_IP_TDB})
     
    ### Interfaces ###
    PUB_IF="eth0"   # public interface
    LO_IF="lo"      # loopback
    VPN_IF="eth1"   # vpn / private net
     
    ### start firewall ###
    echo "Setting LB1 $(hostname) Firewall..."
     
    # DROP and close everything 
    $IPT -P INPUT DROP
    $IPT -P OUTPUT DROP
    $IPT -P FORWARD DROP
     
    # Unlimited lo access
    $IPT -A INPUT -i ${LO_IF} -j ACCEPT
    $IPT -A OUTPUT -o ${LO_IF} -j ACCEPT
     
    # Unlimited vpn / pnet access
    $IPT -A INPUT -i ${VPN_IF} -j ACCEPT
    $IPT -A OUTPUT -o ${VPN_IF} -j ACCEPT
     
    # Drop sync
    $IPT -A INPUT -i ${PUB_IF} -p tcp ! --syn -m state --state NEW -j DROP
     
    # Drop Fragments
    $IPT -A INPUT -i ${PUB_IF} -f -j DROP
     
    $IPT  -A INPUT -i ${PUB_IF} -p tcp --tcp-flags ALL FIN,URG,PSH -j DROP
    $IPT  -A INPUT -i ${PUB_IF} -p tcp --tcp-flags ALL ALL -j DROP
     
    # Drop NULL packets
    $IPT  -A INPUT -i ${PUB_IF} -p tcp --tcp-flags ALL NONE -m limit --limit 5/m --limit-burst 7 -j LOG --log-prefix " NULL Packets "
    $IPT  -A INPUT -i ${PUB_IF} -p tcp --tcp-flags ALL NONE -j DROP
     
    $IPT  -A INPUT -i ${PUB_IF} -p tcp --tcp-flags SYN,RST SYN,RST -j DROP
     
    # Drop XMAS
    $IPT  -A INPUT -i ${PUB_IF} -p tcp --tcp-flags SYN,FIN SYN,FIN -m limit --limit 5/m --limit-burst 7 -j LOG --log-prefix " XMAS Packets "
    $IPT  -A INPUT -i ${PUB_IF} -p tcp --tcp-flags SYN,FIN SYN,FIN -j DROP
     
    # Drop FIN packet scans
    $IPT  -A INPUT -i ${PUB_IF} -p tcp --tcp-flags FIN,ACK FIN -m limit --limit 5/m --limit-burst 7 -j LOG --log-prefix " Fin Packets Scan "
    $IPT  -A INPUT -i ${PUB_IF} -p tcp --tcp-flags FIN,ACK FIN -j DROP
     
    $IPT  -A INPUT -i ${PUB_IF} -p tcp --tcp-flags ALL SYN,RST,ACK,FIN,URG -j DROP
     
    # Log and get rid of broadcast / multicast and invalid 
    $IPT  -A INPUT -i ${PUB_IF} -m pkttype --pkt-type broadcast -j LOG --log-prefix " Broadcast "
    $IPT  -A INPUT -i ${PUB_IF} -m pkttype --pkt-type broadcast -j DROP
     
    $IPT  -A INPUT -i ${PUB_IF} -m pkttype --pkt-type multicast -j LOG --log-prefix " Multicast "
    $IPT  -A INPUT -i ${PUB_IF} -m pkttype --pkt-type multicast -j DROP
     
    $IPT  -A INPUT -i ${PUB_IF} -m state --state INVALID -j LOG --log-prefix " Invalid "
    $IPT  -A INPUT -i ${PUB_IF} -m state --state INVALID -j DROP
     
    # Log and block spoofed ips
    $IPT -N spooflist
    for ipblock in $SPOOFIP
    do
             $IPT -A spooflist -i ${PUB_IF} -s $ipblock -j LOG --log-prefix " SPOOF List Block "
             $IPT -A spooflist -i ${PUB_IF} -s $ipblock -j DROP
    done
    $IPT -I INPUT -j spooflist
    $IPT -I OUTPUT -j spooflist
    $IPT -I FORWARD -j spooflist
     
    # Allow ssh only from selected public ips
    for ip in ${PUB_SSH_ONLY}
    do
            $IPT -A INPUT -i ${PUB_IF} -s ${ip} -p tcp -d ${SERVER_IP} --destination-port 22 -j ACCEPT
            $IPT -A OUTPUT -o ${PUB_IF} -d ${ip} -p tcp -s ${SERVER_IP} --sport 22 -j ACCEPT
    done
     
    # allow incoming ICMP ping pong stuff
    $IPT -A INPUT -i ${PUB_IF} -p icmp --icmp-type 8 -s 0/0 -m state --state NEW,ESTABLISHED,RELATED -m limit --limit 30/sec  -j ACCEPT
    $IPT -A OUTPUT -o ${PUB_IF} -p icmp --icmp-type 0 -d 0/0 -m state --state ESTABLISHED,RELATED -j ACCEPT
     
    # allow incoming HTTP port 80
    $IPT -A INPUT -i ${PUB_IF} -p tcp -s 0/0 --sport 1024:65535 --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT
    $IPT -A OUTPUT -o ${PUB_IF} -p tcp --sport 80 -d 0/0 --dport 1024:65535 -m state --state ESTABLISHED -j ACCEPT
     
     
    # allow outgoing ntp 
    $IPT -A OUTPUT -o ${PUB_IF} -p udp --dport 123 -m state --state NEW,ESTABLISHED -j ACCEPT
    $IPT -A INPUT -i ${PUB_IF} -p udp --sport 123 -m state --state ESTABLISHED -j ACCEPT
     
    # allow outgoing smtp
    $IPT -A OUTPUT -o ${PUB_IF} -p tcp --dport 25 -m state --state NEW,ESTABLISHED -j ACCEPT
    $IPT -A INPUT -i ${PUB_IF} -p tcp --sport 25 -m state --state ESTABLISHED -j ACCEPT
     
    ### add your other rules here ####
 
    #######################
    # drop and log everything else
    $IPT -A INPUT -m limit --limit 5/m --limit-burst 7 -j LOG --log-prefix " DEFAULT DROP "
    $IPT -A INPUT -j DROP
     
    exit 0

#8: Controlling Buffer Overflow Attacks
---------------------------------------

Edit **nginx.conf** and set the buffer size limitations for all clients.

.. code-block:: bash

    vi /usr/local/nginx/conf/nginx.conf

Edit and set the buffer size limitations for all clients as follows:

.. code-block:: nginx

    ## Start: Size Limits & Buffer Overflows ##
    client_body_buffer_size  1K;
    client_header_buffer_size 1k;
    client_max_body_size 1k;
    large_client_header_buffers 2 1k;
    ## END: Size Limits & Buffer Overflows ##

Where,

1. **client_body_buffer_size 1k** - (default is 8k or 16k) The directive specifies the client request body buffer size.
2. **client_header_buffer_size 1k** - Directive sets the headerbuffer size for the request header from client. For the overwhelming majority of requests a buffer size of 1K is sufficient. Increase this if you have a custom header or a large cookie sent from the client (e.g., wap client).
3. **client_max_body_size 1k**- Directive assigns the maximum accepted body size of client request, indicated by the line Content-Length in the header of request. If size is greater the given one, then the client gets the error "Request Entity Too Large" (413). Increase this when you are getting file uploads via the POST method.
4. **large_client_header_buffers 2 1k** - Directive assigns the maximum number and size of buffers for large headers to read from client request. By default the size of one buffer is equal to the size of page, depending on platform this either 4K or 8K, if at the end of working request connection converts to state keep-alive, then these buffers are freed. 2x1k will accept 2kB data URI. This will also help combat bad bots and DoS attacks.

You also need to control timeouts to improve server performance and cut clients. Edit it as follows:

.. code-block:: nginx

    ## Start: Timeouts ##
    client_body_timeout   10;
    client_header_timeout 10;
    keepalive_timeout     5 5;
    send_timeout          10;
    ## End: Timeouts ##

1. **client_body_timeout 10**; - Directive sets the read timeout for the request body from client. The timeout is set only if a body is not get in one readstep. If after this time the client send nothing, nginx returns error "Request time out" (408). The default is 60.
2. **client_header_timeout 10**; - Directive assigns timeout with reading of the title of the request of client. The timeout is set only if a header is not get in one readstep. If after this time the client send nothing, nginx returns error "Request time out" (408).
3. **keepalive_timeout 5 5**; - The first parameter assigns the timeout for keep-alive connections with the client. The server will close connections after this time. The optional second parameter assigns the time value in the header Keep-Alive: timeout=time of the response. This header can convince some browsers to close the connection, so that the server does not have to. Without this parameter, nginx does not send a Keep-Alive header (though this is not what makes a connection "keep-alive").
4. **send_timeout 10**; - Directive assigns response timeout to client. Timeout is established not on entire transfer of answer, but only between two operations of reading, if after this time client will take nothing, then nginx is shutting down the connection.

#9: Control Simultaneous Connections
------------------------------------

You can use NginxHttpLimitZone module to limit the number of simultaneous connections for the assigned session or as a special case, from one IP address. Edit nginx.conf:

.. code-block:: nginx

    ## Only requests to our Host are allowed i.e. nixcraft.in, 
    ## images.nixcraft.in and www.nixcraft.in
    if ($host !~ ^(nixcraft.in|www.nixcraft.in|images.nixcraft.in)$ ) {
     return 444;
    }
    ##

The above will limits remote clients to no more than 5 concurrently "open" connections per remote ip address.

#10: Allow Access To Our Domain Only
------------------------------------

If bot is just making random server scan for all domains, just deny it. You must only allow configured virtual domain or reverse proxy requests. You don't want to display request using an IP address:

.. code-block:: nginx

    ## Only requests to our Host are allowed i.e. nixcraft.in, images.nixcraft.in and www.nixcraft.in
    if ($host !~ ^(nixcraft.in|www.nixcraft.in|images.nixcraft.in)$ ) {
     return 444;
    }
    ##

#11: Limit Available Methods
----------------------------

GET and POST are the most common methods on the Internet. Web server methods are defined in `RFC 2616`_ . If a web server does not require the implementation of all available methods, they should be disabled. The following will filter and only allow GET, HEAD and POST methods:

.. _RFC 2616: http://www.ietf.org/rfc/rfc2616.txt

.. code-block:: nginx

    ## Only allow these request methods ##
    if ($request_method !~ ^(GET|HEAD|POST)$ ) {
     return 444;
    }
    ## Do not accept DELETE, SEARCH and other methods ##

More About HTTP Methods
^^^^^^^^^^^^^^^^^^^^^^^

* The GET method is used to request document such as http://www.cyberciti.biz/index.php.
* The HEAD method is identical to GET except that the server MUST NOT return a message-body in the response.
* The POST method may involve anything, like storing or updating data, or ordering a product, or sending E-mail by submitting the form. This is usually processed using the server side scripting such as PHP, PERL, Python and so on. You must use this if you want to upload files and process forms on server.

#12: How Do I Deny Certain User-Agents?
---------------------------------------

You can easily block user-agents i.e. scanners, bots, and spammers who may be abusing your server.

.. code-block:: nginx

    ## Block download agents ##
    if ($http_user_agent ~* LWP::Simple|BBBike|wget) {
        return 403;
    }
    ##

Block robots called msnbot and scrapbot:

.. code-block:: nginx

    ## Block some robots ##
    if ($http_user_agent ~* msnbot|scrapbot) {
        return 403;
    }

#12: How Do I Block Referral Spam?
----------------------------------

Referer spam is dengerouns. It can harm your SEO ranking via web-logs (if published) as referer field refer to their spammy site. You can block access to referer spammers with these lines.

.. code-block:: nginx

    ## Deny certain Referers ###
    if ( $http_referer ~* (babes|forsale|girl|jewelry|love|nudit|organic|poker|porn|sex|teen) )
    {
     # return 404;
     return 403;
    }
    ##

#13: How Do I Stop Image Hotlinking?
------------------------------------

Image or HTML hotlinking means someone makes a link to your site to one of your images, but displays it on their own site. The end result you will end up paying for bandwidth bills and make the content look like part of the hijacker's site. This is usually done on forums and blogs. I strongly suggest you block and stop image hotlinking at your server level itself.

.. code-block:: nginx

    # Stop deep linking or hot linking
    location /images/ {
      valid_referers none blocked www.example.com example.com;
       if ($invalid_referer) {
         return   403;
       }
    }

Example: Rewrite And Display Image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Another example with link to banned image:

.. code-block:: nginx

    valid_referers blocked www.example.com example.com;
    if ($invalid_referer) {
        rewrite ^/images/uploads.*\.(gif|jpg|jpeg|png)$ 
                http://www.examples.com/banned.jpg last
    }

See also:

* HowTo: `Use nginx map`_ to block image hotlinking. This is useful if you want to block tons of domains.
 
.. _Use nginx map: http://nginx.org/pipermail/nginx/2007-June/001082.html

#14: Directory Restrictions
---------------------------

You can set access control for a specified directory. All web directories should be configured on a case-by-case basis, allowing access only where needed.

Limiting Access By Ip Address
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can limit access to directory `by ip address`_ to /docs/ directory:

.. _by ip address: http://www.cyberciti.biz/faq/linux-unix-nginx-access-control-howto/

.. code-block:: nginx

    location /docs/ {
        ## block one workstation
        deny    192.168.1.1;
        ## allow anyone in 192.168.1.0/24
        allow   192.168.1.0/24;
        ## drop rest of the world
        deny    all;
    }

Password Protect The Directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First create the password file and add a user called vivek:

.. code-block:: bash

    mkdir /usr/local/nginx/conf/.htpasswd/
    htpasswd -c /usr/local/nginx/conf/.htpasswd/passwd vivek

Edit **nginx.conf** and protect the required directories as follows:

.. code-block:: nginx

    ### Password Protect /personal-images/ and /delta/ directories ###
    location ~ /(personal-images/.*|delta/.*) {
        auth_basic  "Restricted";
        auth_basic_user_file   /usr/local/nginx/conf/.htpasswd/passwd;
    }

Once a password file has been generated, subsequent users can be added with the following command:

.. code-block:: bash

    htpasswd -s /usr/local/nginx/conf/.htpasswd/passwd userName

#15: Nginx SSL Configuration
----------------------------

HTTP is a plain text protocol and it is open to passive monitoring. You should use SSL to to encrypt your content for users.

Create an SSL Certificate
^^^^^^^^^^^^^^^^^^^^^^^^^

Type the following commands:

.. code-block:: bash

    cd /usr/local/nginx/conf
    openssl genrsa -des3 -out server.key 1024
    openssl req -new -key server.key -out server.csr
    cp server.key server.key.org
    openssl rsa -in server.key.org -out server.key
    openssl x509 -req -days 365 -in server.csr -signkey server.key \
            -out server.crt

Edit **nginx.conf** and update it as follows:

.. code-block:: nginx

    server {
        server_name example.com;
        listen 443;
        ssl on;
        ssl_certificate /usr/local/nginx/conf/server.crt;
        ssl_certificate_key /usr/local/nginx/conf/server.key;
        access_log /usr/local/nginx/logs/ssl.access.log;
        error_log /usr/local/nginx/logs/ssl.error.log;
    }

Restart the nginx:

.. code-block:: bash

    /usr/local/nginx/sbin/nginx -s reload

See also:

* For more information, read the `Nginx SSL documentation`_ .
 
.. _Nginx SSL documentation: http://wiki.nginx.org/NginxHttpSslModule

#16: Nginx And PHP Security Tips
--------------------------------

PHP is one of the popular server side scripting language. Edit /etc/php.ini as follows:

.. code-block:: cfg

    # Disallow dangerous functions
    disable_functions = phpinfo, system, mail, exec
     
    ## Try to limit resources  ##
     
    # Maximum execution time of each script, in seconds
    max_execution_time = 30
     
    # Maximum amount of time each script may spend parsing request data
    max_input_time = 60
     
    # Maximum amount of memory a script may consume (8MB)
    memory_limit = 8M
     
    # Maximum size of POST data that PHP will accept.
    post_max_size = 8M
     
    # Whether to allow HTTP file uploads.
    file_uploads = Off
     
    # Maximum allowed size for uploaded files.
    upload_max_filesize = 2M
     
    # Do not expose PHP error messages to external users
    display_errors = Off
     
    # Turn on safe mode
    safe_mode = On
     
    # Only allow access to executables in isolated directory
    safe_mode_exec_dir = php-required-executables-path
     
    # Limit external access to PHP environment
    safe_mode_allowed_env_vars = PHP_
     
    # Restrict PHP information leakage
    expose_php = Off
     
    # Log all errors
    log_errors = On
     
    # Do not register globals for input data
    register_globals = Off
     
    # Minimize allowable PHP post size
    post_max_size = 1K
     
    # Ensure PHP redirects appropriately
    cgi.force_redirect = 0
     
    # Disallow uploading unless necessary
    file_uploads = Off
     
    # Enable SQL safe mode
    sql.safe_mode = On
     
    # Avoid Opening remote files
    allow_url_fopen = Off

See also:

* `PHP Security Limit Resources Used By Script`_ 
* `PHP.INI settings Disable exec, shell_exec, system, popen and Other Functions To Improve Security`_  

.. _PHP Security Limit Resources Used By Script: http://www.cyberciti.biz/faq/php-resources-limits/ 
.. _PHP.INI settings Disable exec, shell_exec, system, popen and Other Functions To Improve Security: http://www.cyberciti.biz/faq/linux-unix-apache-lighttpd-phpini-disable-functions/

#17: Run Nginx In A Chroot Jail (Containers) If Possible
--------------------------------------------------------

Putting nginx in a chroot jail minimizes the damage done by a potential break-in by isolating the web server to a small section of the filesystem. You can use `traditional chroot`_ kind of setup with nginx. If possible use `FreeBSD jails`_ , `XEN`_ , or `OpenVZ`_ virtualization which uses the concept of containers.
 
.. _traditional chroot: http://www.cyberciti.biz/faq/howto-run-nginx-in-a-chroot-jail/ 
.. _FreeBSD jails: http://www.cyberciti.biz/faq/howto-setup-freebsd-jail-with-ezjail/ 
.. _XEN: http://www.cyberciti.biz/tips/rhel-centos-xen-virtualization-installation-howto.html
.. _OpenVZ: http://www.cyberciti.biz/faq/openvz-rhel-centos-linux-tutorial/

#18: Limits Connections Per IP At The Firewall Level
----------------------------------------------------

A webserver must keep an eye on connections and limit connections per second. This is serving 101. Both pf and iptables can throttle end users before accessing your nginx server.

Linux Iptables: Throttle Nginx Connections Per Second
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following example will drop incoming connections if IP make more than 15 connection attempts to port 80 within 60 seconds:

.. code-block:: bash

    /sbin/iptables -A INPUT -p tcp --dport 80 -i eth0 -m state --state NEW \
            -m recent --set
    /sbin/iptables -A INPUT -p tcp --dport 80 -i eth0 -m state --state NEW \
            -m recent --update --seconds 60  --hitcount 15 -j DROP
    service iptables save

BSD PF: Throttle Nginx Connections Per Second
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Edit your **/etc/pf.conf** and update it as follows. The following will limits the maximum number of connections per source to 100. 15/5 specifies the number of connections per second or span of seconds i.e. rate limit the number of connections to 15 in a 5 second span. If anyone breaks our rules add them to our abusive_ips table and block them for making any further connections. Finally, flush keyword kills all states created by the matching rule which originate from the host which exceeds these limits.

.. code-block:: cfg

    webserver_ip="202.54.1.1"
    table <abusive_ips> persist
    block in quick from <abusive_ips>
    pass in on $ext_if proto tcp to $webserver_ip port www flags S/SA keep state (max-src-conn 100, max-src-conn-rate 15/5, overload <abusive_ips> flush)

Please adjust all values as per your requirements and traffic (browsers may open multiple connections to your site). See also:

* Sample `PF firewall`_ script.
* Sample `Iptables firewall`_ script.
 
.. _PF firewall: http://bash.cyberciti.biz/firewall/pf-firewall-script/
.. _Iptables firewall: http://bash.cyberciti.biz/firewall/linux-iptables-firewall-shell-script-for-standalone-server/

#19: Configure Operating System to Protect Web Server
-----------------------------------------------------

Turn on SELinux as described above. Set correct permissions on /nginx document root. The nginx runs as a user named nginx. However, the files in the DocumentRoot (/nginx or /usr/local/nginx/html) should not be owned or writable by that user. To find files with wrong permissions, use:

.. code-block:: bash

    find /nginx -user nginx
    find /usr/local/nginx/html -user nginx

Make sure you change file ownership to root or other user. A typical set of permission **/usr/local/nginx/html/**

.. code-block:: bash

    ls -l /usr/local/nginx/html/

Sample outputs:

::

    -rw-r--r-- 1 root root 925 Jan  3 00:50 error4xx.html
    -rw-r--r-- 1 root root  52 Jan  3 10:00 error5xx.html
    -rw-r--r-- 1 root root 134 Jan  3 00:52 index.html

You must delete unwated backup files created by vi or other text editor:

.. code-block:: bash

    find /nginx -name '.?*' -not -name .ht* -or -name '*~' -or -name '*.bak*' \
                -or -name '*.old*'
    find /usr/local/nginx/html/ -name '.?*' -not -name .ht* -or -name '*~' \
                -or -name '*.bak*' -or -name '*.old*'

Pass -delete option to find command and it will get rid of those files too.

#20: Restrict Outgoing Nginx Connections
----------------------------------------

The crackers will download file locally on your server using tools such as wget. Use iptables to block outgoing connections from nginx user. The `ipt_owner module attempts`_ to match various characteristics of the packet creator, for locally generated packets. It is only valid in the OUTPUT chain. In this example, allow vivek user to connect outside using port 80 (useful for RHN access or to grab CentOS updates via repos):

.. _ipt_owner module attempts: http://www.cyberciti.biz/tips/block-outgoing-network-access-for-a-single-user-from-my-server-using-iptables.html

.. code-block:: bash

    /sbin/iptables -A OUTPUT -o eth0 -m owner --uid-owner vivek -p tcp \
            --dport 80 -m state --state NEW,ESTABLISHED  -j ACCEPT

Add above rule to your iptables based shell script. Do not allow nginx web server user to connect outside.

Bounce Tip: Watching Your Logs & Auditing
-----------------------------------------

Check the Log files. They will give you some understanding of what attacks is thrown against the server and allow you to check if the necessary level of security is present or not.

.. code-block:: bash

    grep "/login.php??" /usr/local/nginx/logs/access_log
    grep "...etc/passwd" /usr/local/nginx/logs/access_log
    egrep -i "denied|error|warn" /usr/local/nginx/logs/error_log

The auditd service is provided for system auditing. Turn it on to audit service SELinux events, authetication events, file modifications, account modification and so on. As usual disable all services and follow our "`Linux Server Hardening`_" security tips. 

.. _Linux Server Hardening: http://www.cyberciti.biz/tips/linux-security.html

Conclusion
----------

Your nginx server is now properly harden and ready to server webpages. However, you should be consulted further resources for your web applications security needs. For example, wordpress or any other third party apps has its own security requirements.

References:
-----------

* HowTo: Setup `nginx reverse proxy`_ and HA cluser with the help of keepalived.
* `nginx wiki`_ - The official nginx wiki.
* OpenBSD specific Nginx installation and security how to.



.. _nginx reverse proxy: http://www.cyberciti.biz/faq/series/keepalived-nginx-ha-cluster/ 
.. _nginx wiki: http://wiki.nginx.org/Main


This article is copied from http://www.cyberciti.biz/tips/linux-unix-bsd-nginx-webserver-security.html
------------------------------------------------------------------------------------------------------

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
