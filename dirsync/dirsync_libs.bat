@echo on

set libdir1=%~d0\Projects\lib
set libdir2=%~d0\Projects\DirSyncApp\lib

set libs=%libs%;%libdir1%\JavaEWAH-1.1.6.jar
set libs=%libs%;%libdir1%\jsch-0.1.54.jar
set libs=%libs%;%libdir1%\jzlib-1.1.3.jar
set libs=%libs%;%libdir1%\bridj-0.7.0-windows-only.jar
rem set libs=%libs%;%libdir1%\leveldbjni-all-1.8.jar
set libs=%libs%;%libdir1%\slf4j-api-1.7.25.jar
set libs=%libs%;%libdir1%\slf4j-simple-1.7.25.jar
set libs=%libs%;%libdir1%\zip4j-1.3.2.jar
set libs=%libs%;%libdir2%\DirSyncApp.jar

java -cp %libs% %opts% org.ds.app.DirSyncApp %args%

