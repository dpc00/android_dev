package org.ds.l3;

import java.util.concurrent.CancellationException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ThreadFactory;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

public class DSRT extends Thread {
	private static ThreadFactory thf = r -> {
		DSRT th = new DSRT(r);
		th.setDaemon(true);
		return th;
	};
	public static ExecutorService execService = new ThreadPoolExecutor(16, 64, 5, TimeUnit.MINUTES,
		new LinkedBlockingQueue<>(48000), thf, new ThreadPoolExecutor.AbortPolicy());

	public DSRT(Runnable r) {
		super(Thread.currentThread().getThreadGroup(), r, "DSR (virgin)");
	}

	public State state = State.New;
	public volatile boolean cancelreq = false;

	public static Exception isCancelled() {
		DSRT th = (DSRT) Thread.currentThread();
		boolean b1 = th.cancelreq;
		boolean b2 = th.isInterrupted();
		if (b1) {
			th.state = State.Cancelling;
			return new CancellationException();
		} else if (b2) {
			th.state = State.Interrupting;
			return new InterruptedException();
		}
		return null;
	}

	public void clear() {
		this.cancelreq = false;
		this.state = State.Running;
		resetName();
	}

	public void resetName() {
		setName("DSR " + getId() + " " + this.state.name());
	}

	public enum State {
		New, Running, Interrupting, Cancelling, Interrupted, Cancelled, Failed, Succeeded
	}
}
