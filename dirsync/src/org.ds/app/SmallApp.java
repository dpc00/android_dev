package org.ds.app;

import java.util.concurrent.TimeUnit;

import org.ds.l3.DSRT;

import javafx.application.Application;
import javafx.stage.Stage;

public class SmallApp extends Application {
	public static int apid;
	public static SmallApp it;
	public boolean started;

	public SmallApp() {
		SmallApp.it = this;
		apid++;
	}

	public void start(Stage stage) {
		System.out.println("start");
		this.started = true;
	}

	public void init() throws Exception {
		System.out.println("init");
	}

	public void stop() throws Exception {
		System.out.println("stop");
		DSRT.execService.shutdown();
		System.out.println("await DSRT execService shutdown");
		try {
			DSRT.execService.awaitTermination(5L, TimeUnit.SECONDS);
		} catch (InterruptedException e) {
			System.out.println(e.toString());
		}
		DSRT.execService.shutdownNow();
		while (!DSRT.execService.isShutdown()) Thread.yield();
		System.out.println("DSRT execService shutdown");
	}

	public String toString() {
		return "SmallApp" + apid;
	}
}
