Simple Server Provisioning
==========================
This is a server provisioning tool, it's purpose is to help you provision servers, clusters and entire application infrastructure with minimal knowledge of the cloud. It's meant to work with the most popular Cloud providers

Cloud providers:
> AWS
> Azure

Prerequisites
-------------

### Chef

Inside the "chef-provisioning" folder, create a .chef folder, this folder needs to contain the necessary files in order for you to connect to your Chef Server:

> knife.rb
> <validator>.pem
> <user>.pem

### AWS

ENV["AWS_ACCESS_KEY_ID"]
ENV["AWS_SECRET_ACCESS_KEY"]
ENV["AWS_DEFAULT_REGION"]
ENV["AWS_DEFAULT_OUTPUT"]

Example:

set AWS_ACCESS_KEY_ID=AAAABBBBCCCCDDDDEEEE
set AWS_SECRET_ACCESS_KEY=76TjRiiV3tc89AKo5FmicwESK5X8QHps7aUGEpo0
set AWS_DEFAULT_REGION=us-east-1
set AWS_DEFAULT_OUTPUT=json

### Azure


Install and configure Azure CLI


### License

This application is licensed to Softtek under Apache.
