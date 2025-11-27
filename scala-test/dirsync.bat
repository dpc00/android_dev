Ker@echo on
setlocal enabledelayedexpansion
cd \Projects\scala-test
rem \.bat\plaunch build\scripts\scala-test.bat
set arg1=
set arg2=
set arg3=
set arg4=
if not "%FLASH0%"=="" set arg1=%FLASH0%\
if not "%FLASH1%"=="" set arg2=%FLASH1%\%CLONE_DIR%
if not "%FLASH2%"=="" set arg3=%FLASH2%\%CLONE_DIR%
if not "%FLASH3%"=="" set arg4=%FLASH3%\%CLONE_DIR%

rem E:\Programs\jDKx64\bin\javaw.exe
rem -agentlib:jdwp=transport=dt_socket,suspend=y,address=localhost:60383
rem -Dfile.encoding=UTF-8
rem -Xbootclasspath/a:E:\Programs\eclipse\plugins\org.scala-lang.scala-library_2.11.8.v20160304-115712-1706a37eb8.jar;
rem E:\Programs\eclipse\plugins\org.scala-lang.scala-reflect_2.11.8.v20160304-115712-1706a37eb8.jar
rem -classpath E:\Projects\scala-test\build\classes\main;
rem E:\Programs\gradle-3.4.1\.gradle\caches\modules-2\files-2.1\com.nativelibs4java\bridj\0.7.0\461c40ed578c92106579e370838ed4e224d0289e\bridj-0.7.0.jar;
rem E:\Programs\gradle-3.4.1\.gradle\caches\modules-2\files-2.1\org.scalafx\scalafx_2.11\8.0.102-R11\6691d914199aff2bef654c73388c14f1f6ca4161\scalafx_2.11-8.0.102-R11.jar DirSyncApp E:\ F:\FQZGJQYA

rem java -cp \Projects\lib\bridj-0.7.0-windows-only.jar;\Programs\scala\lib\scala-library-2.12.1.jar;\Programs\scala\lib\scala-reflect-2.12.1.jar;\Projects\lib\scalafx_2.11-8.0.102-R11.jar;\Projects\scala-test\build\libs\scala-test.jar DirSyncApp %arg1% %arg2% %arg3% %arg4%

set lib1=\Projects\lib\bridj-0.7.0-windows-only.jar
rem set lib2=\Programs\scala\lib\scala-library-2.12.1.jar
rem set lib2=\Programs\eclipse\plugins\org.scala-lang.scala-library_2.11.8.v20160304-115712-1706a37eb8.jar
set lib2=\Programs\gradle-3.4.1\.gradle\caches\modules-2\files-2.1\org.scala-lang\scala-library\2.11.8\ddd5a8bced249bedd86fb4578a39b9fb71480573\scala-library-2.11.8.jar
rem set lib3=\Programs\scala\lib\scala-reflect-2.12.1.jar
rem set lib3=\Programs\eclipse\plugins\org.scala-lang.scala-reflect_2.11.8.v20160304-115712-1706a37eb8.jar
set lib3=\Programs\gradle-3.4.1\.gradle\caches\modules-2\files-2.1\org.scala-lang\scala-reflect\2.11.8\b74530deeba742ab4f3134de0c2da0edc49ca361\scala-reflect-2.11.8.jar
rem set lib4=\Projects\lib\scalafx_2.11-8.0.102-R11.jar
set lib4=\Programs\gradle-3.4.1\.gradle\caches\modules-2\files-2.1\org.scalafx\scalafx_2.11\8.0.102-R11\6691d914199aff2bef654c73388c14f1f6ca4161\scalafx_2.11-8.0.102-R11.jar
set lib5=\Projects\scala-test\build\libs\scala-test.jar
set libs=%lib1%;%lib2%;%lib3%;%lib4%;%lib5%

java -cp %libs% DirSyncApp %arg1% %arg2% %arg3% %arg4%

