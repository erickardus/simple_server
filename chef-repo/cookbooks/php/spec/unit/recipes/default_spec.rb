#
# Cookbook Name:: php
# Spec:: default
#
# Copyright (c) 2015 The Authors, All Rights Reserved.

require 'chefspec'

at_exit { ChefSpec::Coverage.report! }

describe 'php::default' do
    let(:chef_run) { ChefSpec::ServerRunner.new.converge('php::default') }

    it 'installs httpd' do
      expect(chef_run).to install_package('httpd')
    end

    it 'installs php' do
      expect(chef_run).to install_package('php')
    end

    it 'Creates file from template phpinfo.conf' do
      expect(chef_run).to create_template('/etc/httpd/conf.d/phpinfo.conf')
    end

    it 'Creates directry for index.php' do
      expect(chef_run).to create_directory('/usr/share/phpinfo')
    end

    it 'Creates file from file index.php' do
      expect(chef_run).to create_cookbook_file('/usr/share/phpinfo/index.php')
    end

end
