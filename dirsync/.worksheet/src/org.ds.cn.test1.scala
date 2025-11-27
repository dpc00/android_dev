package org.ds.cn

import org.ds.l4._

object test1 {;import org.scalaide.worksheet.runtime.library.WorksheetSupport._; def main(args: Array[String])=$execute{;$skip(101); 
	val ar:ActivityRecord = new ActivityRecord("");System.out.println("""ar  : org.ds.cn.ChangeRecord = """ + $show(ar ));$skip(44);
  println("Welcome to the Scala worksheet");$skip(93); 
	Option[(DSLst, FList)](ar.cnl.get("test")) match {
		case Some((dsl:DSLst, fl:FList)) =>
	}}
}
