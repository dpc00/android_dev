import scala.sys.process._

object DosCmd {
	def exec1(s:String):Int = {
		Console.withOut(TextWrap) {
			Console.withErr(TextWrap) {
				("cmd /c " + s).!
			}
		}
	}
	def exec2(s:String):String = {
		("cmd /c " + s).!!
	}
}