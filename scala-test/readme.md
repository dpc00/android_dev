# Scala Dir Sync App

This project is an attempt at a translation to scala with java of a dir synchronization program written in python (py-test repo) which itself was an attempt to translate from javascript (tools repo).

The operative code itself is a basically simple directory tree walk implementation.

It uses BridJ with windows directory calls for speed.  It uses BridJ and windows file notification services also.  The code turned out quite good/interesting but was a difficult exercise and there are no plans to try to repeat the error.

The UI uses scalafx.

It is built using Gradle.  Uses Scala 2.11.8 for compatibility with scalafx.  Uses BridJ 0.7.  The Gradle usage is very flaky.

The learning process and complexity of using scala, scalafx, and BridJ was way too time-consuming.  

To run the command line accepts source-dir and series of target-dirs.  Various run details are in dirsync.bat and build.gradle.

A "plaunch" bat file exists on my flash drive which assigns to environment variables based on custom volume labels so that by the time dirsync.bat is executed FLASH0 through FLASH3 and CLONE_DIR variables are already set:

```
for /f "usebackq tokens=1,2 skip=1" %%i in (`wmic VOLUME where drivetype^=2 get label^,driveletter`) do (
	if "%%j"=="KINGSTON" set FLASH0=%%i
	if "%%j"=="CODE1" set FLASH1=%%i
	if "%%j"=="CODE2" set FLASH2=%%i
	if "%%j"=="CODE3" set FLASH3=%%i
)
if "%FLASH0%"=="" exit
```

