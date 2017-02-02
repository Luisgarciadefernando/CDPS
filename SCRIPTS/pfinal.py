#!/usr/bin/python
from subprocess import call, Popen
import commands
import sys
import os

#Creamos el escenario inicial

os.system ("sudo vnx -f pfinal.xml -v --create")


#Instalamos nodeJS en los servidoes S1-S4

os.system("sudo lxc-attach -n s1 -- apt-get install nodejs -y")
for i in range(2, 5):
    os.system("sudo lxc-attach -n s{i} -- apt-get install nodejs -y".format(i=str(i)))


#Preparamos el servidor S1 para la utilizacion de Mongodb

os.system("""
	sudo lxc-attach -n s1 -- mkdir data
	sudo lxc-attach -n s1 -- mkdir /data/db
	sudo lxc-attach -n s1 -- chmod +rwx /data/db
""")
Popen(["sudo", "lxc-attach", "-n", "s1", "--", "mongod", ">", "/dev/null", "2>&1", "&"])
 


#Clonamos los proyectors CDPSgram-photos y CDPSgram-server en s1 el primero y s2, s3 y s4 el segundo.

os.system("""
	sudo lxc-attach -n s1 -- git clone https://github.com/Luisgarciadefernando/PracticaS.git
	sudo lxc-attach -n s1 -- mv PracticaS /root
	sudo lxc-attach -n s1 -- sh -c 'cd /root/PracticaS && npm install'
""")

for i in range(2, 5):
	os.system("""
	sudo lxc-attach -n s{i} -- git clone https://github.com/Luisgarciadefernando/PracticaF.git
	sudo lxc-attach -n s{i} -- mv PracticaF /root
	sudo lxc-attach -n s{i} -- sh -c 'cd /root/PracticaF && npm install'
""".format(i=str(i)))

#Anadimos los servidores al GlusterfS

os.system("""
    sudo lxc-attach -n nas1 -- gluster peer probe 10.1.4.22
    sudo lxc-attach -n nas1 -- gluster peer probe 10.1.4.23
""")
os.system("sudo lxc-attach -n nas1 -- gluster peer status")
os.system("sudo lxc-attach -n nas1 -- gluster volume create nas replica 3 10.1.4.21:/nas 10.1.4.22:/nas 10.1.4.23:/nas force")
os.system("sudo lxc-attach -n nas1 -- gluster volume start nas")

#Montamos los servidores

for i in range (2 ,5):
	os.system("""
	sudo lxc-attach -n s{i} -- mkdir /mnt/nas
	sudo lxc-attach -n s{i} -- mount -t glusterfs nas1:/nas /mnt/nas	
""".format(i=str(i)))
if os.system("sudo lxc-attach -n s2 -- os.path.isdir(/mnt/nas/fotos)"):
	os.system("sudo lxc-attach -n s2 -- rm -R /mnt/nas/fotos")
os.system("sudo lxc-attach -n s2 -- mkdir /mnt/nas/fotos")


#Configuramos el balanceador de carga para poder utilizarlo

os.system("sudo lxc-attach -n lb -- service apache2 stop")
Popen(["sudo", "lxc-attach", "-n", "lb", "--", "xr", "--verbose", "--server", "http:0:80", "-dr", "--backend", "10.1.3.12:8000", "--backend", "10.1.3.13:8000", "--backend", "10.1.3.14:8000", "--web-interface", "0:8001"])

#Arrancamos los servidores

os.system("sudo lxc-attach -n s1 -- sh -c 'cd /root/PracticaS && npm start' &")
for i in range(2, 5):
	os.system("sudo lxc-attach -n s{i} -- sh -c 'cd /root/PracticaF && npm start' &".format(i=str(i)))








