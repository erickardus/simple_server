#
# Cookbook Name:: haproxy
# Recipe:: default
#
# Copyright (c) 2015 The Authors, All Rights Reserved.


#node.default['haproxy']['source']['version'] = '1.5.13' 
#node.default['haproxy']['global_max_connections'] = 2048 

#node.default['haproxy']['listeners'] = {
#  'frontend' => {
#    "http-in" => ['bind *:80', 'stats enable', 'default_backend servers']
#   },
#  'backend' => {
#    "servers" => [
#       'server server1 10.8.0.1:8000 maxconn 100 weight 1 check',
#       'server server2 10.8.0.2:8000 maxconn 100 weight 1 check',
#       'server server3 10.8.0.3:8000 maxconn 100 weight 1 check'   
#    ]
#   }
#}




# Installs gcc & make packages to compile haproxy source code 
package 'gcc'
package 'make'


#--------------------
# resource: bash install_haproxy
#  Download source code from node['haproxy']['source']['url'], compiles and install the haproxy version as node['haproxy']['source']['version'] 
#--------------------

bash "install_haproxy" do                            
  user 'root'                                                    
  cwd '/tmp'                                                     
  code <<-EOC                                                    
    ( 
      wget #{node['haproxy']['source']['url']}/#{node['haproxy']['source']['version'][0..2]}/src/haproxy-#{node['haproxy']['source']['version']}.tar.gz
      tar xzf haproxy-#{node['haproxy']['source']['version']}.tar.gz &&
      cd haproxy-#{node['haproxy']['source']['version']} &&
      make TARGET=generic  &&
      make install && rm -rf /tmp/haproxy-#{node['haproxy']['source']['version']}*
    ) &> /tmp/haproxy-install.log
  EOC
  #not_if "test -f /usr/local/sbin/haproxy"                   
  not_if "/usr/local/sbin/haproxy -v | grep -q #{node['haproxy']['source']['version']}"
end                                                              



#--------------------
# resource:  user "haproxy"
#   Creates the user haproxy with group = haproxy, UID = 188
#--------------------

user 'haproxy' do
   uid 188
   action :create
end


#--------------------
# resource:  group "haproxy"
#   Creates the group haproxy with GID = 188
#--------------------

group 'haproxy' do
   gid 188
   action :modify
end



#--------------------
# resource:  template 'init_script'
#   Creates the init file /etc/init.d/haproxy  to start/stop haproxy service when server is rebooted
#--------------------

template 'init_script' do
   case node[:platform]
   when 'redhat', 'centos', 'amazon'
      source 'haproxy-init.erb'
   when 'ubuntu'
      source 'haproxy-init-ubuntu.erb'
   end
   path '/etc/init.d/haproxy'
   owner 'root'
   group 'root'
   mode '0755'
   action :create
end


#--------------------
# resource:  cookbook_file '/etc/default/haproxy' 
#   Installs the default file to enable/disable haproxy in ubuntu OS
#--------------------

cookbook_file '/etc/default/haproxy' do
   source 'haproxy'
   owner 'root'
   group 'root'
   mode '0755'
   only_if { platform?('ubuntu') }
end


#--------------------
# resource:  directory  <Configuration directory path>
#   Creates the directory where configuration file will live
#--------------------

directory "#{node['haproxy']['conf_dir']}" do
   action :create
   owner 'root'
   user 'root'
   mode '0755' 
end


#--------------------
# resource:  template "<Configuration file path>"
#   Creates the configuration file based on the given parameters in attributes
#--------------------

template "#{node['haproxy']['conf_dir']}/#{node['haproxy']['conf_file']}" do
   source 'haproxy.cfg.erb'
   owner 'root'
   group 'root'
   mode '0755'
   action :create
end


#--------------------
# resource:  service 'haproxy'
#   Enables the haproxy service on the system
#--------------------

service 'haproxy' do
  supports :start => true, :stop => true, :restart => true, :status => true, :reload => true
  action [ :enable, :start ]
  subscribes :restart, 'template[config_file]', :delayed
end
