shortcut.exe /F:"Test1.lnk" /A:C /T:"\!FLASH0!\PStart.bat" /P: /W:"!FLASH0!\Projects\py-test"
if not errorlevel 1 cscript shortcut.vbs