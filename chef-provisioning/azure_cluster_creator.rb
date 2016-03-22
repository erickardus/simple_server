# A script that will provision a server or cluster of servers and configure them according to Chef policies.
require 'optparse'
require 'erb'

# Default options stored here.
options = {
  :name => "server",
  :number => 1,
  :chef_url => "https://manage.chef.io/organizations/pvtool",
  :roles => [],
  :runlist => [],
  :cloud_service_name => 'erickardus1xx',
  :storage_account_name => 'erickardus1xx',
  :vm_size => "Standard_D1",
  :location => "West US",
  :tcp_endpoints => '80:80',
  :image_id => 'b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04_2-LTS-amd64-server-20150706-en-us-30GB',
  :password => "chefm3t4l\\m/",
}


# Parse command-line arguments
OptionParser.new do |opt|
  opt.banner = "Usage myparse.rb [options]"
  opt.on('-l', '--location LOCATION') { |o| options[:location] = o if o != ""}
  opt.on('-n', '--name NAME') { |o| options[:name] = o if o != ""}
  opt.on('-N', '--number NUMBER') { |o| options[:number] = o if o != ""}
  opt.on('-p', '--password PASSWORD') { |o| options[:password] = o if o != ""}
  opt.on('-i', '--image_id IMAGE-ID') { |o| options[:image_id] = o if o != ""}
  opt.on('-s', '--vm_size SIZE') { |o| options[:vm_size] = o if o != ""}
  opt.on('-c', '--chef_url CHEF-URL') { |o| options[:chef_url] = o if o != ""}
  opt.on("--roles role1,role2,role3", Array, "List of roles") { |o| options[:roles] = o if o != ""}
  opt.on("--runlist recipe1,recipe2,recipe3", Array, "List of recipes") { |o| options[:runlist] = o if o != ""}
  opt.on("--cloud_service_name SERVICENAME") { |o| options[:cloud_service_name] = o if o != ""}
  opt.on("--storage_account_name ACCOUNTNAME") { |o| options[:storage_account_name] = o if o != ""}
  opt.on("--tcp_endpoints ENDPOINTS") { |o| options[:tcp_endpoints] = o if o != ""}
end.parse!


class BindMe


  def initialize(options)
    @location = options[:location]
    @name = options[:name]
    @number = options[:number]
    @password = options[:password]
    @image_id = options[:image_id]
    @vm_size = options[:vm_size]
    @chef_url = options[:chef_url]
    @roles = options[:roles]
    @runlist = options[:runlist]
    @cloud_service_name = options[:cloud_service_name]
    @storage_account_name = options[:storage_account_name]
    @tcp_endpoints = options[:tcp_endpoints]
    @template = File.read('./azure_cluster_template.erb')
  end

  def render
    ERB.new(@template).result(binding)
  end

end



x = BindMe.new(options)
res = x.render
result = File.open("./azure_cluster_provisioning.rb", "w+")
result << res
result.close

# Delete log
# File.delete("../templates/azure_log_interactive.txt ")

# Executes the recently created Chef provisioning script and actually provision infrastructure.
# exec('chef-client -z azure_cluster_provisioning.rb')
pid = Process.spawn('chef-client','-z', 'azure_cluster_provisioning.rb', :out => '../templates/azure_log_interactive.txt')
Process.detach(pid)

# Launch websocketd
pid = Process.spawn('../websocketd', '--address=127.0.0.1', '--port=8082', 'tail', '-f', '../templates/azure_log_interactive.txt')
Process.wait(pid)
exit

