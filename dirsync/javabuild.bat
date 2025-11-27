set ll1=\Projects\lib\groovy-2.5.0-beta-1\lib\ant-1.9.9.jar
set ll2=\Projects\lib\groovy-2.5.0-beta-1\lib\ant-launcher-1.9.9.jar
set JAVA_HOME=%JDK_HOME%
java -cp %ll1%;%ll2% -jar %ll2% -file build.xml jar
