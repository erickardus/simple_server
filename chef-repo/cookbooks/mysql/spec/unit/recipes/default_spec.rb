#
# Cookbook Name:: mysql
# Spec:: default
#
# Copyright (c) 2015 The Authors, All Rights Reserved.

require 'chefspec'

at_exit  {  ChefSpec::Coverage.report!  }

describe 'mysql::default' do
  let(:chef_run)  {  ChefSpec::ServerRunner.new.converge('mysql::default')  }
  
  it 'installs mysql-server' do
    expect(chef_run).to install_package('mysql-server')
#	expect(chef_run).to create_template('/var/www/html/index.html')
#	expect(chef_run).to enable_service('mysqld')
#  end
#it 'installs mysql-server' do
     expect(chef_run).to enable_service('mysqld')
  end
end
