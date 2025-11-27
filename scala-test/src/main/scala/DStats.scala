import java.text.NumberFormat
import java.util.Locale

object DStats {
	@volatile var bcopy: Long = 0
	@volatile var bdel: Long = 0
	@volatile var dircnt: Int = 0
	@volatile var filecnt: Int = 0

	def update(): Unit = {
		DirSyncApp.onFX {
			val nf = NumberFormat.getNumberInstance(Locale.US)
			DirSyncApp.lbl2(0).text.update("Bytes copied: " + nf.format(DStats.bcopy))
			DirSyncApp.lbl2(1).text.update("Bytes deleted: " + nf.format(DStats.bdel))
			DirSyncApp.lbl2(2).text.update("Dirs scanned: " + nf.format(DStats.dircnt))
			DirSyncApp.lbl2(3).text.update("Files checked: " + nf.format(DStats.filecnt))
		}
	}
}

