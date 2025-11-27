package org.ds.cn;

import java.io.Closeable;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

import org.ds.app.DirSyncApp;
import org.ds.event.AREvent;
import org.ds.event.CNEvent;
import org.ds.event.DSEvent;
import org.ds.event.DSEventType;
//import org.ds.l1.KSubs;
//import org.ds.l1.WindowsScanDir;
import org.ds.l3.DSubs;
import org.ds.l4.CNHM;
import org.ds.l4.CNHM.Value;
import org.ds.l4.DSHS;
import org.ds.l4.DSTI;
import org.ds.l4.DirSyncer;
import org.ds.l4.EHS;
import org.ds.l4.FEHM;
import org.ds.types.DItem;
import org.ds.types.FN;
import org.ds.types.FP;
import org.ds.types.PCString;
import org.ds.types.RD;
import org.ds.types.RT;
import org.ds.types.ST;
import org.ds.ui.TextWrap;

import javafx.application.Platform;
import javafx.beans.property.SimpleObjectProperty;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.event.Event;
import javafx.event.EventType;
import javafx.scene.control.TreeItem;
import javafx.scene.control.TreeView;

public class ChangeRecord extends TreeView<PCString> implements Closeable {
	ST st;
	public int cnl_cnt = -1;
	public final CNHM cnl;
	private TreeItem<PCString> cnRt;
	public IChangeNotifier cn;
	public SimpleObjectProperty<AREvent> evntprop = new SimpleObjectProperty<AREvent>();

	public ChangeListener<DSEvent> dscl = new ChangeListener<DSEvent>() {
		@Override
		public void changed(ObservableValue<? extends DSEvent> observable, DSEvent oldValue, DSEvent dse) {
			RD rd = dse.d.rd;
			switch (dse.getEventType().getName()) {
				case "SCANNING_FC":
					break;
				case "SCANNING":
				case "SKIPPING":
					synchronized (ChangeRecord.this.cnl) {
						Optional.ofNullable(ChangeRecord.this.cnl.get(rd)).ifPresent(cnle -> {
							if (cnle.dsl.contains(dse.d.ds)) {
								cnle.dsl.remove(dse.d.ds);
								if (cnle.dsl.size() == 0) {
									ChangeRecord.this.cnl.remove(rd);
									refreshTreeView();
								}
							}
						});
					}
					break;
				case "ERROR":
					addErrorDir(dse.d.ds, dse.d.rd, dse.d.fn, dse.d.e);
			}
		}
	};

	public ChangeListener<CNEvent> cncl = new ChangeListener<CNEvent>() {
		private FP osfp;
		private RD ocrd;
		private FN ofn;

		@Override
		public void changed(ObservableValue<? extends CNEvent> observable, CNEvent oldValue, CNEvent cne) {
			EventType<? extends Event> et = cne.getEventType();
			String etn = et.getName();
			DItem sd = st.SDir(cne.d.rd);
			FP sfp = sd.Fp();
			RD crd = null;
			FN fn = null;
			boolean isdir = DSubs.dir_exists(sfp.s);
			boolean isfile = DSubs.file_exists(sfp.s);
			if (isdir) {
				crd = new RD(DSubs.relativize(ChangeRecord.this.st.Fp().s, sfp.s));
				fn = null;
			} else if (isfile) {
				crd = new RD(DSubs.relativize(ChangeRecord.this.st.Fp().s, DSubs.getParent(sfp.s)));
				fn = new FN(DSubs.getFileName(sfp.s));
			}
			if (!isdir && !isfile)
				return;
			switch (etn) {
				case "CNADD":
				case "CNREM":
				case "CNMOD":
					addItem(crd, fn);
					break;
				case "CNRON":
					this.osfp = sfp;
					this.ocrd = crd;
					this.ofn = fn;
					break;
				case "CNRNN":
					if (this.osfp != null && this.ocrd != null && this.ofn != null) {
						if (!movFileOrDir(this.osfp, sfp)) {
							addItem(this.ocrd, this.ofn);
							addItem(crd, fn);
						}
					}
					this.osfp = null;
					this.ocrd = null;
					this.ofn = null;
					break;
			}
		}
	};

	public ChangeRecord(ST st) {
		super();
		this.st = st;
		this.cnl = new CNHM();
		this.cn = new JavaChangeNotifier(this.st, this.cncl);

		this.cnRt = new TreeItem<>(new RT(this.st.Fp().s));

		setRoot(this.cnRt);
		setShowRoot(false);
	}

	public void close() {
		this.cn.close();
	}

	public boolean containsDS(RD rd, DirSyncer ds) {
		synchronized (this.cnl) {
			Value cnle = this.cnl.get(rd);
			if (cnle != null) {
				if (cnle.dsl.contains(ds))
					return true;
			}
			return false;
		}
	}

	public Value newEntry(RD rd) {
		Value rv = new Value(new DSHS(), new FEHM());
		this.cnl.put(rd, rv);
		return rv;
	}

