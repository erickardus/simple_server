require 'chef/provisioning'
require 'chef/provisioning/azure_driver'

with_driver 'azure'

with_chef_server "https://manage.chef.io/organizations/simple_server",
  :client_name => Chef::Config[:node_name],
  :signing_key_filename => Chef::Config[:client_key]

                                           
machine_batch "cluster" do                   
    1.upto(2) do |i|
        machine_options = {
          :bootstrap_options => {
            :cloud_service_name => "praticazure#{i}",
            :storage_account_name => "praticazure#{i}",
            :vm_size => "Basic_A0",
            :location => "Central US",
            :tcp_endpoints => '80:80',
          },
          :image_id => '0b11de9248dd4d87b18621318e037d37__RightImage-CentOS-6.5-x64-v14.1',
          :password => "chefm3t4l\\m/",
        }            
        machine "praticazure#{i}" do
            machine_options machine_options
            chef_environment 'dev'
                                    
                     
            role 'webserver'           
                                    
        end                                  
    end                                      
end                                          
