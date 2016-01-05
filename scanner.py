import socket
import sys, time
from datetime import datetime
import subprocess
import asyncio

host = ''
max_port = 1024
min_port = 1

def scan_host(host, port, r_code = 1):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        print("  [+]  %d open" % port)
        s.close()
    except ConnectionRefusedError as e:
        print("  [+] %d closed" % port)
    except socket.timeout:
        pass
    return r_code

if __name__ == '__main__':
    try:
        hosts = []
        for ip in range(1,254):
            netRange = '10.10.50.'
            host = netRange + str(ip)
            hosts.append(host)
        for host in hosts:
            scan_ports = [80,135,443,445,137]
            print ("[***] Starting a Portscan on host %s:\n" % host )
            for port in scan_ports:
                response = scan_host(host, port)

    except KeyboardInterrupt:
        sys.exit(1)
