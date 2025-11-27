import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream

import java.io.IOException
import java.nio.channels.FileChannel

import java.nio.file.FileSystem
import java.nio.file.FileSystems
import java.nio.file.FileVisitResult
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.nio.file.SimpleFileVisitor
import java.nio.file.attribute.BasicFileAttributes
import java.nio.file.StandardCopyOption._
import scala.util.control.NonFatal
import scala.util.{Try, Success, Failure}

object DSubs {
	val fs: FileSystem = FileSystems.getDefault()
	var cd: String = ""
	var ncd: String = ""

	@inline
	def twp(s1: String): Unit = {
		TextWrap.println("   " + s1)
	}

	@inline
	def ldUpdate(m: String): Unit = {
		DSubs.synchronized {
			if (!(ncd == cd)) {
				cd = ncd
				TextWrap.println("Dir " + cd)
			}
			TextWrap.println("   " + m)
		}
	}

	@inline
	def resolve(cd2: String, f1: String): String = {
		var fp2 = cd2
		if (f1.length > 0) {
			if (!fp2.endsWith("\\") && !fp2.endsWith("/")) {
				fp2 = fp2 + "\\"
			}
			fp2 = fp2 + f1
		}
		// twp(cd2 + " + '" + f1 + "' resolved to " + fp2)
		return fp2
	}

	@inline
	def delete_file(fp2: String): Try[Int] = {
		Try {
			if (DirSyncApp.cancelled) throw new InterruptedException("abort in delete_file")
			else {
				Kernel32.delete_file(fp2)
			}
		}
	}

	@inline
	def remove_dir(fp2: String): Try[Int] = {
		Try {
			if (DirSyncApp.cancelled) throw new InterruptedException("abort in remove_dir")
			else {
				Kernel32.remove_directory(fp2)
				// DosCmd.exec1("rmdir /s /q " + fp2)
			}
		}
	}

	class DDFV extends SimpleFileVisitor[Path] {
		override def visitFile(file: Path, attrs: BasicFileAttributes): FileVisitResult = {
			if (DirSyncApp.cancelled) return FileVisitResult.TERMINATE
			delete_file(file.toString()) match {
				case Success(rv) =>
					ncd = file.getParent().toString()
					ldUpdate("deleted file " + file.getFileName().toString())
					DStats.bdel += attrs.size
					DStats.update()
					FileVisitResult.CONTINUE
				case Failure(e) =>
					ncd = file.getParent().toString()
					ldUpdate("failed to delete file " + file.getFileName().toString())
					ldUpdate("   ->" + e.toString())
					FileVisitResult.TERMINATE					
			}
		}
		override def postVisitDirectory(dir: Path, e: IOException): FileVisitResult = {
			if (DirSyncApp.cancelled) return FileVisitResult.TERMINATE
			else if (e != null) {
				ncd = dir.getParent().toString()
				ldUpdate("   ->" + e.toString())
				return FileVisitResult.TERMINATE				
			} 
			else {
				remove_dir(dir.toString()) match {
					case Success(_) =>
						ncd = dir.getParent().toString()
						ldUpdate("deleted dir " + dir.getFileName().toString())
						FileVisitResult.CONTINUE
					case Failure(e) =>
						ncd = dir.getParent().toString()
						ldUpdate("failed to delete dir " + dir.getFileName().toString())
						ldUpdate("   ->" + e.toString())
						FileVisitResult.TERMINATE
				}
			}
		}
	}

	@inline
	def copy_file1(fp1:String, fp2:String): Try[Int] = {
		Try {
			if (DirSyncApp.cancelled) throw new InterruptedException("abort in copy_file")
			else {
				Kernel32.copy_file(fp1, fp2)
			}
		}
	}

	@inline
	def copy_file2(fp1:String, fp2:String): Try[Int] = {
		Try {
			if (DirSyncApp.cancelled) throw new InterruptedException("abort in copy_file")
			else {
				val rv = DosCmd.exec1("copy " + fp1 + " " + fp2)
				if(rv != 0) 0 else 1
			}
		}
	}

	@inline
	def copy_file3(fp1:String, fp2:String): Try[Int] = {
		Try {
			if (DirSyncApp.cancelled) throw new InterruptedException("abort in copy_file")
			else {
				val tp = Files.copy(Paths.get(fp1), Paths.get(fp2), REPLACE_EXISTING, COPY_ATTRIBUTES);
				if(tp != null) 1 else 0
			}
		}
	}

	def copy_file4(fp1:String, fp2:String) : Try[Int] = {
		Try {
			if (DirSyncApp.cancelled) throw new InterruptedException("abort in copy_file")
			else {
				val in:File = new File(fp1)
				val out:File = new File(fp2)
				val fis:FileInputStream = new FileInputStream(in)
				val fos:FileOutputStream = new FileOutputStream(out)
				val inChannel:FileChannel = fis.getChannel()
				val outChannel:FileChannel  = fos.getChannel()

				try {
					// inChannel.transferTo(0, inChannel.size(), outChannel); //
					// original -- apparently has trouble copying large files on Windows

					// magic number for Windows, 64Mb - 32Kb)
					val maxCount:Int = (64 * 1024 * 1024) - (32 * 1024)
					val size:Long = inChannel.size()
					var position:Long = 0
					while (position < size) {
						position += inChannel.transferTo(position, maxCount, outChannel)
					}
					1
				}
				finally {
					if (fis != null) fis.close()
					if (fos != null) fos.close()
					if (inChannel != null) inChannel.close()
					if (outChannel != null) outChannel.close()
					Files.setLastModifiedTime(out.toPath(), Files.getLastModifiedTime(in.toPath()))
				}

			}
		}
	}

	def fileCopy(cd1: String, cd2: String, f1: String): Boolean = {
		if (DirSyncApp.cancelled) return false
		var fp1 = resolve(cd1, f1)
		var fp2 = resolve(cd2, f1)

		copy_file4(fp1, fp2) match {
			case Success(_) =>
				ncd = cd1
				ldUpdate("copied " + f1)
				true
			case Failure(e) =>
				ncd = cd1
				ldUpdate("failed to copy " + f1)
				ldUpdate("   ->" + e.toString())
				false
		}
	}

	def fileDelete(cd1: String, cd2: String, f1: String):Boolean = {
		if (DirSyncApp.cancelled) return false
		val fp2 = resolve(cd2, f1)

		delete_file(fp2) match {
			case Success(_) =>
				ncd = cd1
				ldUpdate("deleted file " + f1)
				true
			case Failure(e) =>
				ncd = cd1
				ldUpdate("failed to delete file " + f1)
				ldUpdate("   ->" + e.toString())
				false
		}
	}

	def dirDelete(cd1: String, cd2: String, d1: String): Unit = {
		if (DirSyncApp.cancelled) return
		val directory = fs.getPath(cd2, d1)
		Files.walkFileTree(directory, new DDFV())
	}
}