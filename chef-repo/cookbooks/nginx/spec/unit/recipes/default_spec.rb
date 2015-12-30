#
# Cookbook Name:: nginx
# Spec:: default
#
# Copyright (c) 2015 The Authors, All Rights Reserved.

require 'chefspec'
at_exit  {  ChefSpec::Coverage.report!  }
describe 'nginx::default' do
  let(:chef_run) {ChefSpec::ServerRunner.new.converge('nginx::default') }
   before do
#      stub_command("test -f /usr/local/nginx/sbin/nginx").and_return(true)
# Update the nginx version to test
       stub_command("/usr/local/nginx/sbin/nginx -v | grep -q 1.8.0").and_return(true)
   end
   # Packages for CentOS & Amazon
    it '... installs zlib-devel' do
      expect(chef_run).to install_package('zlib-devel')
    end   
    it '... installs pcre-devel' do
      expect(chef_run).to install_package('pcre-devel')
    end   
    it '... installs gcc' do
      expect(chef_run).to install_package('gcc')
    end   
# Packages for Ubuntu
#        it '... installs libpcre3-dev' do
#      expect(chef_run).to install_package('libpcre3-dev')
#    end   
#    it '... installs build-essential' do
#      expect(chef_run).to install_package('build-essential')
#    end   
#    it '... installs libssl-dev' do
#      expect(chef_run).to install_package('libssl-dev')
#    end   
    it 'start nginx service' do
        expect(chef_run).to start_service('nginx')
    end
    it 'server a web page that says "CHEF' do
        expect(chef_run).to render_file('/data_test/www/index.html').with_content(/CHEF.+/)
    end
    it 'server a web page that says "PROXY"' do
        expect(chef_run).to render_file('/data_test/proxy/index.html').with_content(/PROXY.+/)
    end
    it 'installs nginx' do
          expect(chef_run).to create_template('/etc/init.d/nginx')
#          expect(chef_run).to enable_service('nginx')
          expect(chef_run).to create_template('nginx.conf')
#          expect(chef_run).to create_directory('/etc/nginx')
    end
end