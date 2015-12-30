#
# Cookbook Name:: mysql
# Recipe:: default
#
# Copyright (c) 2015 The Authors, All Rights Reserved.
 package 'mysql-server' do
  action :install
 end

 service 'mysqld' do
  action [:start, :enable]
 end
