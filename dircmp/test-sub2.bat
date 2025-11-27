setlocal
rem src_rt: %1
rem dst_rt: %2
rem rd: %3
rem oc: %4
rem subdir or file: %5

set opc=%4
set opc1=%opc:~0,1%
set opc2=%opc:~1,3%

set t=%3

if [%t:~-1,1%] EQU [\] (
	set fp1=%1%3
	set fp2=%2%3
	set rd=%3
)
if [%t:~-1,1%] NEQ [\] (
	set fp1=%1%\%3
	set fp2=%2%\%3
	set rd=%3\
)

if [%opc1%] EQU [D] (
	if [%opc2%] EQU [Mis] (
		echo rmdir %fp2%\%5 /S /Q>>temp.bat
	)
	if [%opc2%] EQU [New] (
		echo call test-sub1 %1 %2 %rd%%5>>temp.bat
	)
	if [%opc2%] EQU [Exi] (
		echo call test-sub1 %1 %2 %rd%%5>>temp.bat
	)
)
if [%opc1%] EQU [F] (
	echo robocopy %fp1% %fp2% /Z /J /DCOPY:DAT /NOOFFLOAD /R:0 /NS /NC /NFL /NDL /NP>>temp.bat
)
