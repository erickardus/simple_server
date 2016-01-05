#
# Cookbook Name:: apache
# Recipe:: default
#
# Copyright (c) 2015 The Authors, All Rights Reserved.



case node[:platform]
  when 'debian', 'ubuntu'
    include_recipe 'apt'
end
  

package 'Install Apache' do
  case node[:platform]
    when 'redhat', 'centos', 'amazon'
      package_name 'httpd'
    when 'ubuntu', 'debian'
      package_name 'apache2'
  end
end


service 'apache' do
  case node[:platform]
    when 'redhat', 'centos', 'amazon'
      service_name 'httpd'
    when 'ubuntu', 'debian'
      service_name 'apache2'
  end
  action [ :enable, :start ]
end
