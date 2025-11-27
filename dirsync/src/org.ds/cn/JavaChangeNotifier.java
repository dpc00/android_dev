package org.ds.cn;

import java.io.IOException;
import java.nio.file.FileSystems;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardWatchEventKinds;
import java.nio.file.WatchEvent;
import java.nio.file.WatchKey;
import java.nio.file.WatchService;

import org.ds.event.AEvent;
import org.ds.event.CNEvent;
import org.ds.event.DSEventType;
import org.ds.types.RD;
import org.ds.types.ST;

import com.sun.nio.file.ExtendedWatchEventModifier;

import javafx.beans.property.SimpleObjectProperty;
import javafx.beans.value.ChangeListener;
import javafx.event.Event;
import javafx.event.EventType;

public class JavaChangeNotifier implements IChangeNotifier {
	private final Thread cnt;
	private final ST st;

	public SimpleObjectProperty<CNEvent> evntprop = new SimpleObjectProperty<CNEvent>();
	WatchService ws;
	WatchKey k1;

	public JavaChangeNotifier(ST st, ChangeListener<CNEvent> cncl) {
		this.st = st;
		this.evntprop.addListener(cncl);
		this.cnt = new Thread(Thread.currentThread().getThreadGroup(), JavaChangeNotifier.this::cns, "JavaChangeNotifier");
		this.cnt.setDaemon(true);
	}

	public void start() {
		if (this.cnt.getState() == Thread.State.NEW) this.cnt.start();
	}

	public void close() {
		try {
			if (this.ws != null) this.ws.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private void cns() {
		while (true) {
			if (this.ws == null || this.k1 == null) {
				try {
					Path p = Paths.get(this.st.Fp().s);
					if (this.ws == null) this.ws = FileSystems.getDefault().newWatchService();
					this.k1 = p.register(this.ws, new WatchEvent.Kind<?>[]{
						StandardWatchEventKinds.ENTRY_CREATE,
						StandardWatchEventKinds.ENTRY_DELETE,
						StandardWatchEventKinds.ENTRY_MODIFY
					}, ExtendedWatchEventModifier.FILE_TREE);
				} catch (IOException e) {
					e.printStackTrace();
					if (this.ws != null) {
						try {
							this.ws.close();
						} catch (IOException e2) {
							e2.printStackTrace();
						}
						this.ws = null;
					}
				}
			} else {
				for (WatchEvent<?> we : this.k1.pollEvents()) {
					EventType<AEvent> et = null;
					switch (we.kind().name()) {
						case "ENTRY_CREATE":
							et = DSEventType.CNADD;
							break;
						case "ENTRY_DELETE":
							et = DSEventType.CNREM;
							break;
						case "ENTRY_MODIFY":
							et = DSEventType.CNMOD;
							break;
						default:
							System.out.println(we.kind().name());
							continue;
					}
					RD rd = new RD(((WatchEvent<Path>) we).context().toString());
					CNEvent cne = new CNEvent(JavaChangeNotifier.this, Event.NULL_SOURCE_TARGET, et, rd);
					this.evntprop.setValue(cne);
				}
				if (this.k1.isValid()) {
					this.k1.reset();
					Thread.yield();
				} else {
					try {
						this.ws.close();
						this.ws = null;
						this.k1 = null;
					} catch (IOException e) {
						e.printStackTrace();
						this.ws = null;
						this.k1 = null;
					}
				}
			}
			if (Thread.currentThread().isInterrupted()) break;
		}
	}
}
