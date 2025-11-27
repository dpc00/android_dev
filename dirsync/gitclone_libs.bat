@echo on

set libdir1=%~d0\Projects\lib
set libdir2=%~d0\Projects\DirSyncApp\lib

set libs=%libs%;%libdir1%\JavaEWAH-1.1.6.jar
set libs=%libs%;%libdir1%\jsch-0.1.54.jar
set libs=%libs%;%libdir1%\jzlib-1.1.3.jar
set libs=%libs%;%libdir1%\leveldbjni-all-1.8.jar
set libs=%libs%;%libdir1%\org.eclipse.jgit-4.9.0.201710071750-r.jar
set libs=%libs%;%libdir1%\org.eclipse.jgit.ui-4.8.0.201706111038-r.jar
set libs=%libs%;%libdir1%\org.eclipse.jgit.console-3.7.1.201504261725-r.jar
set libs=%libs%;%libdir1%\slf4j-api-1.7.25.jar
set libs=%libs%;%libdir1%\slf4j-simple-1.7.25.jar
set libs=%libs%;%libdir1%\zip4j-1.3.2.jar
set libs=%libs%;%libdir2%\DirSyncApp.jar

java -cp %libs% %opts% org.ds.app.Main2 %args%