	public void refreshTreeView() {
		// if (DirSyncApp.it.arList != null) {
		int ic = itemCnt();
		if (this.cnl_cnt != ic) {
			Platform.runLater(() -> {
				TreeItem<PCString> tmp = this.cnRt;
				// tmp.setExpanded(true);
				synchronized (this.cnl) {
					tmp.getChildren().setAll(this.cnl.entrySet().stream()
						.sorted(Comparator.comparing(en -> en.getKey().s)).map((Map.Entry<RD, Value> me) -> {
							TreeItem<PCString> ti2 = new TreeItem<>(me.getKey());
							// ti2.setExpanded(true);
							ti2.getChildren().setAll(me.getValue().fl.entrySet().stream()
								.sorted(Comparator.comparing(en -> en.getKey().s)).map((Map.Entry<FN, EHS> me1) -> {
									TreeItem<PCString> ti3 = new TreeItem<>(me1.getKey());
									// ti3.setExpanded(true);
									ti3.getChildren().setAll(me1.getValue().stream()
										.sorted(Comparator.comparing(Throwable::toString)).map((Throwable e) -> {
											List<String> sa = TextWrap.minNumLinesWrap(e.toString(), 80, 10);
											String s = sa.stream().collect(Collectors.joining("\n\t"));
											TreeItem<PCString> ti4 = new TreeItem<>(new PCString(s));
											ti4.setExpanded(true);
											return ti4;
										}).collect(Collectors.toList()));
									return ti3;
								}).collect(Collectors.toList()));
							return ti2;
						}).collect(Collectors.toList()));
				}
			});
			this.cnl_cnt = ic;
		}
	}

	private int itemCnt() {
		final int[] cnt = {0};
		synchronized (this.cnl) {
			for (Value e : this.cnl.values()) {
				cnt[0]++;
				cnt[0] += e.dsl.size();
				cnt[0] += e.fl.size();
				for (EHS el : e.fl.values()) {
					cnt[0] += el.size();
				}
			}
		}
		return cnt[0];
	}

	private Value newEntry(DirSyncer ds, RD rd, FN fn, Throwable e) {
		Value rv = new Value(new DSHS(ds), new FEHM(fn, e));
		this.cnl.put(rd, rv);
		return rv;
	}

	private Value newEntry(RD rd, FN fn) {
		Value rv = new Value(new DSHS(), new FEHM(fn));
		this.cnl.put(rd, rv);
		return rv;
	}

	@SuppressWarnings("unused")
	private Value newEntry(RD rd, FN fn, Throwable e) {
		Value rv = new Value(new DSHS(), new FEHM(fn, e));
		this.cnl.put(rd, rv);
		return rv;
	}

	void addErrorDir(DirSyncer ds, RD rd, FN fn, Throwable e) {
		synchronized (this.cnl) {
			Value cnle = this.cnl.get(rd);
			if (cnle != null) {
				if (!cnle.dsl.contains(ds))
					cnle.dsl.add(ds);
				EHS el = cnle.fl.get(fn);
				if (el != null) {
					if (!el.contains(e))
						el.add(e);
				} else {
					cnle.fl.put(fn, new EHS(e));
				}
			} else {
				newEntry(ds, rd, fn, e);
			}
		}
		refreshTreeView();
	}

	boolean movFileOrDir(FP on1, FP nn1) {
		RD rn1 = new RD(DSubs.relativize(this.st.Fp().s, on1.s));
		RD rn2 = new RD(DSubs.relativize(this.st.Fp().s, nn1.s));
		boolean af = true;

		for (DSTI te1 : DirSyncApp.it.dsl.d) {
			FP on2 = new FP(DSubs.resolve(te1.st.Fp().s, rn1.s));
			FP nn2 = new FP(DSubs.resolve(te1.st.Fp().s, rn2.s));
			try {
				boolean isdir = DSubs.dir_exists(on2.s);
				boolean isfile = DSubs.file_exists(on2.s);
				if (isdir) {
					Files.move(Paths.get(on2.s), Paths.get(nn2.s)); // ??
				} else if (isfile) {
					Files.move(Paths.get(on2.s), Paths.get(nn2.s)); // ??
				} else
					throw new IOException("file/dir not found");
				TextWrap.it.taprintln("renamed " + on2 + " to " + nn2);
				RD rn3 = new RD(DSubs.getParent(rn1.s));
				RD rn4 = new RD(DSubs.getParent(rn2.s));
				AREvent ev1 = new AREvent(ChangeRecord.this, Event.NULL_SOURCE_TARGET, DSEventType.AREV, rn3);
				this.evntprop.setValue(ev1);
				if (!rn3.equals(rn4)) {
					AREvent ev2 = new AREvent(ChangeRecord.this, Event.NULL_SOURCE_TARGET, DSEventType.AREV, rn4);
					this.evntprop.setValue(ev2);
				}
			} catch (Exception e) {
				TextWrap.it.taprintln("rename " + on2 + " to " + nn2 + " failed: " + e.toString());
				af = false;
			}
		}
		return af;
	}

	void addItem(RD rd, FN fn) {
		synchronized (this.cnl) {
			Value cnle = this.cnl.get(rd);
			if (cnle == null) {
				cnle = newEntry(rd, fn);
			} else if (fn != null) {
				cnle.fl.computeIfAbsent(fn, k -> new EHS());
			}
			AREvent are = new AREvent(ChangeRecord.this, Event.NULL_SOURCE_TARGET, DSEventType.AREV, rd);
			this.evntprop.setValue(are);
		}
		refreshTreeView();
	}
}
