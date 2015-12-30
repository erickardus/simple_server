require 'serverspec'

set :backend, :exec

describe 'php Verification' do

  it 'php Package is installed' do
     expect(package 'php').to be_installed
  end

  it 'httpd Package is installed' do
     expect(package 'httpd').to be_installed
  end

  it 'Responds on phpinfo call' do
     expect(command('curl localhost:80/phpinfo/index.php').stdout).to match /PHP Version/
  end
end
