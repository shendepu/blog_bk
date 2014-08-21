************************************
Nginx Installation and Configuration
************************************

Installation
============

.. code-block:: bash

    ./configure --sbin-path=/usr/local/nginx/nginx \
	    	--conf-path=/usr/local/nginx/nginx.conf \
	    	--pid-path=/var/run/nginx.pid \
	    	--error-log-path=/var/log/nginx/error.log \
	    	--http-log-path=/var/log/nginx/access.log \
	    	--user=nginx --group=nginx \
	    	--with-http_ssl_module \
	    	--with-http_stub_status_module \
	    	--with-pcre=../pcre-8.35 \
	    	--with-zlib=../zlib-1.2.8 \
	    	--with-openssl=../openssl-1.0.1h


Configuration
=============

nginx.conf 

.. code-block:: nginx

    user  nginx;
	worker_processes  4;

	error_log  logs/error.log;

	pid        logs/nginx.pid;

	events {
	    worker_connections 	65535;
	}

	http {
	    include       mime.types;
	    default_type  application/octet-stream;

	    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
	                      '$status $body_bytes_sent "$http_referer" '
	                      '"$http_user_agent" "$http_x_forwarded_for"';
	    access_log  logs/access.log  main;

	    sendfile        on;
	    #tcp_nopush     on;
	    client_max_body_size 1000m;
	    keepalive_timeout  10;
	    gzip  on;
	    ssl_session_cache	shared:SSL:20m;
	    ssl_session_timeout	10m;

	    #fastcgi_cache_path /usr/local/nginx/fastcgi_cache 
	    #                   levels=1:2 keys_zone=TEST:10m inactive=5m;    
	    #fastcgi_connect_timeout 300;    
	    #fastcgi_send_timeout 300;    
	    #fastcgi_read_timeout 300;    
	    #fastcgi_buffer_size 64k;    
	    #fastcgi_buffers 4 64k;    
	    #fastcgi_busy_buffers_size 128k;    
	    #fastcgi_temp_file_write_size 128k;    
	    #fastcgi_cache TEST;    
	    #fastcgi_cache_valid 200 302 1h;    
	    #fastcgi_cache_valid 301 1d;    
	    #fastcgi_cache_valid any 1m;
 
	    include conf/bizforce-monitor.conf; 
	}

bizforce-monitor.conf: Nginx status，Munin及Nagios配置：

.. code-block:: nginx

    server {
        listen 127.0.0.1;
        server_name localhost;
        location /nginx_status {
                stub_status on;
                access_log   off;
                allow 127.0.0.1;
                deny all;
        }
    } 

    server {
        listen       80;
        server_name  munin.bizforce.cn;
        return 301 https://munin.bizforce.cn$request_uri;
    }

    server {
        listen       443;
        server_name  munin.bizforce.cn;

        access_log   /var/log/nginx/bizforce-monitor/munin.access.log main;

        ssl                  on;
        ssl_certificate      ssl/asterisk.bizforce.cn.crt;
        ssl_certificate_key  ssl/asterisk.bizforce.cn.key;

        ssl_protocols  SSLv3 TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers  HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers   on;

        proxy_read_timeout         1

    	location ^~ /munin-cgi/munin-cgi-graph/ {
            auth_basic             	"Access to the web interface is restricted";
            auth_basic_user_file   	/etc/munin/htpasswd.users;
		    rewrite ^/munin-cgi/munin-cgi-graph(.*) /munin-cgi-graph$1;

		    access_log off;
		    root			/var/www/cgi-bin;
		    fastcgi_pass 		127.0.0.1:9993;
    	}	

        location / {
            auth_basic             "Access to the web interface is restricted";
            auth_basic_user_file   /etc/munin/htpasswd.users;

            root   /var/www/html/munin;
            index  index.html index.htm;
        }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    } 

    server {
        listen       80;
        server_name  nagios.bizforce.cn;
	    return 301 https://nagios.bizforce.cn$request_uri;
    } 
 
    server {
        listen       443;
        server_name  nagios.bizforce.cn;
        
        access_log   /var/log/nginx/bizforce-monitor/nagios.access.log main;

        ssl                  on;
        ssl_certificate      ssl/asterisk.bizforce.cn.crt;
        ssl_certificate_key  ssl/asterisk.bizforce.cn.key;

        ssl_protocols  SSLv3 TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers  HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers   on;
               
        proxy_read_timeout         100;

        location ~ .*\.cgi$ {
            auth_basic            "Restricted";
            auth_basic_user_file  /usr/local/nagios/etc/htpasswd.users;
            rewrite ^/nagios/cgi-bin/(.*)\.cgi /$1.cgi;

            root                  /usr/local/nagios/sbin;
            #include              fastcgi.conf;

            include               fastcgi_params;
            fastcgi_param         AUTH_USER $remote_user;
            fastcgi_param         REMOTE_USER $remote_user;
            fastcgi_pass          127.0.0.1:9992;
        }

        location / {
            auth_basic             "Access to the web interface is restricted";
            auth_basic_user_file   /usr/local/nagios/etc/htpasswd.users;

            rewrite ^/nagios/(.*) /$1 break;

            root               /usr/local/nagios/share;
            index              index.php;
            #include           fastcgi.conf;
            include            fastcgi_params;
            fastcgi_param      SCRIPT_FILENAME  $document_root$fastcgi_script_name;

            if ($uri ~ "\.php"){
                fastcgi_pass       127.0.0.1:9991;
            }
        }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }




.. author:: default
.. categories:: none
.. tags:: none
.. comments::
