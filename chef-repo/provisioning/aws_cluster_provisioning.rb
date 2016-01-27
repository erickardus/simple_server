require 'chef/provisioning'
require 'chef/provisioning/aws_driver'

with_driver "aws::us-west-1"

my_vpc = aws_vpc 'myapp-vpcx' do
    cidr_block '10.0.0.0/16'
    main_routes '0.0.0.0/0' => :internet_gateway
    internet_gateway true
end

my_sg = aws_security_group 'myapp-sgx' do
    vpc lazy { my_vpc.aws_object_id }
    inbound_rules '0.0.0.0/0' => [ 22, 80, 3306 ]
end

my_subnet = aws_subnet 'myapp-public1x' do
    vpc lazy { my_vpc.aws_object_id}
    cidr_block '10.0.1.0/24'
    availability_zone 'us-west-1a'
    map_public_ip_on_launch true
end

with_chef_server "https://manage.chef.io/organizations/simple_server",
  :client_name => Chef::Config[:node_name],
  :signing_key_filename => Chef::Config[:client_key]


machine_batch "cluster" do
    1.upto(1) do |i|
        machine "west#{i}" do

            machine_options(
                lazy do
                {
                    ssh_username: "ec2-user",
                    bootstrap_options: {
                        image_id: "ami-2708f363",
                        instance_type: "t2.micro",
                        subnet_id: my_subnet.aws_object_id,
                        security_group_ids: [my_sg.aws_object_id]
                    },
                }
                end
            )

            

            

        end
    end
end

