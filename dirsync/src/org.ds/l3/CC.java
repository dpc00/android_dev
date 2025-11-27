package org.ds.l3;

import java.io.IOException;
import java.io.Serializable;
import java.nio.file.AccessDeniedException;
import java.nio.file.DirectoryStream;
import java.nio.file.NoSuchFileException;
import java.nio.file.NotDirectoryException;
import java.util.TreeMap;

import org.ds.cn.ChangeRecord;
import org.ds.event.AEvent;
import org.ds.event.AREvent;
import org.ds.event.AbstractEventTarget;
import org.ds.event.DSEvent;
import org.ds.event.DSEventType;
import org.ds.l2.DE;
import org.ds.l2.IDEStream;
import org.ds.l2.JavaDEStream;
import org.ds.l2.WindowsDEStream;
import org.ds.l4.CHM;
import org.ds.types.DItem;
import org.ds.types.FP;
import org.ds.types.ST;
import org.ds.types.Updatable;

import javafx.beans.property.SimpleLongProperty;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.event.Event;
import javafx.event.EventType;

public class CC extends AbstractEventTarget<AEvent> {
	public static boolean option_WDE = false;

	public CC(ST st, ChangeRecord ar) {
		this.st = st;
		// addEventHandler(DSEventType.ACTION, this.dsl1);
		if (ar != null) {
			ar.evntprop.addListener(this.arcl);
		}
		chm = new CHM(this);
	}

	public ChangeListener<AREvent> arcl = new ChangeListener<AREvent>() {
		@Override
		public void changed(ObservableValue<? extends AREvent> observable, AREvent oldValue, AREvent are) {
			EventType<? extends Event> et = are.getEventType();
			if (et == DSEventType.AREV) {
				DItem sd = CC.this.st.SDir(are.d.rd);
				Contents c = chm.get(sd);
				if (c != null) {
					c.utime = are.etime;
				}
			}
		}
	};

	public CHM chm;
	public Updatable<Number> dirscached = new Updatable<>(0L, new SimpleLongProperty());
	public Updatable<Number> dirsread = new Updatable<>(0L, new SimpleLongProperty());

	// public final EventHandler<AEvent> dsl1 = dse -> {
	// DSEvent dse2 = (DSEvent)dse;
	// String rd = dse2.rd;
	// EventType<? extends Event> et = dse.getEventType();
	// Contents c1 = get(rd);
	// if (c1 != null) {
	// }
	// };

	public ChangeListener<DSEvent> dscl = new ChangeListener<DSEvent>() {
		@Override
		public void changed(ObservableValue<? extends DSEvent> observable, DSEvent oldValue, DSEvent dse) {
			DItem sd = CC.this.st.SDir(dse.d.rd);
			EventType<? extends Event> et = dse.getEventType();
			Contents c1 = chm.get(sd);
			if (c1 != null) {
				switch (et.getName()) {
				case "CREATEDIR":
				case "COPYFILE":
				case "DELETEFILE":
				case "ERROR":
					c1.utime = dse.etime;
					break;
				case "REMOVEDIR":
					chm.remove(sd);
				}
			}
			switch (et.getName()) {
			case "CREATEDIR":
			case "REMOVEDIR":
				DItem psd = sd.Parent();
				Contents c2 = chm.get(psd);
				if (c2 != null) {
					c2.utime = dse.etime;
				}
				break;
			}

		}
	};

	public Updatable<Number> filesread = new Updatable<>(0L, new SimpleLongProperty());
	public long size;

	public final ST st;

	public void clear() {
		chm.clear();
	}
	
	public Contents getContents(DItem sd) {
		return chm.get(sd);
	}

	public static class Contents implements Serializable {
		public IDEStream getStream(String s) throws IOException {
			if(option_WDE) {
				return new WindowsDEStream(s);
			}
			else {
				return new JavaDEStream(s);
			}
		}

		public Contents() {
		}
		public Contents(DItem sd) {
			this.dirs = new TreeMap<>();
			this.files = new TreeMap<>();
			// IDEStream des = null;
			FP p = sd.Fp();
			try (IDEStream des = getStream(p.s)) {
				this.dex = true;
				this.ftime = System.nanoTime();
				for (DE de : des) {
					if (de.isdir) {
						this.dirs.put(de.fname, de);
					} else if (de.isfile) {
						this.files.put(de.fname, de);
					}
				}
			}
			catch(AccessDeniedException e) {
				this.dex = true;
				this.blocked = true;
			}
			catch(NoSuchFileException e) {
				this.dex = false;
				this.blocked = false;
			}
			catch(NotDirectoryException e) {
				this.dex = false;
				this.blocked = false;
			}
			catch (Exception e) {
				System.out.println(e.toString());
			}
		}
		public boolean blocked = false;
		public boolean dex = false;
		public TreeMap<String, DE> dirs;
		public TreeMap<String, DE> files;
		public long ftime;
		public long lfctime;
		public long utime;
	}
}
