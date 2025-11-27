package org.ds.l4;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.concurrent.Callable;
import java.util.concurrent.FutureTask;
import java.util.stream.Collectors;

import org.ds.l3.DSRT;
import org.ds.types.RD;
import org.ds.ui.TextWrap;

public class DirSyncRunner {
	// private DirSyncer ds;
	private static boolean isfirst = true;
	DSTI te;
	DSRT th;
	public FutureTask<ArrayList<Exception>> ft;
	Collection<RD> rdl;
	boolean cas;
	ArrayList<Exception> exs = new ArrayList<>();

	private Callable<ArrayList<Exception>> clb = new Callable<ArrayList<Exception>>() {
		@Override
		public ArrayList<Exception> call() throws Exception {
			DirSyncRunner.this.th = (DSRT) Thread.currentThread();
			DirSyncRunner.this.th.clear();
			DirSyncRunner.this.exs.clear();
			String m = DirSyncRunner.this.cas ? "Full" : "Partial";
			DirSyncRunner.this.th.state = DSRT.State.Running;
			doWork(DirSyncRunner.this.rdl, DirSyncRunner.this.cas, DirSyncRunner.this.exs);
			switch (DirSyncRunner.this.th.state.name()) {
				case "Running":
					if (DirSyncRunner.this.exs.isEmpty()) {
						DirSyncRunner.this.th.state = DSRT.State.Succeeded;
						DirSyncRunner.this.th.resetName();
						TextWrap.it.taprintln(m + " sync " + DirSyncRunner.this.te.ds.s.st.Fp().s + "=>" + DirSyncRunner.this.te.ds.d.st.Fp().s + " succeeded.");
					} else {
						DirSyncRunner.this.th.state = DSRT.State.Failed;
						DirSyncRunner.this.th.resetName();
						TextWrap.it.taprintln(m + " sync " + DirSyncRunner.this.te.ds.s.st.Fp().s + "=>" + DirSyncRunner.this.te.ds.d.st.Fp().s + " failed.");
					}
					break;
				case "Cancelling":
					DirSyncRunner.this.th.state = DSRT.State.Cancelled;
					DirSyncRunner.this.th.resetName();
				case "Cancelled":
					TextWrap.it.taprintln(m + " sync " + DirSyncRunner.this.te.ds.s.st.Fp().s + "=>" + DirSyncRunner.this.te.ds.d.st.Fp().s + " cancelled.");
					break;
				case "Interrupting":
					DirSyncRunner.this.th.state = DSRT.State.Interrupted;
					DirSyncRunner.this.th.resetName();
				case "Interrupted":
					TextWrap.it.taprintln(m + " sync " + DirSyncRunner.this.te.ds.s.st.Fp().s + "=>" + DirSyncRunner.this.te.ds.d.st.Fp().s + " interrupted.");
					break;
			}
			dumpExceptions(DirSyncRunner.this.exs);
			DirSyncRunner.this.te.ds.rcnt++;
			return DirSyncRunner.this.exs;
		}
	};

	public DirSyncRunner(DSTI te, Collection<RD> rdl, boolean cas) {
		this.te = te;
		this.rdl = rdl;
		this.cas = cas;
	}

	public void cancel() {
		if (this.th != null) {
			this.th.cancelreq = true;
		} else if (this.ft != null)
			this.ft.cancel(true);
	}

	public void doWork(Collection<RD> rdl, boolean cas, ArrayList<Exception> exs) {
		String m = DirSyncRunner.this.cas ? "Full" : "Partial";
		DSRT th = (DSRT) Thread.currentThread();
		th.resetName();
		th.setName(th.getName() + " " + m + " dirsync (" + this.te.ds.s.st.Fp().s + ")->(" + this.te.ds.d.st.Fp().s + ")");

		Exception e2 = DSRT.isCancelled();
		if (e2 != null) {
			exs.add(e2);
			return;
		}
		this.te.ds.scanDirPairs(rdl, cas, exs);
		if (DirSyncer.chkCancelled(exs)) {
			th.state = DSRT.State.Cancelling;
		}
		if (DirSyncer.chkInterrupted(exs)) {
			th.state = DSRT.State.Interrupting;
		}
	}

	public void dumpExceptions(ArrayList<Exception> exs) {
		if (!exs.isEmpty()) {
			try {
				Files.write(Paths.get("./DirSyncAppErrors.log"), exs.stream().map(e -> {
					StringBuilder s1 = new StringBuilder(e.toString());
					if (e.getCause() != null && e.getCause() != e) {
						s1.append(", ").append(e.getCause().toString());
					}
					if (e.getSuppressed() != null) {
						for (Throwable e2 : Arrays.asList(e.getSuppressed())) {
							s1.append(", ").append(e2.toString());
						}
					}
					return s1.toString();
				}).collect(Collectors.toList()), (isfirst ? StandardOpenOption.CREATE : StandardOpenOption.APPEND));
				isfirst = false;
			} catch (IOException e) {
			}
		}
	}

	public void finalize() {
		if (isRunning()) {
			cancel();
		}
	}

	public boolean isRunning() {
		return this.th != null && this.th.state == DSRT.State.Running;
	}

	public void restart(Collection<RD> rdl, boolean cas) {
		if (isRunning())
			return;
		this.rdl = rdl;
		this.cas = cas;
		start();
	}

	public void start() {
		if (isRunning())
			return;
		this.ft = (FutureTask<ArrayList<Exception>>) DSRT.execService.submit(this.clb);
	}

	public boolean notStarted() {
		if(this.th == null) return true;
		return this.th.state == DSRT.State.New;
	}

	public boolean isntDone() {
		if(this.th == null) return true;
		return this.th.state.ordinal() < DSRT.State.Interrupted.ordinal();
	}
}
