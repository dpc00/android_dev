@echo on
setlocal enabledelayedexpansion
cd \Projects\DirSyncApp
if exist dirsync.log del dirsync.log
if not "%FLASH0%"=="" set arg0=%FLASH0%\
if not "%FLASH1%"=="" set arg1=%FLASH1%\
if not "%FLASH2%"=="" set arg2=%FLASH2%\
if not "%FLASH3%"=="" set arg3=%FLASH3%\
if not "%FLASH4%"=="" set arg4=%FLASH4%\
if not "%FLASH5%"=="" set arg5=%FLASH5%\
if not "%FLASH6%"=="" set arg6=%FLASH6%\

set args=%arg0% %arg1% %arg2% %arg3% %arg4% %arg5% %arg6%
dirsync_libs.bat !args!
