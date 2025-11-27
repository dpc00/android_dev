setlocal enabledelayedexpansion
set path=%path%;%~d0\.bat
cd %~d0\Projects
plaunch.bat eclipse.exe -data !FLASH0!\Projects\eclipse-workspace
