pushd %~d0\Projects\go
call %~d0\.bat\plaunch.bat bin\dirsync.exe
popd
pause
%~d0\.bat\dirsync.bat