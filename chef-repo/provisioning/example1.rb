require 'chef/provisioning'
require 'chef/provisioning/aws_driver'

with_driver 'aws::us-east-1'

with_machine_options({
  ssh_username: "ec2-user",
  bootstrap_options: {
    image_id: "ami-60b6c60a",
    instance_type: "t2.micro",
  },
})

machine 'erick' do
  recipe 'apache'
end
