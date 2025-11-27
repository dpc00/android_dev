robocopy %~d0\Programs\USB_Disk_Eject %TEMP%\USB_Disk_Eject /S /MIR
start %TEMP%\USB_Disk_Eject\USB_Disk_Eject.exe
