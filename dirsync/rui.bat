set lib1=\Projects\lib\bridj-0.7.0-windows-only.jar
set lib2=\Programs\gradle-3.4.1\.gradle\caches\modules-2\files-2.1\org.scala-lang\scala-library\2.11.8\ddd5a8bced249bedd86fb4578a39b9fb71480573\scala-library-2.11.8.jar
set lib3=\Programs\gradle-3.4.1\.gradle\caches\modules-2\files-2.1\org.scala-lang\scala-reflect\2.11.8\b74530deeba742ab4f3134de0c2da0edc49ca361\scala-reflect-2.11.8.jar
set lib4=\Programs\gradle-3.4.1\.gradle\caches\modules-2\files-2.1\org.scalafx\scalafx_2.11\8.0.102-R11\6691d914199aff2bef654c73388c14f1f6ca4161\scalafx_2.11-8.0.102-R11.jar
set lib5=\Projects\DirSyncApp\build\libs\DirSyncApp.jar
set lib6=\Projects\lib\reflection-ui-3.0.3\target\reflection-ui-3.0.3.jar
set lib7=\Projects\lib\reflection-ui-3.0.3\target\dependency\classmate-1.1.0.jar
set lib8=\Projects\lib\reflection-ui-3.0.3\target\dependency\commons-lang3-3.2.jar
set lib9=\Projects\lib\reflection-ui-3.0.3\target\dependency\filters-2.0.235.jar
set lib10=\Projects\lib\reflection-ui-3.0.3\target\dependency\guava-18.0.jar
set lib11=\Projects\lib\reflection-ui-3.0.3\target\dependency\paranamer-2.7.jar
set lib12=\Projects\lib\reflection-ui-3.0.3\target\dependency\swing-worker-1.1.jar
set lib13=\Projects\lib\reflection-ui-3.0.3\target\dependency\swingx-1.6.1.jar

set libs=%lib1%;%lib2%;%lib3%;%lib4%;%lib5%;%lib7%;%lib8%;%lib9%;%lib10%;%lib11%;%lib12%;%lib13%
@rem java -cp %libs% DirSyncApp %arg1% %arg2% %arg3% %arg4%


java -cp %libs% -jar \Projects\lib\reflection-ui-3.0.3\target\reflection-ui-3.0.3.jar