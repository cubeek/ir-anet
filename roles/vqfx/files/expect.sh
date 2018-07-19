#!/bin/bash
set -x

expect -c"
  set timeout 300
  spawn vagrant ssh vqfx
  expect \"Password:\"
  send \"Juniper\r\"
  expect \"root@:RE:0%\"
  send \"cli\r\"
  expect \"root>\"
  send \"config\r\"
  expect \"root#\"
  send \"set interfaces em1 unit 0 family inet address 169.254.0.2/24\r\"
  expect \"root#\"
  send \"commit\r\"
  expect \"root#\"
  send \"exit\r\"
  expect \"root>\"
  send \"restart chassis-control\r\"
  expect \"root>\"
  send \"exit\r\"
  expect \"root@:RE:0%\"
  send \"exit\r\"
"

sleep 60

# get vagrant config for scp command
vagrant ssh-config vqfx > /tmp/sshconf

# copy the infterface wait script into the appliance
expect -c "
spawn bash -c \"scp -F /tmp/sshconf /tmp/wait.sh vqfx:~/wait.sh\"
expect {
  -re \".*es.*o.*\" {
    exp_send \"yes\r\"
    exp_continue
  }
  -re \".*sword.*\" {
    exp_send \"Juniper\r\"
  }
}
interact
"

# wait for interfaces to come up, then configure
expect -c"
  set timeout 300
  spawn vagrant ssh vqfx
  expect \"Password:\"
  send \"Juniper\r\"
  expect \"root@:RE:0%\"
  send \"csh wait.sh\r\"
  expect \"root@:RE:0%*\"
  send \"cli\r\"
  expect \"root>\"
  send \"config\r\"
  expect \"root#\"
  send \"set vlans br-tenant vlan-id 37\r\"
  expect \"root#\"
  send \"set interfaces interface-range br-tenant unit 0 family ethernet-switching vlan members br-tenant\r\"
  expect \"root#\"
  send \"set interfaces irb unit 1 family inet address 192.168.2.250/24\r\"
  expect \"root#\"
  send \"set vlans default l3-interface irb.1\r\"
  expect \"root#\"
  send \"set interfaces xe-0/0/0 unit 0 family ethernet-switching vlan members default\r\"
  expect \"root#\"
  send \"set interfaces xe-0/0/1 unit 0 family ethernet-switching vlan members default\r\"
  expect \"root#\"
  send \"set interfaces interface-range br-tenant member-range xe-0/0/0 to xe-0/0/1\r\"
  expect \"root#\"
  send \"set interfaces interface-range br-tenant native-vlan-id 37\r\"
  expect \"root#\"
  send \"delete interfaces interface-range br-tenant unit 0 family ethernet-switching vlan members br-tenant\r\"
  expect \"root#\"
  send \"set interfaces interface-range br-tenant unit 0 family ethernet-switching interface-mode trunk\r\"
  expect \"root#\"
  send \"set interfaces interface-range br-tenant unit 0 family ethernet-switching vlan members br-tenant\r\"
  expect \"root#\"
  send \"commit\r\"
  expect \"root#\"
  send \"exit\r\"
  expect \"root#\"
  send \"exit\r\"
  expect \"root>\"
  send \"exit\r\"
  expect \"root@:RE:0%\"
  send \"exit\r\"
"
