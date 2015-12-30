#
# Cookbook Name:: nginx
# Recipe:: default
#
# Copyright (c) 2015 The Authors, All Rights Reserved.

# Define nginx version and url for download

version = node['nginx']['version']
url     = node['nginx']['url']

# Define nginx directory and version and url for download

user    = node['nginx']['user']
dir     = node['nginx']['dir']
www     = node['nginx']['data_test']
image   = node['nginx']['data_images']
proxy   = node['nginx']['data_proxy']

# Needed libraries to compile nginx for CentOS and Amazon

package 'zlib-devel' do
  action :install
  only_if { platform? ('centos') or ('amazon')}
end

package 'pcre-devel' do
  action :install
  only_if { platform? ('centos') or ('amazon')}
end

package 'gcc' do
  action :install
  only_if { platform? ('centos') or ('amazon')}
end

# Needed libraries to compile nginx for Ubuntu

package 'libpcre3-dev' do
  action :install
  only_if { platform? ('ubuntu') }
end

package 'build-essential' do
  action :install
  only_if { platform? ('ubuntu') }
end

package 'libssl-dev' do
  action :install
    only_if { platform? ('ubuntu') }
end

#package ['zlib-devel', 'pcre-devel', 'gcc'] do
#  action :install
#  only_if { platform? ('centos') or ('amazon')}
#end

# Needed libraries to compile nginx for Ubuntu

#package ['libpcre3-dev', 'build-essential', 'libssl-dev'] do
#  action :install
#  only_if { platform? ('ubuntu') }
#end

# create directory for downloading nginx

directory 'nginx_config_dir1' do
 path "#{dir}"
 action :create
 owner 'root'
 user  'root'
 mode  '0755'
end 

# download nginx for Ubuntu including PGP signature 

bash "install_nginx_ubuntu" do
  user 'root'
 code <<-EOC
    mkdir #{dir}
    cd #{dir}
    wget #{url}nginx-#{version}.tar.gz.asc
    wget #{url}nginx-#{version}.tar.gz
    gpg #{url}nginx-#{version}.tar.gz.asc
    gpg #{url}nginx-#{version}.tar.gz.asc
    tar xzf nginx-#{version}.tar.gz &&
    cd nginx-#{version} &&
    ./configure && make && make install
  EOC
#    not_if "test -f /usr/local/nginx/sbin/nginx"
#    not_if "/usr/local/nginx/sbin/nginx -v | grep -q #{node['nginx']['version']}"
    only_if { platform?('ubuntu') }
end

# download nginx for Centos and Amazon 

bash "install_nginx" do
  user 'root'
  code <<-EOC
#    mkdir #{dir}
    mkdir -p #{www}
    mkdir -p #{image}
    mkdir -p #{proxy}
    cd #{dir}
    wget #{url}nginx-#{version}.tar.gz
    tar xzf nginx-#{version}.tar.gz &&
    cd nginx-#{version} &&
    ./configure && make && make install
  EOC
#    not_if "test -f /usr/local/nginx/sbin/nginx"
    not_if "/usr/local/nginx/sbin/nginx -v | grep -q #{node['nginx']['version']}"
end

# create directory for downloading nginx based on version

directory 'nginx_config_dir2' do
 path "#{dir}nginx-#{version}"
 action :create
 owner 'root'
 user  'root'
 mode  '0755'
end 

# template for nginx configuration file 

template "nginx.conf" do
  path "#{dir}nginx-#{version}/conf/nginx.conf"
  source 'nginx.conf.erb'
  owner 'root'
  group 'root'
  mode '0755'
end

# template for creating init file to start/stop nginx 

template 'init_script' do
   case node[:platform]
   when 'centos', 'amazon'
      source 'nginx.init.erb'
   when 'ubuntu'
      source 'nginx.init_ubuntu.erb'
   end
   path '/etc/init.d/nginx'
   owner 'root'
   group 'root'
   mode '0755'
   action :create
end

#template "/etc/init.d/nginx" do
#  source 'nginx.init.erb'
#  owner 'root'
#  group 'root'
#  mode '0755'
#end

# resource service to start and enable nginx

#service 'nginx' do
#  action [ :start, :enable ]
#end

service 'nginx' do
  supports :status => true, :restart => true, :reload => true
  action   :start
end

# template for serving static content

template "#{www}index.html" do
  source 'nginx.conf.static.erb'
  owner 'root'
  group 'root'
  mode '0755'
end

# template for serving simple proxy server

template "#{proxy}index.html" do
  source 'nginx.conf.proxy.erb'
  owner 'root'
  group 'root'
  mode '0755'
end