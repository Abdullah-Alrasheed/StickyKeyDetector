#!/usr/bin/python3
import hashlib
import os 
from winreg import *

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

system_drive = os.environ['WINDIR']
cmd =  system_drive + "\\System32\\cmd.exe"
powershell =  system_drive + "\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
explorer =  system_drive + "\\explorer.exe"
sethc =  system_drive + "\\System32\\sethc.exe"
osk =  system_drive + "\\System32\\osk.exe"
narrator =  system_drive + "\\System32\\Narrator.exe"
magnify =  system_drive + "\\System32\\Magnify.exe"
displayswitch =  system_drive + "\\System32\\DisplaySwitch.exe"
key = 'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\'
reg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
debuggerkeys = ['sethc.exe','osk.exe','Narrator.exe','Magnify.exe','DisplaySwitch.exe','utilman.exe']
property = 'Debugger'
paths = [cmd,powershell,explorer,sethc,osk,narrator,magnify,displayswitch]
launchers = [cmd,powershell,explorer]
values = {}

for path in paths:
	hash = md5(path)
	values[path] = hash
print("Message,MD5,Match")	
for key1, value1 in values.items(): 
	for key2, value2 in values.items():
		if key1 != key2 and key2 in launchers and key1 not in launchers:
			if value1 == value2:
				print(key1.split('\\')[-1]+" has been possibly replaced with " + key2.split('\\')[-1] +","+ value1 + ",true")
			else:
				print(key1.split('\\')[-1]+" has not been replaced with " + key2.split('\\')[-1] +","+ value1 + ",false")

key = OpenKey(reg, key)
for i in range(1024):
	try: 
		for name in debuggerkeys:
			asubkey=OpenKey(key,name)
			val=QueryValueEx(asubkey, "Debugger")
			print(name + " has been set with a debugger with the following name " + val[0].split('\\')[-1] +","+ md5(val[0]) + ",true")
			debuggerkeys.remove(name)
	except EnvironmentError:
		break
