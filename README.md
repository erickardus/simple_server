
You will need to create the following env variables in your machine:

--------------- Chef ---------------------

You need to create a .chef folder inside chef-repo, containing knife.rb and related credentials to your chef server.

> dir

29/12/2015  10:23 p. m.    <DIR>          .
29/12/2015  10:23 p. m.    <DIR>          ..
29/12/2015  10:16 p. m.    <DIR>          chef-repo
29/12/2015  12:19 p. m.               372 README.md
29/12/2015  12:24 p. m.    <DIR>          simple-server-project

------------- AWS ------------------------

ENV["AWS_ACCESS_KEY_ID"]
ENV["AWS_SECRET_ACCESS_KEY"]
ENV["AWS_DEFAULT_REGION"]
ENV["AWS_DEFAULT_OUTPUT"]

Example:

set AWS_ACCESS_KEY_ID=AAAABBBBCCCCDDDDEEEE
set AWS_SECRET_ACCESS_KEY=76TjRiiV3tc89AKo5FmicwESK5X8QHps7aUGEpo0
set AWS_DEFAULT_REGION=us-east-1
set AWS_DEFAULT_OUTPUT=json


-------------- Azure -----------------------

Install and configure Azure CLI