require 'spec_helper'

describe 'mysql' do
   it 'installs mysql-server' do
     expect(package 'mysql-server').to be_installed
   end
end
