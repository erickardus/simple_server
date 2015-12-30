name 'haproxy'
maintainer 'Miguel Leal'
maintainer_email 'miguel.leal@softtek.com'
license 'all_rights'
description 'Installs/Configures haproxy'
long_description 'Installs/Configures haproxy'
%w{ centos redhat fedora ubuntu debian amazon }.each do |os|
  supports os
end
version '0.1.0'
