import java.nio.file.Paths
import java.util.function.Consumer

import scala.collection.JavaConverters.asScalaIteratorConverter
import scala.collection.mutable.{ TreeSet => MSSet }

import javafx.{ concurrent => jfxc }
import scalafx.concurrent.Task

class ActivityRecord(val rt: String) {
	// TextWrap.println("ActivityRecord")
	var cnl_cnt:Int = -1;
	var ts = new MSSet[String]()
	val cn = new ChangeNotifier(
		rt,
		new Consumer[ChangeNotifier.CNI] {
			override def accept(cne:ChangeNotifier.CNI):Unit = {
				val sfp = DSubs.resolve(rt, cne.path)
				// var lm: String = ""
				// cne.action match {
				// 	case WC.CNE_ADDED => lm += "Added"
				// 	case WC.CNE_REMOVED => lm += "Removed"
				// 	case WC.CNE_MODIFIED => lm += "Modified"
				// 	case WC.CNE_RENAMED_OLD_NAME => lm += "Renamed - old name"
				// 	case WC.CNE_RENAMED_NEW_NAME => lm += "Renamed - new name"
				// 	case _ => lm += "?"
				// }
				// lm += " "
				// lm += cne.path
				// lm += " "
				if (cne.isdir && cne.action == WC.CNE_MODIFIED) {
					ActivityRecord.this.synchronized {
						ts += cne.path
						// lm += cne.path
					}
				} else {
					val prt = Paths.get(rt)
					val pfp = Paths.get(sfp).getParent()
					val np = prt.relativize(pfp)
					ActivityRecord.this.synchronized {
						ts += np.toString()
						// lm += np.toString()
					}
				}
				ActivityRecord.this.update()
				// System.out.println(lm);
			}
		}
	)

	def update():Unit = {
		if(cnl_cnt != ts.size) {
			var s: String = ""
			for (rd <- ts) {
				s += (" " + rd) + '\n';
			}
			DirSyncApp.onFX {
				if (DirSyncApp.cnList != null) {
					DirSyncApp.cnList.text.update(s)
				}
			}
			cnl_cnt = ts.size
		}
	}
}

