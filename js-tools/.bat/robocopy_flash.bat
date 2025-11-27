setlocal
for /f "usebackq tokens=1,2 skip=1" %%i in (`wmic VOLUME get label^,driveletter`) do (
	if "%%j"=="CODE0" set FLASH0=%%i
	if "%%j"=="CODE1" set FLASH1=%%i
	if "%%j"=="CODE2" set FLASH2=%%i
	if "%%j"=="CODE3" set FLASH3=%%i
	if "%%j"=="CODE4" set FLASH4=%%i
	if "%%j"=="CODE5" set FLASH5=%%i
	if "%%j"=="CODE6" set FLASH6=%%i
)
set exc=/XD %FLASH0%\$RECYCLE.BIN
set exc=%exc% /XD "%FLASH0%\System Volume Information"
rem set exc=%exc% /XD %FLASH0%\PortableApps\FirefoxPortable\Data\profile

set opt=/A-:RSH /J /MIR /MOT:1 /MT /NP /R:0 /S /SL /W:0 /XO

if [%FLASH0%] NEQ [] (
	if [%FLASH1%] NEQ [] (
	   if [%FLASH1%] NEQ [%FLASH0%] (
			start robocopy.exe %FLASH0%\ %FLASH1%\ %opt% %exc%
		)
	)
	if [%FLASH2%] NEQ [] (
		if [%FLASH2%] NEQ [%FLASH0%] (
			start robocopy.exe %FLASH0%\ %FLASH2%\ %opt% %exc%
		)
	)
	if [%FLASH3%] NEQ [] (
		if [%FLASH3%] NEQ [%FLASH0%] (
			start robocopy.exe %FLASH0%\ %FLASH3%\ %opt% %exc%
		)
	)
	if [%FLASH4%] NEQ [] (
		if [%FLASH4%] NEQ [%FLASH0%] (
	   		start robocopy.exe %FLASH0%\ %FLASH4%\ %opt% %exc%
		)
	)
	if [%FLASH5%] NEQ [] (
		if [%FLASH5%] NEQ [%FLASH0%] (
	   		start robocopy.exe %FLASH0%\ %FLASH5%\ %opt% %exc%
		)
	)
	if [%FLASH6%] NEQ [] (
		if [%FLASH6%] NEQ [%FLASH0%] (
			start robocopy.exe %FLASH0%\ %FLASH6%\ %opt% %exc%
		)
	)
)
