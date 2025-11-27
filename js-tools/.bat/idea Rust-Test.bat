setlocal enabledelayedexpansion
set path=%path%;%~d0\Programs\idea\bin;%~d0\.bat
cd %~d0\Projects
plaunch.bat idea.bat !FLASH0!\Projects\Rust-Test