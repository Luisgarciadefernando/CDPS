#!/usr/bin/python
from subprocess import call, Popen
import commands
import sys
import os


#Configuracion de nagios

call(["sudo", "lxc-attach", "-n", "nagios", "--", "sudo", "apt-get", "update"])
call(["sudo", "lxc-attach", "-n", "nagios", "--", "sudo", "apt-get", "install", "nagios3", "-y"])

#Creacion de ficheros de configuracion de nagios

call(["sudo", "lxc-attach", "-n", "nagios", "--", "git", "clone", "https://github.com/Luisgarciadefernando/Nagios.git"])
call(["sudo", "lxc-attach", "-n", "nagios", "--", "cp", "/Nagios/s1_nagios2.cfg", "/etc/nagios3/conf.d/"])
call(["sudo", "lxc-attach", "-n", "nagios", "--", "cp", "/Nagios/s2_nagios2.cfg", "/etc/nagios3/conf.d/"])
call(["sudo", "lxc-attach", "-n", "nagios", "--", "cp", "/Nagios/s3_nagios2.cfg", "/etc/nagios3/conf.d/"])
call(["sudo", "lxc-attach", "-n", "nagios", "--", "cp", "/Nagios/s4_nagios2.cfg", "/etc/nagios3/conf.d/"])
call(["sudo", "lxc-attach", "-n", "nagios", "--", "cp", "/Nagios/nas1_nagios2.cfg", "/etc/nagios3/conf.d/"])
call(["sudo", "lxc-attach", "-n", "nagios", "--", "cp", "/Nagios/nas2_nagios2.cfg", "/etc/nagios3/conf.d/"])
call(["sudo", "lxc-attach", "-n", "nagios", "--", "cp", "/Nagios/nas3_nagios2.cfg", "/etc/nagios3/conf.d/"])
call(["sudo", "lxc-attach", "-n", "nagios", "--", "cp", "/Nagios/hostgroups_nagios2.cfg", "/etc/nagios3/conf.d/hostgroups_nagios2.cfg"])
call(["sudo", "lxc-attach", "-n", "nagios", "--", "service", "apache2", "restart"])
call(["sudo", "lxc-attach", "-n", "nagios", "--", "service", "nagios3", "restart"])


#Fcihero de configuracion de FW

os.system("""
	sudo lxc-attach -n fw -- git clone https://github.com/Luisgarciadefernando/FWB.git
	sudo lxc-attach -n fw -- cp /FWB/fw.fwb /root/fw.fwb
""")

