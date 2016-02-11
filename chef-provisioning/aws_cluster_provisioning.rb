require 'chef/provisioning'
require 'chef/provisioning/aws_driver'

with_driver "aws::us-east-1"



    with_chef_server "https://manage.chef.io/organizations/simple_server",
      :client_name => Chef::Config[:node_name],
      :signing_key_filename => Chef::Config[:client_key]


    machine_batch "cluster" do
        1.upto(1) do |i|
            machine "myserverx#{i}" do

                machine_options(
                    lazy do
                    {
                        ssh_username: "ec2-user",
                        bootstrap_options: {
                            image_id: "ami-0d4cfd66",
                            instance_type: "t2.micro",
                            subnet_id: 'subnet-58853a2e',
                            security_group_ids: ['sg-76a4b60f']
                        },
                    }
                    end
                )

                
 
                
                    role 'webserver'
                

            end
        end
    end    

