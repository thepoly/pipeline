Instructions of how to operate the Polytechnic's server when not on the RPI wifi:

Use RPI's VPN: TODO

How to access the poly.rpi.edu server and solve common issues:

Connect to Cisco IPSEC’s RPI VPN. It is the only VPN that works with the Polytechnic’s server.

Use the IP address 128.113.71.217 to connect to RPI’s server, which hosts poly.rpi.edu as well as other RPI-based sites. Use port 443.

Use 10.10.10.1 to access Pfsense, use the following credentials to get access: 
admin
(Ask the Polytechnic for the password)

To launch the virtual machine, Dokku:

Use 10.10.10.14
Login with root
(Ask the Polytechnic for the password)

To run with ESXi:
srv1.poly.rpi.edu
Login with root
(Ask the Polytechnic for the password)

Common issue: Running out of server storage

To solve the issue of server having limited server space delete log files:
Remove access.log.2.gz
Var log
Rm *.log.*
Cat error.log
Find other large files
