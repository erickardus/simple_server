#
# Cookbook Name:: mysql
# Spec:: default
#
# Copyright (c) 2016 The Authors, All Rights Reserved.

require 'spec_helper'

describe 'mysql::default' do

    let(:chef_run) { ChefSpec::ServerRunner.new.converge('mysql::default') }

    it 'installs mysql-server' do
      expect(chef_run).to install_package('mysql-server')
    end

    it 'enables mysqld' do
      expect(chef_run).to enable_service('mysqld')
    end

    it 'starts mysqld' do
      expect(chef_run).to start_service('mysqld')
    end

    it 'added root password' do
      expect(chef_run).to run_bash("change_root_passwd")
    end

    it 'created_mydb_sql_file' do
      expect(chef_run).to create_cookbook_file('/tmp/mydb.sql')
    end

    it 'executed sql script' do
      expect(chef_run).to run_bash("execute_sql_script")
    end

end
