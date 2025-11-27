setlocal enabledelayedexpansion
rem src_rt: %1
rem dst_rt: %2
rem rd: %3

set t=%~3

if [%t:~-1,1%] EQU [\] (
	set fp1=%1\%~3
	set fp2=%2\%~3
	set rd=%t:~0,-1%
)
if [%t:~-1,1%] NEQ [\] (
	set fp1=%1\\%~3
	set fp2=%2\\%~3
	set rd=%t%
)
echo fp1: _%fp1%_ fp2: _%fp2%_

for /F "usebackq tokens=1 delims=" %%i in (`bin\dircmp.exe ^"%fp1%^" ^"%fp2%^"`) do (
	set sline=%%i
	set opc=%sline:~0,4%
	set opc1=!opc:~0,1!
	set opc2=!opc:~1,3!
	set fn=%sline:~5%


	if [!opc1!] EQU [D] (
		if [!opc2!] EQU [Mis] (
			echo rmdir ^"!fp2!\!fn!^" /S /Q>>temp.bat
		)
		if [!opc2!] EQU [New] (
			echo call test-sub1 %1 %2 ^"%rd%\!fn!^">>temp.bat
		)
		if [!opc2!] EQU [Exi] (
			echo call test-sub1 %1 %2 ^"%rd%\!fn!^">>temp.bat
		)
	)
	if [!opc1!] EQU [F] (
		echo robocopy ^"%fp1%^" ^"%fp2%^" /Z /J /DCOPY:DAT /NOOFFLOAD /R:0 /NS /NC /NFL /NDL /NP>>temp.bat
	)
)
