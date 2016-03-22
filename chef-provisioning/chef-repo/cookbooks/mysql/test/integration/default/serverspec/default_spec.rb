require 'spec_helper'

describe 'mysql server' do

  it 'package installation' do
    expect(package('mysql-server')).to be_installed
  end

  it 'service is enabled' do
    expect(service('mysqld')).to be_enabled
  end

  it 'service is running' do
    expect(service('mysqld')).to be_running
  end


  it 'added root password' do
    expect(command("mysql -u root -pmypass -e 'show databases;'").stdout).to match /mysql/
  end

  it 'added /tmp/mydb.sql file' do
    expect(file('/tmp/mydb.sql')).to be_file
  end

  it 'populated DB' do
    expect(command("mysql -u root -pmypass -e 'show databases;'").stdout).to match /mydb/
  end  

end
