#!/usr/bin/python3
import hashlib
import os 
from winreg import *
import win32api

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

system_drive = os.environ['WINDIR'].lower()
cmd =  system_drive + "\\system32\\cmd.exe"
powershell =  system_drive + "\\system32\\windowspowershell\\v1.0\\powershell.exe"
explorer =  system_drive + "\\explorer.exe"
sethc =  system_drive + "\\system32\\sethc.exe"
osk =  system_drive + "\\system32\\osk.exe"
narrator =  system_drive + "\\system32\\narrator.exe"
magnify =  system_drive + "\\system32\\magnify.exe"
displayswitch =  system_drive + "\\system32\\displayswitch.exe"
atbroker =  system_drive + "\\system32\\atbroker.exe"
key = 'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\'
reg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
debuggerkeys = ['sethc.exe','utilman.exe','osk.exe','narrator.exe','magnify.exe','displayswitch.exe','atbroker.exe']
property = 'Debugger'
paths = [cmd,powershell,explorer,sethc,osk,narrator,magnify,displayswitch,atbroker]
launchers = [cmd,powershell,explorer]
values = {}
file_description = {}
validation_details = {system_drive + '\\system32\\cmd.exe': 'windows command processor', system_drive + '\\system32\\windowspowershell\\v1.0\\powershell.exe': 'windows powershell', system_drive + '\\explorer.exe': 'windows explorer', system_drive + '\\system32\\sethc.exe': 'accessibility shortcut keys', system_drive + '\\system32\\osk.exe': 'accessibility on-screen keyboard', system_drive + '\\system32\\narrator.exe': 'screen reader', system_drive + '\\system32\\magnify.exe': 'microsoft screen magnifier', system_drive + '\\system32\\displayswitch.exe': 'display switch',  system_drive + '\\system32\\atbroker.exe': 'windows assistive technology manager'}

for path in paths:
	hash = md5(path)
	values[path.lower()] = hash
	langs = win32api.GetFileVersionInfo(path, r'\VarFileInfo\Translation')
	details = r'StringFileInfo\%04x%04x\FileDescription' %(langs[0][0], langs[0][1])        
	file_description[path.lower()] = win32api.GetFileVersionInfo(path, details).lower()
	
print("Message,MD5,Match,Description")	
for key1, value1 in values.items(): 
	for key2, value2 in values.items():
		if key1 != key2 and key2 in launchers and key1 not in launchers:
			if value1 == value2:
				print(key1.split('\\')[-1]+" has been possibly replaced with " + key2.split('\\')[-1] +","+ value1 + ",true, ")
			else:
				print(key1.split('\\')[-1]+" has not been replaced with " + key2.split('\\')[-1] +","+ value1 + ",false, ")

for key3, value3 in file_description.items(): 
	for key4, value4 in validation_details.items():
		if key3 != key4 and key4 in launchers and key3 not in launchers:
			if value3 == value4:
				print(key3.split('\\')[-1]+" has the same descption as " + key4.split('\\')[-1] +",,false,"+value3)
			else:
				print(key3.split('\\')[-1]+" doesn't have the same descption as " + key4.split('\\')[-1] +",,false,"+value3)
				
key = OpenKey(reg, key)
for i in range(1024):
	try: 
		for name in debuggerkeys:
			asubkey=OpenKey(key,name)
			val=QueryValueEx(asubkey, "Debugger")
			print(name + " has been set with a debugger with the following name " + val[0].split('\\')[-1] +","+ md5(val[0]) + ",true, ")
			debuggerkeys.remove(name)
	except EnvironmentError:
		break
