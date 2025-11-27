setlocal enabledelayedexpansion
:start
cd \Projects\scala-test
call \.bat\plaunch.bat java -cp ..\lib\bridj-0.7.0-windows-only.jar;..\lib\scala\lib\*;build\classes\main DirSync !FLASH0!\ !FLASH1!\!CLONE_DIR! 
pause
goto :start