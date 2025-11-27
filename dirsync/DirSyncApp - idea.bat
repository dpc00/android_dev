@echo on

setlocal enabledelayedexpansion
set src=C:\
set dst=%TEMP%


set rd=
set arg1=%src%\%rd%
set arg2=%dst%\%rd%
set args=%arg1% %arg2%


dirsync_libs.bat !args!

