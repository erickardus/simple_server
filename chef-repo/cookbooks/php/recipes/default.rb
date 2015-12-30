#
# Cookbook Name:: php
# Recipe:: default
#
# Copyright (c) 2015 The Authors, All Rights Reserved.

#  Installs php and httpd packages
package 'php'
package 'php-mysql'
package 'httpd'

service 'php' do
  action :nothing
end

service 'php-mysql' do
  action :nothing
end

# Ensure httpd is running and enabled
service 'httpd' do
  action [ :start, :enable ]
end

# Creaters folder to allocate php's index.php file 
directory node['phpinfo_location'] do
  owner 'root'
  group 'root'
  mode '0755'
  action :create
end

#  Creates index.php to show phpinfo() function 
cookbook_file "#{node.phpinfo_location}/index.php" do
  source 'index.php'
  owner 'root'
  group 'root'
  mode '0755'
  action :create
end

# Changes to /etc/php.ini file 
execute 'memory_limit' do
  command "sed -i 's/memory_limit =.*/memory_limit = 128M/g' /etc/php.ini" 
end

execute 'max_execution_time' do
  command "sed -i 's/max_execution_time =.*/max_execution_time = 120/g' /etc/php.ini" 
end

execute 'max_upload_size' do
  command "sed -i 's/upload_max_filesize =.*/upload_max_filesize = 50M/g' /etc/php.ini " 
end

# Enables phpinfo page in httpd service
template '/etc/httpd/conf.d/phpinfo.conf' do
  source 'phpinfo.conf.erb'
  owner 'root'
  group 'root'
  mode '0755'
  action :create
  notifies :restart, 'service[httpd]', :immediately
end
