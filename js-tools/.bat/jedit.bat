setlocal enabledelayedexpansion
cd \Projects\DirSyncApp
rem \.bat\plaunch.bat gradle.bat jEdit %1 %2 %3 %4 %5
\.bat\plaunch !JAVA_HOME!\bin\javaw.exe -jar !FLASH0!\PortableApps\jEditPortable\App\jEdit\jedit.jar -settings=!FLASH0!\portableapps\jeditportable\data\.jedit %1 %2 %3 %4 %5
