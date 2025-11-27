for /F "usebackq tokens=1" %%d in (`type dlllist.txt`) do (
	copy %windir%\System32\%%d E:\DLLs
	)