package org.ds.app;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.text.NumberFormat;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Locale;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Future;
import java.util.concurrent.FutureTask;
import java.util.concurrent.ScheduledThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicReference;
import java.util.function.Predicate;
import java.util.stream.Collectors;

import org.ds.cn.ChangeRecord;
//import org.ds.git.GitFunctions;
import org.ds.l2.DosCmd;
import org.ds.l3.CC;
import org.ds.l3.DSRT;
import org.ds.l3.DSubs;
import org.ds.l3.Try;
import org.ds.l4.DSList;
import org.ds.l4.DSTI;
import org.ds.l4.DirSyncRunner;
import org.ds.l4.DirSyncer;
import org.ds.types.RD;
import org.ds.types.VL;
import org.ds.ui.DRow;
import org.ds.ui.DStatsTable;
import org.ds.ui.SRow;
// import org.ds.ui.SStatsTable;
import org.ds.ui.STRow;
import org.ds.ui.TextWrap;

import javafx.application.Application;
import javafx.beans.binding.Bindings;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.concurrent.ScheduledService;
import javafx.concurrent.Task;
import javafx.event.ActionEvent;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.CheckBox;
import javafx.scene.control.Label;
import javafx.scene.control.Separator;
import javafx.scene.control.TextArea;
import javafx.scene.control.ToolBar;
import javafx.scene.control.Tooltip;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;
import javafx.util.Duration;

// import scalafx.concurrent.WorkerStateEvent._

public class DirSyncApp extends Application {
	public static ScheduledThreadPoolExecutor stpe = null;

	public static DirSyncApp it;
	public DSList dsl;
	public CheckBox cbLogAllScans;
	public Label lbCurDir;
	public int maxh;
	public int maxw;
	public int minh;
	public int minw;
	public TextArea taEvents;
	ArrayList<String> args2;
	ArrayList<String> vls2;
	TextArea arList;
	ChangeRecord arTV;
	Button bAbort;
	Button bClearCaches;
	Button bDump;
	Button bFull;
	Button bGitBackup;
	Button bPartial;
	Button bQDir;
	Button bRotate;
	CheckBox cbBackgroundPartial;
	CheckBox cbDirect;
	public DStatsTable stDStats;
	// SStatsTable stSStats;
	HBox hb4;
	ToolBar hbButtons;
	Label lbl0;
	NumberFormat nf;
	Scene scene1;
	VBox vb1;
	VBox vbPartial;
	AtomicReference<DSRT> thar = new AtomicReference<>();
	Future<Void> f2;
	ArrayList<RtData> parms;


	ScheduledService<Void> f5 = new ScheduledService<Void>() {
		protected Task<Void> createTask() {
			return new Task<Void>() {
				protected Void call() {
					if (noneRunning()) {
						runPartialSyncsBackground();
					}
					return null;
				}
			};
		}
	};

	public DirSyncApp() {
		stpe = new ScheduledThreadPoolExecutor(12);
		it = this;
	}

	public static void main(String[] args) {
		Application.launch(DirSyncApp.class, args);
	}

