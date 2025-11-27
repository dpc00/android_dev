import java.time.Instant
import java.util.{Timer, TimerTask}

import javafx.util.Duration
import javafx.concurrent.Worker.State._

import scala.collection.mutable.{ MutableList => List }
import scala.concurrent.{Await, Future}
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.duration.DurationInt
import scala.language.postfixOps
import scala.util.{Failure, Success}

import scalafx.Includes._
import scalafx.application.JFXApp
import scalafx.application.JFXApp.PrimaryStage
import scalafx.application.Platform
import scalafx.concurrent.{ScheduledService, Service, Task, WorkerStateEvent}
import scalafx.concurrent.Worker
import scalafx.event.ActionEvent
import scalafx.geometry.Insets
import scalafx.scene.Scene
import scalafx.scene.control.{Button, CheckBox, Label, SplitPane, TextArea}
import scalafx.scene.layout.{HBox, VBox}
import scalafx.scene.layout.Priority.Never
import scalafx.scene.paint.Color.White

object DirSyncApp extends JFXApp {

	/**
	 * Run operation `op` on FX application thread and wait for completion.
	 * If the current thread is the FX application, the operation will be run on it.
	 *
	 * @param op operation to be performed.
	 */
	def onFX(op: => Unit): Unit = {
		if (Platform.isFxApplicationThread) {
			op
		} else {
			Platform.runLater { op }
		}
	}

	var cancelled:Boolean = false

	val sp1 = new SplitPane

	var lbl1: List[Label] = new List[Label]()
	var lbl2: List[Label] = new List[Label]()

	val b1 = new Button("Sync")
	b1.tooltip = "Full Sync"
	val b2 = new Button("Sync")
	b2.tooltip = "Partial Sync"
	val b3 = new Button("Abort")
	b3.tooltip = "Abort task"

	var cnList: TextArea = new TextArea()
	cnList.tooltip = "Change notification directories"
	var taEvents: TextArea = new TextArea()
	taEvents.tooltip = "Changes"
	var lbl3: Label = new Label()
	lbl3.tooltip = "Current directory being checked"

	val cb1:CheckBox = new CheckBox("Windows Dir Scan (Java Dir Scan)")
	cb1.tooltip = "Use Windows Calls vs. Java nio calls"
	cb1.selected = true
	Contents.option_WDE = true

	def main2(): Unit = {
		val args = parameters.unnamed
		TextWrap.println("=" * 80)
		TextWrap.print(" DirSync program started at " + Instant.now().toString())

		if (args.size < 2) {
			TextWrap.println("Must provide at least two paths. One source and one destination.")
			return
		}
		var args2: List[String] = List(args.toList: _*)

		val p1 = args2(0)
		DSList.p1 = p1
		DSList.ar = new ActivityRecord(DSList.p1)

		TextWrap.println(" with args:")
		args2.foreach { a1 => TextWrap.print(" '" + a1 + "'") }
		args2 = args2.drop(1)

		if (args2.size > 0) {
			args2.map { a2 =>
				DSList += new DirSync(p1, a2)
			}
		}

		lbl1 += new Label("Source:")
		lbl1 += new Label(DSList.p1)
		lbl1 += new Label("Target(s):")
		var tn = 1
		DSList.foreach { ds =>
			lbl1 += new Label(tn + ":  " + ds.p2)
			tn += 1
		}

		lbl2 += new Label("Bytes copied: " + DStats.bcopy)
		lbl2 += new Label("Bytes deleted: " + DStats.bdel)
		lbl2 += new Label("Dirs scanned: " + DStats.dircnt)
		lbl2 += new Label("Files checked: " + DStats.filecnt)

		stage = new PrimaryStage {
			title = "DirSync App"
			scene = new Scene {
				val vbFull = new VBox {
					for (ti <- lbl1) {
						children += ti
					}
					children += b1
					spacing = 4
					padding = Insets(6, 4, 6, 4)
					hgrow = Never
				}
				val vbPartial = new VBox {
					children = List(new Label("Change notification dirs:"), cnList, b2)
					spacing = 4
					padding = Insets(6, 4, 6, 4)
					hgrow = Never
				}
				val vbEvents = new VBox {
					fill = White
					children += new Label("Events:")
					children += taEvents
					spacing = 4
					padding = Insets(6, 4, 6, 4)
					hgrow = Never
				}
				val vbInfo = new VBox {
					for (ti <- lbl2) {
						children += ti
					}
					children += b3
					spacing = 4
					padding = Insets(6, 4, 6, 4)
					minWidth = 400
					hgrow = Never
				}
				val hb1 = new HBox { children = List(vbFull, vbPartial) 
					spacing = 4
					padding = Insets(6, 4, 6, 4)
				}
				val hb2 = new HBox { children = List(vbEvents, vbInfo) 
					spacing = 4
					padding = Insets(6, 4, 6, 4)
				}
				val vb1 = new VBox { children = List(hb1, lbl3, hb2, cb1) 
					spacing = 4
					padding = Insets(6, 4, 6, 4)
				}
				content = vb1
			}
		}
	}

