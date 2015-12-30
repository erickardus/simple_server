#
# Cookbook Name:: haproxy

default['haproxy']['source']['version'] = '1.5.14'
default['haproxy']['source']['url'] = 'http://www.haproxy.org/download/'
default['haproxy']['source']['target_os'] = 'generic'
default['haproxy']['source']['target_cpu'] = ''
default['haproxy']['source']['target_arch'] = ''
default['haproxy']['source']['use_pcre'] = false
default['haproxy']['source']['use_openssl'] = false
default['haproxy']['source']['use_zlib'] = false

default['haproxy']['conf_dir'] = '/etc/haproxy'
default['haproxy']['conf_file'] = 'haproxy.cfg'

default['haproxy']['conf_cookbook'] = "haproxy"
default['haproxy']['conf_template_source'] = "haproxy.cfg.erb"
default['haproxy']['user'] = "haproxy"
default['haproxy']['group'] = "haproxy"

default['haproxy']['enable_default_http'] = true
default['haproxy']['mode'] = "http"
default['haproxy']['incoming_address'] = "0.0.0.0"
default['haproxy']['incoming_port'] = 80

default['haproxy']['member_port'] = 8080
default['haproxy']['member_weight'] = 1
default['haproxy']['app_server_role'] = "webserver"
default['haproxy']['defaults_retries'] = 3
default['haproxy']['balance_algorithm'] = "roundrobin"
default['haproxy']['enable_ssl'] = false
default['haproxy']['ssl_incoming_address'] = "0.0.0.0"
default['haproxy']['ssl_incoming_port'] = 443
default['haproxy']['ssl_member_port'] = 8443
default['haproxy']['httpchk'] = nil
default['haproxy']['ssl_httpchk'] = nil
default['haproxy']['enable_admin'] = true
default['haproxy']['admin']['address_bind'] = "127.0.0.1"
default['haproxy']['admin']['port'] = 22002
default['haproxy']['admin']['options'] = { 'stats' => 'uri /' }
default['haproxy']['enable_stats_socket'] = false
default['haproxy']['stats_socket_path'] = "/var/run/haproxy.sock"
default['haproxy']['stats_socket_user'] = node['haproxy']['user']
default['haproxy']['stats_socket_group'] = node['haproxy']['group']
default['haproxy']['pid_file'] = "/var/run/haproxy.pid"

default['haproxy']['defaults_options'] = ["httplog", "dontlognull", "redispatch"]
default['haproxy']['x_forwarded_for'] = false
default['haproxy']['global_options'] = {}
default['haproxy']['defaults_timeouts']['connect'] = "5s"
default['haproxy']['defaults_timeouts']['client'] = "50s"
default['haproxy']['defaults_timeouts']['server'] = "50s"
default['haproxy']['cookie'] = nil

default['haproxy']['global_max_connections'] = 4096
default['haproxy']['member_max_connections'] = 100
default['haproxy']['frontend_max_connections'] = 2000
default['haproxy']['frontend_ssl_max_connections'] = 2000

#default['haproxy']['install_method'] = 'package'


default['haproxy']['pool_members'] = {}

node.default['haproxy']['listeners'] = {
  'listen' => {},
  'frontend' => {
    "http-in" => ['bind *:80', 'stats enable', 'default_backend servers']
   },
  'backend' => {
    "servers" => [
       'server server1 127.0.0.1:8000 maxconn 100 weight 1 check',
       'server server2 127.0.0.1:8001 maxconn 100 weight 1 check',
       'server server3 127.0.0.1:8002 maxconn 100 weight 1 check',
    ]
   }
}



#default['haproxy']['listeners'] = {
  #'listen' => {},
  #'frontend' => {},
  #'backend' => {}
##}
