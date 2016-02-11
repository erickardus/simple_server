# See http://docs.chef.io/config_rb_knife.html for more information on knife configuration options

current_dir = File.dirname(__FILE__)
log_level                :info
log_location             STDOUT
node_name                "erickardus"
client_key               "#{current_dir}/erickardus.pem"
validation_client_name   "simple_server-validator"
validation_key           "#{current_dir}/simple_server-validator.pem"
chef_server_url          "https://api.chef.io/organizations/simple_server"
cookbook_path            ["#{current_dir}/../cookbooks"]
