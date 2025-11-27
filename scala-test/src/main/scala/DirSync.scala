import java.nio.file.FileSystem
import java.nio.file.FileSystems
import java.nio.file.Files
import java.util.function.Consumer
import java.util.HashMap
import System.nanoTime

import scala.collection.JavaConverters.asScalaSetConverter
import scala.collection.mutable.{ MutableList => List, Set }

// import de.sciss.swingplus._

object DSList extends List[DirSync] {
	var p1: String = null
	var ar: ActivityRecord = null
}

class DirSync(val p1: String, val p2: String) {
	val fs: FileSystem = FileSystems.getDefault()
	var il = 0

	def profile[R](code: => R, t: Long = nanoTime) = (code, nanoTime - t)

	def dUpdate(cd1: String): Unit = {
		DirSyncApp.onFX {
			DirSyncApp.lbl3.text.update("scanning " + cd1)
		}
	}
	
	def dClear(): Unit = {
		DirSyncApp.onFX {
			DirSyncApp.lbl3.text.update("")
		}
	}

	def sepThread(c: => Unit):Unit = {
			new Thread {
				override def run():Unit = {
					DSubs.synchronized {
						c
					}
				}
			}.start()
	}

	def syncDir(srt: String, drt: String, rd: String = "", ne:Boolean = false): Unit = {
		if (DirSyncApp.cancelled) return
		var cd1 = DSubs.resolve(srt, rd)
		var cd2 = DSubs.resolve(drt, rd)

		if (Kernel32.dir_exists(cd1)) {
			if (!Kernel32.dir_exists(cd2)) {
				Files.createDirectories(fs.getPath(cd2))
			}

			val sContents = new Contents(cd1)
			val dContents = new Contents(cd2)

			val ops = new OpLists(sContents, dContents, ne)

			dUpdate(cd1)

			// operations
			if(ops.dFiles!=null) {
				ops.dFiles.forEach(
					new Consumer[DE] {
						override def accept(di:DE):Unit = {
							if(DSubs.fileDelete(cd1, cd2, di.fname)) {
								DStats.bdel += di.size
							}
						}
					}
				)
			}

			if(ops.dDirs!=null) {
				ops.dDirs.forEach(
					new Consumer[DE] {
						override def accept(di:DE):Unit = {
							DSubs.dirDelete(cd1, cd2, di.fname)
						}
					}
				)
			}

			if(ops.cFiles!=null) {
				ops.cFiles.forEach(
					new Consumer[DE] {
						override def accept(si:DE):Unit = {
							if (DSubs.fileCopy(cd1, cd2, si.fname)) {
								DStats.bcopy += si.size
							}
						}
					}
				)
			}

			if(ops.cDirs != null) {
				ops.cDirs.forEach(
					new Consumer[DE] {
						override def accept(si:DE):Unit = {
							syncDir(cd1, cd2, si.fname)
						}
					}
				)
			}

			DStats.filecnt += ops.scf.size
			DStats.update()

		}
		DStats.dircnt += 1
		DStats.update()
	}

	def runPartialSync(): Unit = {
		val ts = DSList.ar.ts
		for (rd <- ts) {
			syncDir(p1, p2, rd, true)
		}
		dClear()
	}

	def runSync(): Unit = {
		syncDir(p1, p2, "")
		dClear()
	}
}
