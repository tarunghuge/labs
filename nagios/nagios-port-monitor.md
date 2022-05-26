

How To Monitor Network Switch and Ports Using Nagios
====================================================

by Ramesh Natarajan   on November 3, 2008

[Tweet](httpstwitter.comshare)

![[Nagios Monitoring Switch]](httpsstatic.thegeekstuff.comwp-contentuploads200810nagios-switch.jpg [Nagios Monitoring Switch])Nagios is hands-down the best monitoring tool to monitor host and network equipments. Using Nagios plugins you can monitor pretty much monitor anything.  
  
I use Nagios intensively and it gives me peace of mind knowing that I will get an alert on my phone, when there is a problem. More than that, if warning levels are setup properly, Nagios will proactively alert you before a problem becomes critical.  
  
Earlier I wrote about, how to [setup Nagios](httpswww.thegeekstuff.com200805nagios-30-jumpstart-guide-for-red-hat-overview-installation-and-configuration) to monitor [Linux Host](httpswww.thegeekstuff.com200806how-to-monitor-remote-linux-host-using-nagios-30), [Windows Host](httpswww.thegeekstuff.com200807how-to-monitor-remote-windows-machine-using-nagios-on-linux) and [VPN device](httpswww.thegeekstuff.com200809how-to-monitor-vpn-active-sessions-and-temperature-using-nagios).  
  
In this article, I’ll explain how to configure Nagios to monitor network switch and it’s active ports.  

### 1. Enable switch.cfg in nagios.cfg

Uncomment the switch.cfg line in usrlocalnagiosetcnagios.cfg as shown below.

[nagios-server]# grep switch.cfg usrlocalnagiosetcnagios.cfg
cfg_file=usrlocalnagiosetcobjectsswitch.cfg

### 2. Add new hostgroup for switches in switch.cfg

Add the following switches hostgroup to the usrlocalnagiosetcobjectsswitch.cfg file.

define hostgroup{
hostgroup_name  switches
alias           Network Switches
}

### 3. Add a new host for the switch to be monitered

In this example, I’ve defined a host to monitor the core switch in the usrlocalnagiosetcobjectsswitch.cfg file. Change the address directive to your switch ip-address accordingly.

define host{
use             generic-switch
host_name       core-switch
alias           Cisco Core Switch
address         192.168.1.50
hostgroups      switches
}

### 4. Add common services for all switches

Displaying the uptime of the switch and verifying whether switch is alive are common services for all switches. So, define these services under the switches hostgroup_name as shown below.

# Service definition to ping the switch using check_ping
define service{
use                     generic-service
hostgroup_name          switches
service_description     PING
check_command           check_ping!200.0,20%!600.0,60%
normal_check_interval   5
retry_check_interval    1
}

# Service definition to monitor switch uptime using check_snmp
define service{
use                     generic-service
hostgroup_name          switches
service_description     Uptime
check_command           check_snmp!-C public -o sysUpTime.0
}

### 5. Add service to monitor port bandwidth usage

check_local_mrtgtraf uses the [Multil Router Traffic Grapher – MRTG](httposs.oetiker.chmrtg). So, you need to install MRTG for this to work properly. The .log file mentioned below should point to the MRTG log file on your system.

define service{
use			        generic-service
host_name			core-switch
service_description	Port 1 Bandwidth Usage
check_command		check_local_mrtgtraf!varlibmrtg192.168.1.11_1.log!AVG!1000000,2000000!5000000,5000000!10
}

### 6. Add service to monitor an active switch port

Use check_snmp to monitor the specific port as shown below. The following two services monitors port#1 and port#5. To add additional ports, change the value ifOperStatus.n accordingly. i.e n defines the port#.

(adsbygoogle = window.adsbygoogle  []).push({});

# Monitor status of port number 1 on the Cisco core switch
define service{
use                  generic-service
host_name            core-switch
service_description  Port 1 Link Status
check_command        check_snmp!-C public -o ifOperStatus.1 -r 1 -m RFC1213-MIB
}

# Monitor status of port number 5 on the Cisco core switch
define service{
use                  generic-service
host_name            core-switch
service_description  Port 5 Link Status
check_command	       check_snmp!-C public -o ifOperStatus.5 -r 1 -m RFC1213-MIB
}

### 7. Add services to monitor multiple switch ports together

Sometimes you may need to monitor the status of multiple ports combined together. i.e Nagios should send you an alert, even if one of the port is down. In this case, define the following service to monitor multiple ports.

# Monitor ports 1 - 6 on the Cisco core switch.
define service{
use                   generic-service
host_name             core-switch
service_description   Ports 1-6 Link Status
check_command         check_snmp!-C public -o ifOperStatus.1 -r 1 -m RFC1213-MIB, -o ifOperStatus.2 -r 1 -m RFC1213-MIB, -o ifOperStatus.3 -r 1 -m RFC1213-MIB, -o ifOperStatus.4 -r 1 -m RFC1213-MIB, -o ifOperStatus.5 -r 1 -m RFC1213-MIB, -o ifOperStatus.6 -r 1 -m RFC1213-MIB
}

### 8. Validate configuration and restart nagios

Verify the nagios configuration to make sure there are no warnings and errors.

# usrlocalnagiosbinnagios -v usrlocalnagiosetcnagios.cfg

Total Warnings 0
Total Errors   0
Things look okay - No serious problems were detected during the pre-flight check

Restart the nagios server to start monitoring the VPN device.

# etcrc.dinit.dnagios stop
Stopping nagios .done.

# etcrc.dinit.dnagios start
Starting nagios done.

Verify the status of the switch from the Nagios web UI http{nagios-server}nagios as shown below

[![[Nagios GUI for Network Switch]](httpsstatic.thegeekstuff.comwp-contentuploads200810nagios-ui-for-switch.jpg [Nagios GUI for Network Switch])](httpsstatic.thegeekstuff.comwp-contentuploads200810nagios-ui-for-switch.jpg)

Fig Nagios GUI displaying status of a Network Switch

### 9. Troubleshooting

Issue1 Nagios GUI displays “check_mrtgtraf Unable to open MRTG log file” error message for the Port bandwidth usage

Solution1 make sure the .log file defined in the check_local_mrtgtraf service is pointing to the correct location.  
  
Issue2 Nagios UI displays “Return code of 127 is out of bounds – plugin may be missing” error message for Port Link Status.

Solution2 Make sure both net-snmp and net-snmp-util packages are installed. In my case, I was missing the net-snmp-utils package and installing it resolved this issue as shown below.

[nagios-server]# rpm -qa  grep net-snmp
net-snmp-libs-5.1.2-11.el4_6.11.2
net-snmp-5.1.2-11.el4_6.11.2

[nagios-server]# rpm -ivh net-snmp-utils-5.1.2-11.EL4.10.i386.rpm
Preparing...       ########################################### [100%]
1net-snmp-utils   ########################################### [100%]

[nagios-server]# rpm -qa  grep net-snmp
net-snmp-libs-5.1.2-11.el4_6.11.2
net-snmp-5.1.2-11.el4_6.11.2
net-snmp-utils-5.1.2-11.EL4.10

Note After you’ve installed net-snmp and net-snmp-utils, re-compile and re-install nagios plugins as explained in “6. Compile and install nagios plugins” in the [Nagios 3.0 jumpstart guide](httpswww.thegeekstuff.com200805nagios-30-jumpstart-guide-for-red-hat-overview-installation-and-configuration).


