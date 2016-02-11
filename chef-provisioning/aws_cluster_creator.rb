# A script that will provision a server or cluster of servers and configure them according to Chef policies.
require 'optparse'
require 'erb'

# Default options stored here.
options = {
  :region => "us-east-1",
  :name => "server",
  :number => 1,
  :ssh_username => "ec2-user",
  :ami => "ami-60b6c60a",
  :instance_type => "t2.micro",
  :chef_url => "https://manage.chef.io/organizations/simple_server",
  :roles => [],
  :runlist => []
}


# Parse command-line arguments
OptionParser.new do |opt|
  opt.banner = "Usage myparse.rb [options]"
  opt.on('-r', '--region REGION') { |o| options[:region] = o if o != ""}
  opt.on('-n', '--name NAME') { |o| options[:name] = o if o != ""}
  opt.on('-N', '--number NUMBER') { |o| options[:number] = o if o != ""}
  opt.on('-u', '--user USER') { |o| options[:ssh_username] = o if o != ""}
  opt.on('-a', '--ami AMI-ID') { |o| options[:ami] = o if o != ""}
  opt.on('-t', '--type INSTANCE-TYPE') { |o| options[:instance_type] = o if o != ""}
  opt.on('-c', '--chef_url CHEF-URL') { |o| options[:chef_url] = o if o != ""}
  opt.on('-V', '--vpc [VPC]') do |vpc|
    options[:vpc] = vpc;
  end
  opt.on('-S', '--subnet_id [SUBNET]') do |subnet|
    options[:subnet] = subnet;
  end
  opt.on('-s', '--securitygroup_id [SG]') do |sg|
    options[:securitygroup] = sg;
  end
  opt.on('--vpcselection SELECTION') do |sel|
    options[:vpcselection] = sel;
  end
  opt.on("--roles role1,role2,role3", Array, "List of roles") { |o| options[:roles] = o if o != ""}
  opt.on("--runlist recipe1,recipe2,recipe3", Array, "List of recipes") { |o| options[:runlist] = o if o != ""}
end.parse!


# Defines a class to pass parameters to ERB and render it.
class BindMe


  def initialize(options)
    @region = options[:region]
    @name = options[:name]
    @number = options[:number]
    @ssh_username = options[:ssh_username]
    @ami = options[:ami]
    @instance_type = options[:instance_type]
    @chef_url = options[:chef_url]
    @roles = options[:roles]
    @runlist = options[:runlist]
    @vpc = options[:vpc]
    @subnet = options[:subnet]
    @securitygroup = options[:securitygroup]
    @vpcselection = options[:vpcselection]
    @template = File.read('./aws_cluster_template.erb')
  end

  def render
    ERB.new(@template).result(binding)
  end

end


# Creates Chef provisioning script out of a template
x = BindMe.new(options)
res = x.render
result = File.open("./aws_cluster_provisioning.rb", "w+")
result << res
result.close

# Executes the recently created Chef provisioning script and actually provision infrastructure.
exec('chef-client -z aws_cluster_provisioning.rb')