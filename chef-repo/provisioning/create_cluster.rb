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
  :chef_url => "https://manage.chef.io/organizations/simple_server"
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
end.parse!


class BindMe


  def initialize(options)
    @region = options[:region]
    @name = options[:name]
    @number = options[:number]
    @ssh_username = options[:ssh_username]
    @ami = options[:ami]
    @instance_type = options[:instance_type]
    @chef_url = options[:chef_url]
    @template = File.read('./create_node.erb')
  end

  def render
    ERB.new(@template).result(binding)
  end

end



x = BindMe.new(options)
res = x.render
result = File.open("./creator_script.rb", "w+")
result << res
result.close

exec('chef-client -z creator_script.rb')