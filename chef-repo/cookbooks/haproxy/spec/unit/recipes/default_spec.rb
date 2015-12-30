#
# Cookbook Name:: haproxy
# Spec:: default
#
# Copyright (c) 2015 The Authors, All Rights Reserved.

require 'chefspec'

at_exit { ChefSpec::Coverage.report! }

describe 'haproxy::default' do
    let(:chef_run) { ChefSpec::ServerRunner.new.converge('haproxy::default') }
#    let(:chef_run) { ChefSpec::ServerRunner.new(platform: 'centos').converge('haproxy::default') }

    before do
       stub_command("/usr/local/sbin/haproxy -v | grep -q 1.5.14").and_return(true)
    end


    it '... installs gcc' do
      expect(chef_run).to install_package('gcc')
    end

    it '... installs make' do
      expect(chef_run).to install_package('make')
    end

    it '... executes bash resource to install haproxy from source package' do
      expect(chef_run).to run_bash('install_haproxy')
    end

    it '... creates haproxy user with uid = 188' do
      expect(chef_run).to create_user('haproxy').with_uid(188)
    end

    it '... verifies haproxy group modified to gid = 188' do
      expect(chef_run).to modify_group('haproxy').with_gid(188)
    end

    it '... configuration directory is created' do
      expect(chef_run).to create_directory('config_dir').with_gid(188)
    end

    it '... creates configuration file from template' do
      expect(chef_run).to create_template('config_file').with_gid(188)
    end

    it '... creates haproxy init script file from template' do
      expect(chef_run).to create_template('init_script').with_gid(188)
    end

    it '... creates /etc/default/haproxy file from cookbook file' do
      expect(chef_run).to create_cookbook_file('etc_default_file')
    end

end
