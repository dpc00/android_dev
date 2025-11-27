@echo off
for /f "usebackq tokens=1,2 skip=1" %%i in (`wmic VOLUME get label^,driveletter`) do (
	if "%%j"=="CODE0" set FLASH0=%%i
	if "%%j"=="CODE1" set FLASH1=%%i
	if "%%j"=="CODE2" set FLASH2=%%i
	if "%%j"=="CODE3" set FLASH3=%%i
	if "%%j"=="CODE4" set FLASH4=%%i
	if "%%j"=="CODE5" set FLASH5=%%i
	if "%%j"=="CODE6" set FLASH6=%%i
	if "%%j"=="CODE7" set FLASH7=%%i
)
path %path%;%~d0\Programs
@echo on
if not "%FLASH0%"=="" \programs\removedrive\x64\removedrive.exe %FLASH0% -47 -e -dbg >%~d0\temp.txt
if not "%FLASH1%"=="" \programs\removedrive\x64\removedrive.exe %FLASH1% -47 -e -dbg >>%~d0\temp.txt
if not "%FLASH2%"=="" \programs\removedrive\x64\removedrive.exe %FLASH2% -47 -e -dbg >>%~d0\temp.txt
if not "%FLASH3%"=="" \programs\removedrive\x64\removedrive.exe %FLASH3% -47 -e -dbg >>%~d0\temp.txt
if not "%FLASH4%"=="" \programs\removedrive\x64\removedrive.exe %FLASH4% -47 -e -dbg >>%~d0\temp.txt
if not "%FLASH5%"=="" \programs\removedrive\x64\removedrive.exe %FLASH5% -47 -e -dbg >>%~d0\temp.txt
if not "%FLASH6%"=="" \programs\removedrive\x64\removedrive.exe %FLASH6% -47 -e -dbg >>%~d0\temp.txt
notepad %~d0\temp.txt
pause