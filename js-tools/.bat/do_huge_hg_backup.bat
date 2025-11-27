@echo on
setlocal enabledelayedexpansion
setlocal

for /f "usebackq tokens=1,2 skip=1" %%i in (`wmic VOLUME get label^,driveletter`) do (
	if "%%j"=="CODE0" set FLASH0=%%i
)

if [%FLASH0%] EQU [] exit

%CODE0%
cd \

set HGUSER=Donald Chitester ^<dpchitester^@gmail.com^>
set HOME=%FLASH0%\

path %FLASH0%\.bat;%path%
path %path%;%FLASH0%\Programs\Mercurial

call :main %FLASH0% PortableApps
call :main %FLASH0% Programs
call :main %FLASH0% Projects
endlocal
exit /B

:main
setlocal
rem code0 driveletter: %1
rem MAIN subdir: %2
set sd=%~1\%~2
if ["!sd: =!"] NEQ ["!sd!"] set sd=^"!sd!^"
for /F "usebackq delims=" %%M in (`dir %sd% /A:D /B`) do (
	set ssd=%~1\%~2\%%~M
	if ["!ssd: =!"] NEQ ["!ssd!"] set ssd=^"!ssd!^"
	call :do_backup !ssd!
)
endlocal
exit /B

:do_backup
setlocal
set HG_WORK_TREE=%1
pushd %HG_WORK_TREE%
if exist hgbackup.bat call hgbackup.bat
popd
endlocal
exit /B
