package org.ds.event;

import java.util.concurrent.Callable;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicReference;

import javafx.application.Platform;

/**
 * General JavaFX utilities
 *
 * @author hendrikebbers
 */
class FXUtils {
	public static <T> T runAndWait(final Callable<T> c) throws Exception {
		if (Platform.isFxApplicationThread()) {
			return c.call();
		}
		final CountDownLatch doneLatch = new CountDownLatch(1);
		final AtomicReference<T> rv = new AtomicReference<>();
		final AtomicReference<Exception> ex = new AtomicReference<>();

		Platform.runLater(() -> {
			try {
				rv.set(c.call());
			} catch (Exception e) {
				ex.set(e);
			} finally {
				doneLatch.countDown();
			}
		});
		try {
			doneLatch.await();
			if (ex.get() != null) {
				throw ex.get();
			}
		} catch (InterruptedException e) {
			Thread.currentThread().interrupt();
		}
		return rv.get();
	}

	public static void runAndWait(final Runnable r) {
		if (Platform.isFxApplicationThread()) {
			r.run();
		} else {
			final CountDownLatch doneLatch = new CountDownLatch(1);
			Platform.runLater(() -> { // on FXApp thread
				try {
					r.run();
				} finally {
					doneLatch.countDown();
				}
			});
			try {
				doneLatch.await();
			} catch (InterruptedException e) {
				Thread.currentThread().interrupt();
			}
		}
	}
}