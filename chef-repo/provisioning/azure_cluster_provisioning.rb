require 'chef/provisioning'
require 'chef/provisioning/azure_driver'

with_driver 'azure'

machine_options = {
  :bootstrap_options => {
    :cloud_service_name => 'caritasx',
    :storage_account_name => 'caritasx',
    :vm_size => "Standard_D1",
    :location => "West US",
    :tcp_endpoints => '80:80',
  },
  :image_id => 'b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04_2-LTS-amd64-server-20150706-en-us-30GB',
  :password => "chefm3t4l\\m/",
}

with_chef_server "https://manage.chef.io/organizations/simple_server",
  :client_name => Chef::Config[:node_name],
  :signing_key_filename => Chef::Config[:client_key]

                                           
machine_batch "cluster" do                   
    1.upto(1) do |i|            
        machine "mahalo#{i}" do
            machine_options machine_options
                                    
                     
                role 'webserver'           
                                    
        end                                  
    end                                      
end                                          
