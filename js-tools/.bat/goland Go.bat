setlocal enabledelayedexpansion
set path=%path%;%~d0\Programs\GoLand\bin;%~d0\.bat
cd %~d0\Projects
plaunch.bat start goland.bat !FLASH0!\Projects\Go
