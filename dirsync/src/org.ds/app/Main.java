package org.ds.app;

import java.util.ArrayList;
import java.util.Collections;
import java.util.function.Predicate;

import org.ds.event.DSEvent;
import org.ds.l3.DSRT;
import org.ds.l4.DSList;
import org.ds.l4.DSTI;
import org.ds.l4.DirSyncRunner;
import org.ds.types.RD;
import org.ds.types.VL;

import javafx.application.Application;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;

public class Main {
	public static ArrayList<RtData> parms = ParamReader.build(new Predicate<VL>() {
		@Override
		public boolean test(VL vl) {
			return vl.s.startsWith("CODE") && Integer.valueOf(vl.s.substring(4).trim()) == 0;
		}
	}, new Predicate<VL>() {
		@Override
		public boolean test(VL vl) {
			return vl.s.startsWith("CODE") && Integer.valueOf(vl.s.substring(4).trim()) > 0;
		}
	});
	public static DSList dslist = new DSList().build2(parms);

	public static void runFullSyncs() {
		for (DSTI te : dslist.d) {
			if (te.runner == null) {
				te.runner = new DirSyncRunner(te, Collections.singletonList(new RD("")), true);
				te.runner.start();
			} else {
				te.runner.restart(Collections.singletonList(new RD("")), true);
			}
		}
	}

	public static ChangeListener<DSEvent> eh1 = new ChangeListener<DSEvent>() {
		@Override
		public void changed(ObservableValue<? extends DSEvent> observable, DSEvent oldValue, DSEvent cur) {
			String en = cur.getEventType().getName();
			String s = cur.d.rd.s;
			switch (en) {
				case "SCANNING":
					break;
				case "ENDSCAN":
					break;
				default:
					System.out.println(en);
			}
		}
	};

	public static void main(String[] args) {
		Runnable r = new Runnable() {
			public void run() {
				Application.launch(SmallApp.class, new String[]{});
			}
		};
		DSRT.execService.submit(r);

		while (SmallApp.it == null) {
			System.out.println("SmallApp/it is " + (SmallApp.it == null ? "nil" : "non-nil"));
			try {
				Thread.sleep(500);
			} catch (InterruptedException e) {
			}
		}
		while (!SmallApp.it.started) {
			System.out.println(SmallApp.it + " is not started");
			try {
				Thread.sleep(500);
			} catch (InterruptedException e) {
			}
		}

		for (DSTI te : dslist.d) {
			te.ds.evntprop.addListener(eh1);
		}

		System.out.println("runFullSyncs");
		runFullSyncs();

		for (DSTI te : dslist.d) {
			while (te.runner == null) {
				System.out.println(te.runner + " is nil");
				try {
					Thread.sleep(500);
				} catch (InterruptedException e) {
				}
			}
		}
		for (DSTI te : dslist.d) {
			while (te.runner.notStarted()) {
				System.out.println(te.runner + " is not started");
				try {
					Thread.sleep(500);
				} catch (InterruptedException e) {
				}
			}
		}
		for (DSTI te : dslist.d) {
			while (te.runner.isntDone()) {
//				System.out.println(te.runner + " isn't done");
				try {
					Thread.sleep(3000);
				} catch (InterruptedException e) {
				}
			}
		}
		for (DSTI te : dslist.d) {
			te.ds.evntprop.removeListener(eh1);
		}
	}
}
