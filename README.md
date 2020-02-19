# StickyKeyDetector
A python script that is inspired by @TrullJ powershell implementation that tries to identify Sticky Key backdoors by checking the following:
* Checks the file hashes of (cmd.exe, powershell.exe,explorer.exe) on the local system against (sethc.exe,osk.exe,Narrator.exe,Magnify.exe,DisplaySwitch.exe) to verfiy if they have been replaced or not.

* Queries the registray key "SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\" and checks if a debbuger was set to sethc.exe or utilman.exe.
