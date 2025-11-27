setlocal enabledelayedexpansion

@echo on
for /f "usebackq skip=1 delims=" %%i in (`wmic OS get OSArchitecture`) do (
	set sline=%%i
	set dw=!SLINE:~0,6!
	if [!dw!] EQU [32-bit] (
		set ARCH=x32
	)
	if [!dw!] EQU [64-bit] (
		set ARCH=x64
	)
)

for /f "usebackq skip=1 delims=" %%i in (`wmic VOLUME get label^,driveletter`) do (
	set sline=%%i
	set dl=!SLINE:~0,2!
	set vl=!SLINE:~13,5!
	if [!vl!] EQU [CODE0] (
		set FLASH0=!dl!
		echo CODE0 drive found on %FLASH0%
	)
	if [!vl!] EQU [CODE1] (
		set FLASH1=!dl!
		echo CODE1 drive found on %FLASH1%
	)
	if [!vl!] EQU [CODE2] (
		set FLASH2=!dl!
		echo CODE2 drive found on %FLASH2%
	)
	if [!vl!] EQU [CODE3] (
		set FLASH3=!dl!
		echo CODE3 drive found on %FLASH3%
	)
	if [!vl!] EQU [CODE4] (
		set FLASH4=!dl!
		echo CODE4 drive found on %FLASH4%
	)
	if [!vl!] EQU [CODE5] (
		set FLASH5=!dl!
		echo CODE5 drive found on %FLASH5%
	)
	if [!vl!] EQU [CODE6] (
		set FLASH6=!dl!
		echo CODE6 drive found on %FLASH6%
	)
)
if [%FLASH0%] EQU [] (
	echo No CODE0 drive found!
	pause
	exit /B
)

set CLONE_DIR=
set EXE4J_JAVA_HOME=%FLASH0%\Programs\jDK%ARCH%
set GOLAND_PROPERTIES=%FLASH0%\Programs\GoLand\idea.properties
set GOROOT=%FLASH0%\Programs\go.%ARCH%
set GOPATH=%FLASH0%\Projects\go
set HGUSER=Donald Chitester ^<dpchitester^@gmail.com^>
set HOME=%FLASH0%\
set IDEA_PROPERTIES=%FLASH0%\Programs\idea\idea.properties
set JAVA_HOME=%FLASH0%\Programs\jDK%ARCH%\jre
set JDK_HOME=%FLASH0%\Programs\jDK%ARCH%
set M2_HOME=%FLASH0%\Projects\lib\.m2
set NODE_PATH=%FLASH0%\Programs\node-v8.9.1-win-%ARCH%\node_modules;%FLASH0%\Projects\tools\lib
set PUB_CACHE=%FLASH0%\Programs\Pub\Cache
set PYTHONHOME=%FLASH0%\Programs\Python36%ARCH%
set PYTHONPATH=%FLASH0%\Projects\py-test

@echo on
path %FLASH0%\Programs\7-Zip;%path%
path %FLASH0%\Programs\dart-sdk.%ARCH%\bin;%path%
path %FLASH0%\Programs\jDK%ARCH%\bin;%path%
path %FLASH0%\Programs\jDK%ARCH%\lib;%path%
path %FLASH0%\Programs\jDK%ARCH%\jre\bin;%path%
path %FLASH0%\Programs\jDK%ARCH%\jre\lib;%path%
path %FLASH0%\Programs\Mercurial;%path%
path %FLASH0%\Programs\node-v8.9.1-win-%ARCH%;%path%
path %FLASH0%\Programs\Python36%ARCH%;%path%
path "%FLASH0%\Programs\Sublime Text Build 3143 %ARCH%";%path%
path %FLASH0%\Programs\Utils;%path%
path %GOPATH%\bin;%path%
path %GOROOT%\bin;%path%
path %PUB_CACHE%\bin;%path%
path "%FLASH0%\Programs\eclipse %ARCH%";%path%
%*
