@echo off
cd c:\projects

del qucs\PHILC*.*
del qucs\asco*.*
del qucs-s\PHILC*.*
del qucs-s\asco*.*
rem del qucs\netlist*.*
rem del qucs\log*.*

java -jar "c:\Users\Donald Chitester\bfg.jar" --no-blob-protection -D \qucs\PHILC*.* .git
java -jar "c:\Users\Donald Chitester\bfg.jar" --no-blob-protection -D \qucs\asco*.* .git
java -jar "c:\Users\Donald Chitester\bfg.jar" --no-blob-protection -D \qucs\netlist*.* .git
java -jar "c:\Users\Donald Chitester\bfg.jar" --no-blob-protection -D \qucs\log*.* .git

java -jar "c:\Users\Donald Chitester\bfg.jar" --no-blob-protection -D qucs-s\PHILC*.* .git
java -jar "c:\Users\Donald Chitester\bfg.jar" --no-blob-protection -D qucs-s\asco*.* .git
java -jar "c:\Users\Donald Chitester\bfg.jar" --no-blob-protection -D qucs-s\netlist*.* .git
java -jar "c:\Users\Donald Chitester\bfg.jar" --no-blob-protection -D \RW\** .git


python.exe c:\projects\python-win\pybackup.py

:erre
pause
