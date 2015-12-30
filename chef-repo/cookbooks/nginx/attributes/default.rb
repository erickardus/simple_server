#
# Cookbook Name:: nginx
# Recipe:: default
#
# Copyright (c) 2015 The Authors, All Rights Reserved.

# Define nginx version and url for download

default['nginx']['version'] = '1.8.0'
default['nginx']['url']     = 'http://www.nginx.org/download/'
default['nginx']['user']    = 'root'
default['nginx']['dir']     = '/etc/nginx/'

default['nginx']['data_test']   = '/data_test/www/'
default['nginx']['data_images'] = '/data_test/images/'
default['nginx']['data_proxy']  = '/data_test/proxy/'