	public void init() throws Exception {
		this.minh = 120;
		this.maxh = 300;
		this.minw = 400;
		this.maxw = 800;

		// public Boolean cancelled;
		this.args2 = new ArrayList<>();
		this.arList = new TextArea();
		this.bAbort = new Button("Abort");
		this.bClearCaches = new Button("Clear Caches");
		this.bDump = new Button("Dump Vars");
		this.bFull = new Button("Full_Scan");
		this.bGitBackup = new Button("Git Backup");
		this.bPartial = new Button("Partial_Scan");
		this.bQDir = new Button("Q-Dir");
		this.bRotate = new Button("Src/Dst");
		this.cbBackgroundPartial = new CheckBox("Periodic Update");
		this.cbDirect = new CheckBox("Windows Find Functions (Java Find Functions)");
		this.cbLogAllScans = new CheckBox("Log dir scans");
		CC.option_WDE = false;
		this.hb4 = new HBox();
		this.hbButtons = new ToolBar();
//		this.hbInfo = new HBox();
		this.lbCurDir = new Label(DirSyncer.empty);
		this.lbl0 = new Label();
		this.nf = NumberFormat.getNumberInstance(Locale.US);
		this.taEvents = new TextArea();
		this.vb1 = new VBox();
		this.vbPartial = new VBox();

		this.bFull.setTooltip(new Tooltip("Full Scan"));
		this.bFull.setOnAction(e -> {
			if (noneRunning()) {
				runFullSyncs();
			}
		});

		this.bGitBackup.setTooltip(new Tooltip("attempts to update all found git repos"));
		this.bGitBackup.setOnAction(event -> {
			if (noneRunning()) {
				runGitBackups();
			}
		});

		this.bPartial.setTooltip(new Tooltip("Partial Scan"));
		this.bPartial.setOnAction(e -> {
			if (noneRunning()) {
				runPartialSyncs();
			}
		});

		this.bAbort.setTooltip(new Tooltip("Abort task(s)"));
		this.bAbort.setOnAction(e -> cancelTasks());
		this.bRotate.setTooltip(new Tooltip("Rotate src/dst"));
		this.bRotate.setOnAction(e -> {
			cancelTasks();
			this.dsl.clearCCs();
			rotate();
		});

		this.bClearCaches.setTooltip(new Tooltip("Prepare for fresh rescan"));
		this.bClearCaches.setOnAction(e -> {
			cancelTasks();
			this.dsl.clearCCs();
		});

		this.bQDir.setTooltip(new Tooltip("run Q-Dir on error dirs"));
		this.bQDir.setOnAction(e -> runQDir());

		this.bDump.setTooltip(new Tooltip("Status of certain structures -> vardump.txt"));
		this.bDump.setOnAction((ActionEvent e) -> {
			FutureTask<String> f3 = new FutureTask<>(() -> {
				TextWrap.it.taprintln("assembling vardump.txt...");
				String s1 = VarDump.it.dsReport();
				try {
					Files.write(Paths.get("vardump.txt"), s1.getBytes());
				} catch (IOException e1) {
					e1.printStackTrace();
				}
				TextWrap.it.taprintln("vardump.txt written.");
				// var s1 = VarDump.dsJson(DSList)
				return s1;
			});
			Thread th = new Thread(null, f3, "vardump");
			th.setDaemon(true);
			th.start();
		});

		this.lbCurDir.setTooltip(new Tooltip("Current directory being scanned"));

		this.cbDirect.setTooltip(new Tooltip("Scan using more direct calls."));
		this.cbDirect.setSelected(false);
		this.cbDirect.setOnAction(e -> CC.option_WDE = this.cbDirect.isSelected());

		this.cbBackgroundPartial.setTooltip(new Tooltip("Repetitive scan based on change notification and detected errors"));
		this.cbBackgroundPartial.setSelected(false);
		this.cbBackgroundPartial.setOnAction(e -> {
			if (this.cbBackgroundPartial.isSelected()) {
				this.f5.setDelay(Duration.seconds(2));
				this.f5.setPeriod(Duration.seconds(40));
				this.f5.restart();
			} else {
				this.f5.cancel();
			}
		});

		this.cbLogAllScans.setSelected(false);
		this.cbLogAllScans.setTooltip(new Tooltip("Log all dir scans"));

		this.arList.setTooltip(new Tooltip("Change notification/error directories"));
		this.taEvents.setTooltip(new Tooltip("Events"));
		this.stDStats = new DStatsTable();
		this.stDStats.setPrefHeight(this.minh * 1.5);

		ArrayList<String> args = new ArrayList<String>(getParameters().getUnnamed());
		if (!args.isEmpty()) {
			this.parms = ParamReader.build(args);
		} else {
			this.parms = ParamReader.build(new Predicate<VL>() {
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
		}

		///
		restart();

		this.vbPartial.getChildren().add(new Label("Changed items"));
		this.vbPartial.getChildren().add(this.arTV);
		this.vbPartial.setSpacing(4);
		this.vbPartial.setPadding(new Insets(6, 4, 6, 4));

		this.hb4.getChildren().add(this.cbDirect);
		this.hb4.getChildren().add(this.cbLogAllScans);
		this.hb4.getChildren().add(this.cbBackgroundPartial);
		this.hb4.setSpacing(4);
		this.hb4.setPadding(new Insets(6, 4, 6, 4));

		this.arTV.setPrefHeight(this.minh);

		this.hbButtons.getItems().add(this.bFull);
		this.hbButtons.getItems().add(this.bPartial);
//		this.hbButtons.getItems().add(this.bClearCaches);
//		this.hbButtons.getItems().add(this.bGitBackup);
//		this.hbButtons.getItems().add(this.bDump);
//		this.hbButtons.getItems().add(this.bRotate);
//		this.hbButtons.getItems().add(this.bQDir);
		this.hbButtons.getItems().add(this.bAbort);
		this.hbButtons.setPadding(new Insets(6, 4, 6, 4));

		this.taEvents.setPrefHeight(this.minh * 1.6);

		this.vb1.getChildren().add(this.lbl0);
		this.vb1.getChildren().add(new Separator());
		this.vb1.getChildren().add(this.hbButtons);
		this.vb1.getChildren().add(this.vbPartial);
		this.vb1.getChildren().add(new Label("Events"));
		this.vb1.getChildren().add(this.taEvents);
		this.vb1.getChildren().add(this.lbCurDir);
		this.lbCurDir.setMinHeight(this.minh / 1.7);

		this.vb1.getChildren().add(this.hb4);

//		stSStats = new SStatsTable();
//		this.stSStats.setPrefHeight(this.minh * 0.6);

//		this.vb1.getChildren().add(stSStats);
		this.vb1.getChildren().add(this.stDStats);

		this.vb1.setSpacing(4);
		this.vb1.setPadding(new Insets(6, 4, 6, 4));

		this.scene1 = new Scene(this.vb1);
	}

	public void start(Stage stage) {
		stage.setResizable(true);
		stage.setTitle("DirSyncApp");
		stage.setScene(this.scene1);
		stage.show();
	}

	@Override
	public void stop() throws Exception {
		if (this.arTV != null) {
			final ChangeRecord ar = this.arTV;
			DSRT.execService.submit(ar::close);
			this.arTV = null;
		}
		for (DSTI te1 : this.dsl.d) {
			if (te1 != null && te1.runner != null && te1.runner.isRunning()) {
				if (te1.runner.ft != null)
					System.out.println("cancelling " + te1.runner.ft.toString());
				te1.runner.cancel();
			}
		}
		DSRT.execService.shutdown();
		System.out.println("await DSRT execService shutdown");
		try {
			DSRT.execService.awaitTermination(5L, TimeUnit.SECONDS);
		} catch (InterruptedException e) {
			System.out.println(e.toString());
		}
		DSRT.execService.shutdownNow();
		while (!DSRT.execService.isShutdown()) Thread.yield();
		stpe.shutdown();
		System.out.println("await DirSync.stpe shutdown");
		try {
			stpe.awaitTermination(5L, TimeUnit.SECONDS);
		} catch (InterruptedException e) {
			System.out.println(e.toString());
		}
		stpe.shutdownNow();
		while (!stpe.isShutdown()) Thread.yield();
	}

	void cancelTasks() {
		for (DSTI te1 : this.dsl.d) {
			if (te1.runner != null) {
				if (te1.runner.isRunning()) {
					te1.runner.cancel();
				}
			}
		}
	}

	void clearStats(DirSyncer ds) {
		this.taEvents.setText("");
		ds.clearStats();
	}

	boolean noneRunning() {
		for (DSTI te1 : this.dsl.d) {
			if (te1.runner != null) {
				if (te1.runner.isRunning())
					return false;
			}
		}
		return true;
	}

	void restart() {
		this.arList.setText("");
		this.taEvents.setText("");

		if (this.arTV != null) {
			final ChangeRecord r = this.arTV;
			DSRT.execService.submit(r::close);
			this.arTV = null;
		}
		this.lbCurDir.textProperty().unbind();
		this.stDStats.getItems().clear();

		this.dsl = new DSList().build1(this.parms);
		this.arTV = this.dsl.ar;

		StringBuilder lbl0_txt = new StringBuilder("Source: " + this.dsl.s.st.Fp() + "\tTarget(s):");
		for (DSTI te1 : this.dsl.d) {
			lbl0_txt.append(" ").append(te1.st.Fp());
		}
		this.lbl0.setText(lbl0_txt.toString());

		ObservableList<STRow> rows = FXCollections.observableArrayList();
		if(DirSyncApp.it.dsl.d.size() > 0) {
			rows.add(new SRow(DirSyncApp.it.dsl.d.first().ds));
			this.dsl.d.forEach(dsti -> rows.add(new DRow(dsti.ds)));
		}
		this.stDStats.setItems(rows);

		SimpleStringProperty newln = new SimpleStringProperty("\n");
		SimpleStringProperty[] sspa = new SimpleStringProperty[this.dsl.d.size() * 2];
		int ii = 0;
		for (DSTI dsti : this.dsl.d) {
			sspa[ii++] = (SimpleStringProperty) dsti.ds.curdir.p;
			sspa[ii++] = newln;
		}
		this.lbCurDir.textProperty().bind(Bindings.concat(
			(Object[]) sspa
		));
	}

	void rotate() {
		@SuppressWarnings("unchecked")
		ArrayList<RtData> tmp1 = (ArrayList<RtData>) this.parms.clone();
		tmp1.remove(0);
		tmp1.add(this.parms.get(0));
		this.parms = tmp1;
		restart();
		this.arTV.refreshTreeView();
	}

	void chkCN() {
		arTV.cn.start();
	}

	void runFullSyncs() {
		chkCN();
		for (DSTI te1 : this.dsl.d) {
			if (te1.runner == null) {
				te1.runner = new DirSyncRunner(te1, Collections.singletonList(new RD("")), true);
				clearStats(te1.ds);
				te1.runner.start();
			} else {
				clearStats(te1.ds);
				te1.runner.restart(Collections.singletonList(new RD("")), true);
			}
		}
	}

	void runGitBackups() {
		chkCN();
		if ((this.thar.get() != null && this.thar.get().state.ordinal() <= DSRT.State.Running.ordinal())
			|| (this.f2 != null && !(this.f2.isCancelled() || this.f2.isDone())))
			return;
		this.thar.set(null);
		this.f2 = null;
		Callable<Void> c1 = () -> {
			DSRT th = (DSRT) Thread.currentThread();
			this.thar.set(th);
			th.clear();
			th.setName(th.getName() + " git-backups");
			for (DSTI te1 : this.dsl.d) {
				te1.ds.clearStats();
			}
//			GitFunctions.doUpdates();
			////
//			ArrayList<FP> fpl = GitFunctions.findRepos();
//			if (!fpl.isEmpty()) {
//				fpl.sort(GitFunctions::compareGDs);
//				final Collection<RD> rdl = new ArrayList<>(dsl.ar.cnl.keySet());
//				for (FP fp : fpl) {
//					RD rd = new RD(DSubs.relativize(dsl.s.rt.s, fp.s));
//					rdl.add(rd);
//				}
//				for (DSTI te1 : dsl.d) {
//					if (te1.runner == null) {
//						te1.runner = new DirSyncRunner(te1, rdl, true);
//						te1.runner.start();
//					} else {
//						te1.runner.restart(rdl, true);
//					}
//				}
//			}
			////

			th.state = DSRT.State.Succeeded;
			th.resetName();
			th.setName(th.getName() + " git-backups");
			return null;
		};
		Callable<Void> c2 = () -> {
			Future<Void> f1 = DSRT.execService.submit(c1);
			try {
				f1.get();
			} catch (InterruptedException | ExecutionException e) {
				e.printStackTrace();
			}
			return null;
		};
		this.f2 = DSRT.execService.submit(c2);
	}

	void runPartialSyncs() {
		chkCN();
		final Collection<RD> rdl = new ArrayList<>(this.dsl.ar.cnl.keySet());
		for (DSTI te1 : this.dsl.d) {
			if (te1.runner == null) {
				te1.runner = new DirSyncRunner(te1, rdl, true);
				clearStats(te1.ds);
				te1.runner.start();
			} else {
				clearStats(te1.ds);
				te1.runner.restart(rdl, true);
			}
		}
	}

	void runPartialSyncsBackground() {
		chkCN();
		final Collection<RD> rdl = new ArrayList<>(this.dsl.ar.cnl.keySet());
		for (DSTI te1 : this.dsl.d) {
			if (te1.runner == null) {
				te1.runner = new DirSyncRunner(te1, rdl, true);
				te1.runner.start();
			} else {
				te1.runner.restart(rdl, true);
			}
		}
	}

	void runQDir() {
		ArrayList<String> cmdline = new ArrayList<>();
		cmdline.add(Paths.get(System.getenv("FLASH0"), "PortableApps", "Q-DirPortable", "Q-DirPortable.exe").toString());
		this.dsl.ar.cnl.forEach((rd, e) -> e.dsl.forEach(ds -> {
			if (!e.fl.isEmpty()) {
				cmdline.add(DSubs.resolve(ds.d.st.Fp().s, rd.s));
			}
		}));
		String cmd = cmdline.stream().collect(Collectors.joining(" "));
		Runnable r = () -> {
			Try<DosCmd.RetV, DosCmd.RetV> rv = DosCmd.exec(cmd);
			if (rv.isFailure()) {
				System.out.println(rv.getE().stderr.stream().collect(Collectors.joining("\n")));
				System.out.println(rv.getE().stdout.stream().collect(Collectors.joining("\n")));
			}
		};
		new Thread(null, r, "Q-Dir").start();
	}
}

// wmic process get ExecutablePath, ProcessID
// wmic process get Caption, CommandLine, Description, ExecutablePath, Name,
// ProcessID
// taskkill /FI "IMAGENAME eq java.exe" /F
