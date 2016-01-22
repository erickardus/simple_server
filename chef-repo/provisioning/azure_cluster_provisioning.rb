require 'chef/provisioning'
require 'chef/provisioning/azure_driver'

with_driver 'azure'

with_chef_server "https://manage.chef.io/organizations/simple_server",
  :client_name => Chef::Config[:node_name],
  :signing_key_filename => Chef::Config[:client_key]

                                           
machine_batch "cluster" do                   
    1.upto(1) do |i|
        machine_options = {
          :bootstrap_options => {
            :cloud_service_name => "hello#{i}",
            :storage_account_name => "hello#{i}",
            :vm_size => "Basic_A0",
            :location => "East US",
            :tcp_endpoints => '80:80',
          },
          :image_id => 'b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04_2-LTS-amd64-server-20150706-en-us-30GB',
          :password => "chefm3t4l\\m/",
        }            
        machine "hello#{i}" do
            machine_options machine_options
            chef_environment 'dev'
                                    
                     
            role 'webserver'           
                                    
        end                                  
    end                                      
end                                          
