#
# Cookbook Name:: mysql
# Recipe:: default
#
# Copyright (c) 2016 The Authors, All Rights Reserved.
#

package 'mysql-server' do
  action :install
end

service 'mysqld' do
  action [ :enable, :start ]
end

root_password = node['mysql']['root']['password']

bash 'change_root_passwd' do
  code <<-EOH
    mysqladmin -u root password "#{root_password}"
    touch /tmp/addedpasswd
    EOH
  not_if { ::File.exists?('/tmp/addedpasswd') }
end

cookbook_file '/tmp/mydb.sql' do
  source 'mydb.sql'
end

bash 'execute_sql_script' do
  code <<-EOH
    mysql -u root -p"#{root_password}" < '/tmp/mydb.sql'
    touch /tmp/executedsql
  EOH
  not_if { ::File.exists?('/tmp/executedsql') }
end
