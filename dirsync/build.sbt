import sbt.IvyPaths

libraryDependencies += "com.nativelibs4java" % "bridj" % "0.7.0"

scalaVersion := "2.12.1"

lazy val root = (project in file("."))
  .settings(
    name := "Test1",
    scalaVersion := "2.12.1"
  )

// oneJarSettings///

// scalaHome := Some(file("\\Projects\\lib\\scala"))
// unmanagedJars in Compile ++= scalaInstance.value.jars

scalacOptions ++= Seq("-deprecation")

javaHome := Some(file("\\Programs\\jDKx64"))
javacOptions ++= Seq("-Xlint:unchecked")

sourcesInBase := true
scalaSource in Compile := baseDirectory.value
javaSource in Compile := baseDirectory.value

ivyPaths := new IvyPaths(file("\\Projects\\DirSyncApp"), Some(file("\\Projects\\DirSyncApp\\.ivy2")))

lazy val copy_flash = taskKey[Unit]("Backups flash drive to flash drive")

copy_flash := {
  DirSync.main(Array(sys.env.get("FLASH0").get + "\\", sys.env.get("CLONE_DIR").get))
}
