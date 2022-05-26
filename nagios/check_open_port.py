#!/usr/bin/env python

'''
Script to check open ports 
Creation date: 19/01/2017
Date last updated: 19/03/2017

* 
* License: GPL
* Copyright (c) 2017 DI-FCUL
* 
* Description:
* 
* This file contains the check_open_port plugin
* 
* Use the nrpe program to check request on remote server.
* 
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
* 
* You should have received a copy of the GNU General Public License
* along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

# import modules
import socket
import subprocess
import sys
from optparse import OptionParser

__author__ = "\nAuthor: Raimundo Henrique da Silva Chipongue\nE-mail: fc48807@alunos.fc.ul.pt, chipongue1@gmail.com\nInstitution: Faculty of Science of the University of Lisbon\n"
__version__= "1.0.0"

# define exit codes
ExitOK = 0
ExitWarning = 1
ExitCritical = 2
ExitUnknown = 3

def scan(opts):
    listfound = []
    try:
        for port in range(1,7000):  
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((opts.host, port))
            if result == 0:
                listfound.extend([int(i) for i in ("{}".format(port)).split(" ")])
        return listfound
    except:
        print("Error, unable to scan")
        sys.exit(ExitUnknown)

def getopenport(opts):
    try:
        authorized_ports = [int(i) for i in opts.port.split(",")]
        authorized_ports = sorted(authorized_ports)       
    except:
        print("Error, check list of authorized ports, i.e.: -p 500,21,23,80,3333")
        sys.exit(ExitUnknown)
        
    all_open_ports = scan(opts)
    unauthorized_ports = sorted((list(set(all_open_ports) - (set(authorized_ports)))))
    num_anauth_open_ports = len(unauthorized_ports)
    if num_anauth_open_ports == 0:
        print("Not found any anauthorized port open.")
        sys.exit(ExitOK)
    else:
        unauthorized_ports = ", ".join(str(x) for x in unauthorized_ports)
        print("Were found the following %s unauthorized open ports: %s!" %(num_anauth_open_ports, unauthorized_ports))
        sys.exit(ExitCritical)
      
def main():
    parser = OptionParser("usage: %prog -H <IP address> and -p <port or list of ports>, that have been authorized to are open, e.i. <-p 500,21,23,80,3333>")
    parser.add_option("-H","--hostaddress", dest="host", help="Specify the IP address you want to check")
    parser.add_option("-p","--port", dest="port", default="0", help="Specify the ports or list of allowed ports to be open, i.e.: <-p 500,21,23,80,3333>")
    parser.add_option("-V","--version", action="store_true", dest="version", help="This option show the current version number of the program and exit")
    parser.add_option("-A","--author", action="store_true", dest="author", help="This option show author information and exit")
    (opts, args) = parser.parse_args()
    
    if opts.author:
        print(__author__)
        sys.exit()
    if opts.version:
        print("check_open_port.py %s"%__version__)
        sys.exit()
    if opts.host and opts.port:
        try:
            ServerIP = socket.gethostbyname(opts.host)
        except:
            parser.error("Incorrect IP Address.")
        getopenport(opts)
    else:
        parser.error(" This program requires at least one argument.") 
        

if __name__ == '__main__':
    main()
