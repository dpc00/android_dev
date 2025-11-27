import java.io.PrintStream
import java.util.StringTokenizer

import scala.collection.mutable.{ MutableList => List }

object TextWrap extends PrintStream(Console.out) {
	val delims = "\\/,;-%&$![]{}|<>? "
	def minNumLinesWrap(text: String, lw: Int): List[String] = {
		var sa: List[String] = List[String]()
		var cl: String = null
		val tokenizer: StringTokenizer = new StringTokenizer(text, delims, true)
		var lw2 = lw
		while (tokenizer.hasMoreTokens) {
			val tok: String = tokenizer.nextToken
			if (tok.length + (if (cl != null) cl.length else 0) >= lw2 - 1 && !(tok.length == 1 && (delims contains tok(0)) && tok != " ")) {
				if (cl != null) {
					sa += cl.trim
					lw2 = lw - 3
				}
				cl = tok.trim
			} else {
				cl = if (cl == null) tok else cl + tok
			}
		}
		if ((if (cl != null) cl.length else 0) > 0) sa += cl
		sa
	}

	override def print(s1: String): Unit = {
		val sa: Array[String] = minNumLinesWrap(s1, 80).toArray
		var s2: String = ""
		for (i <- 0 to sa.size - 1) {
			if (i > 0) {
				s2 += "\n   " + sa(i)
			} else s2 += sa(i)
		}
		if (DirSyncApp.taEvents != null) {
			DirSyncApp.onFX(
				{ DirSyncApp.taEvents.appendText(s2 + "\n") }
			)
		}
		// Console.print(s2)
	}

	override def println(s: String = ""): Unit = {
		print(s)
		// Console.println()
	}
}