	val f1 = Service[Unit] {
		Task[Unit] {
			DStats.dircnt = 0
			DStats.filecnt = 0
			// DStats.bcopy = 0
			// DStats.bdel = 0
			DStats.update
			val f2 = Future.traverse(DSList)(ds1 => Future(ds1.runSync()))
			f2.onComplete {
				case Success(r) => {
					if(cancelled) {
						TextWrap.println("Full sync aborted.")
					}
					else {
						val f4 = Future.traverse(DSList)(ds1 => Future(ds1.runPartialSync()))
						f4 onComplete {
							case Success(r) => {
								DSList.ar.synchronized {
									DSList.ar.ts.clear()
									DSList.ar.update()
								}
								if(cancelled) {
									TextWrap.println("Partial sync aborted.")
								}
								else {
									TextWrap.println("Partial sync task finished.")
								}
							}
							case Failure(e) => {
								TextWrap.println("Error completing some runPartialSync: " + e.toString)
							}
						}
						Await.ready(f4, 10 minutes)
						TextWrap.println("Full sync task finished.")
					}
				}
				case Failure(e) => {
					TextWrap.println("Error completing full sync: " + e.toString)
				}
			}
			Await.ready(f2, 10 minutes)
		}
	}

	val f3 = Service[Unit] {
		Task[Unit] {
			DStats.dircnt = 0
			DStats.filecnt = 0
			// DStats.bcopy = 0
			// DStats.bdel = 0
			DStats.update
			val f4 = Future.traverse(DSList)(ds1 => Future(ds1.runPartialSync()))
			f4 onComplete {
				case Success(r) => {
					DSList.ar.synchronized {
						DSList.ar.ts.clear()
						DSList.ar.update()
					}
					if(cancelled) {
						TextWrap.println("Partial sync aborted.")
					}
					else {
						TextWrap.println("Partial sync task finished.")
					}
				}
				case Failure(e) => {
					TextWrap.println("Error completing some runPartialSync: " + e.toString)
				}
			}
			Await.ready(f4, 10 minutes)
		}
	}

	val f5 = ScheduledService[Unit] {
		Task[Unit] {
			if(DSList.ar.ts.size > 0) {
				onFX {
					if(!busy()) {
						f3.restart()
					}
				}
			}
		}
	}
	f5.setDelay(Duration.minutes(1))
	f5.setPeriod(Duration.minutes(1))
	// f5.start()
	
	def busy():Boolean = {
		return f1.isRunning || f3.isRunning
	}

	b1.onAction = { e: ActionEvent =>
		if(!busy()) {
			cancelled = false
			f1.restart()
		}
	}

	b2.onAction = { e: ActionEvent =>
		if(!busy()) {
			cancelled = false
			f3.restart()
		}
	}

	b3.onAction = { e: ActionEvent =>
		if(busy()) {
			cancelled = true
		}
	}

	cb1.onAction = { e: ActionEvent =>
		Contents.option_WDE = cb1.selected()
	}

	main2()

	// if (!busy()) {
	//  	f1.start()
	//  }

}