package org.ds.l4;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.LinkOption;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;
import java.util.Map;
import java.util.Objects;
import java.util.function.Consumer;
import java.util.function.Predicate;

import org.ds.app.DirSyncApp;
import org.ds.cn.ChangeRecord;
import org.ds.event.DSEData;
import org.ds.event.DSErrorEvent;
import org.ds.event.DSEvent;
import org.ds.event.DSEventType;
import org.ds.event.DSMagEvent;
import org.ds.event.DSStartEndEvent;
import org.ds.l2.DE;
import org.ds.l3.CC.Contents;
import org.ds.l3.DSRT;
import org.ds.l3.DSubs;
import org.ds.l3.Failure;
import org.ds.l3.OpCode;
import org.ds.l3.OpList;
import org.ds.l3.Success;
import org.ds.l3.Try;
import org.ds.types.DItem;
import org.ds.types.FN;
import org.ds.types.FP;
import org.ds.types.RD;
import org.ds.types.Updatable;
import org.ds.ui.TextWrap;

import javafx.beans.property.SimpleLongProperty;
import javafx.beans.property.SimpleObjectProperty;
import javafx.beans.property.SimpleStringProperty;
import javafx.event.Event;
import javafx.event.EventTarget;

//import org.ds.l1.KSubs;
//import org.ds.l1.WindowsScanDir;

public class DirSyncer {
	public class DPI {
		DItem cd1;
		DItem cd2;
		OpList ops;
		RD rd;
		int ii;
		int jj;
		boolean blocked;

//		public DPI(FP cd1, FP cd2, RD rd, OpList ops) {
//			this.cd1 = cd1;
//			this.cd2 = cd2;
//			this.rd = rd;
//			this.ops = ops;
//		}

		public DPI(RD rd) {
			this.rd = rd;
			this.cd1 = s.st.SDir(rd);
			this.cd2 = d.st.SDir(rd);
			Contents sContents = s.cc.getContents(this.cd1);
			Contents dContents = d.cc.getContents(this.cd2);
			this.ops = new OpList(sContents, dContents);
			if (sContents.files.containsKey(".nosync") || cd1.Fp().s.contains("$RECYCLE.BIN") || cd1.Rp().s.contains("System Volume Information")) {
				this.blocked = true;
			}
		}
	}

	public static class DPIStack implements Iterable<DPI> {
		ArrayList<DPI> stk = new ArrayList<>();

		@Override
		public Iterator<DPI> iterator() {
			return new Iterator<DPI>() {
				@Override
				public boolean hasNext() {
					return !isEmpty();
				}

				@Override
				public DPI next() {
					return pop();
				}
			};
		}

		public int size() {
			return this.stk.size();
		}

		void add(DPI dpi) {
			this.stk.add(dpi);
		}

		boolean isEmpty() {
			return this.stk.size() == 0;
		}

		// abcde
		//

		DPI pop() {
			if (this.stk.size() > 0) {
				return this.stk.remove(0);
			}
			throw new IndexOutOfBoundsException("DPI.pop");
		}

		void push(DPI dpi) {
			this.stk.add(0, dpi);
		}
	}

	boolean ncd = true;
	public DSSI s;
	public DSTI d;
	public int rcnt;
	public static String empty = "";
	static int dcnt = 0;
	private ArrayList<EventTarget> etl = new ArrayList<>();

	public Updatable<Number> bytescopied = new Updatable<>(0L, new SimpleLongProperty(0L));
	public Updatable<Number> bytesdeleted = new Updatable<>(0L, new SimpleLongProperty(0L));
	public Updatable<Number> dirsadded = new Updatable<>(0L, new SimpleLongProperty(0L));
	public Updatable<Number> dirsdeleted = new Updatable<>(0L, new SimpleLongProperty(0L));
	public Updatable<Number> errorcnt = new Updatable<>(0L, new SimpleLongProperty(0L));
	public Updatable<Number> filescopied = new Updatable<>(0L, new SimpleLongProperty(0L));
	public Updatable<Number> filesdeleted = new Updatable<>(0L, new SimpleLongProperty(0L));
	public Updatable<String> curdir = new Updatable<>("", new SimpleStringProperty(""));

	public SimpleObjectProperty<DSEvent> evntprop = new SimpleObjectProperty<DSEvent>(null);

	public DirSyncer(final DSSI s, final DSTI d, ChangeRecord ar) {
		this.s = s;
		this.d = d;

		if (ar != null) {
			this.evntprop.addListener(ar.dscl);
		}
		this.evntprop.addListener(d.cc.dscl);
	}

	public static boolean chkCancelled(ArrayList<Exception> exs) {
		return exs.stream().anyMatch(ex -> ex instanceof InterruptedException);
	}

	public static boolean chkInterrupted(ArrayList<Exception> exs) {
		return exs.stream().anyMatch(ex -> ex instanceof InterruptedException);
	}

	public void clearStats() {
		this.bytescopied.setV(0L);
		this.bytesdeleted.setV(0L);
		this.dirsadded.setV(0L);
		this.dirsdeleted.setV(0L);
		this.errorcnt.setV(0L);
		this.filescopied.setV(0L);
		this.filesdeleted.setV(0L);
		this.s.cc.dirsread.setV(0L);
		this.s.cc.filesread.setV(0L);
		this.d.cc.dirsread.setV(0L);
		this.d.cc.filesread.setV(0L);
	}

	public ArrayList<Exception> scanDirPair(RD rd, boolean cas) {
		ArrayList<Exception> exs = new ArrayList<>();
		scanDirPair(rd, cas, exs);
		return exs;
	}

	public void scanDirPair(RD rd, Boolean cas, ArrayList<Exception> exs) { // producer
		DPI dpi = new DPI(rd);
		Exception ex = DSRT.isCancelled();
		if (Objects.nonNull(ex)) {
			exs.add(ex);
			return;
		}
		scanDirPair(dpi, cas, exs);
	}

	public void scanDirPairs(Collection<RD> rdl, Boolean cas, ArrayList<Exception> exs) { // producer
		DPIStack stk = new DPIStack();
		for (RD rd : rdl) {
			stk.add(new DPI(rd));
		}
		for (DPI dpi : stk) {
			Exception ex = DSRT.isCancelled();
			if (Objects.nonNull(ex)) {
				exs.add(ex);
				return;
			}
			scanDirPair(dpi, cas, exs);
		}
	}

	private void dClear() {
		this.curdir.setV("");
	}

	private void dirMsg(String m) {
		if (this.ncd) {
			TextWrap.it.taprintln(this.curdir.getV());
			this.ncd = false;
		}
		TextWrap.it.taprintln("   " + m);
	}

	private void fPath(RD rd) {
		String oldcurdirs = this.curdir.getV();
		this.curdir.setV(
			this.d.st.Vl().s + " (" +
				this.d.st.Fp().s + ") <= " +
				this.s.st.Vl().s +  " (" +
				this.s.st.Fp().s + ") " +
				rd.s
		);
		this.ncd = this.ncd || !oldcurdirs.equals(this.curdir.getV());
	}

	private void scanDirPair(DPI ci, Boolean cas, ArrayList<Exception> exs) { // producer
		Consumer<DPI> bs1 = qi -> {
			DSStartEndEvent ev1 = new DSStartEndEvent(DirSyncer.this, Event.NULL_SOURCE_TARGET, DSEventType.SCANNING,
				DirSyncer.this, qi.rd, null);
			// System.out.println(ev1.getEventType().getName() + " " + qi.rd +
			// " (" + (++dcnt) + ")");
			this.evntprop.setValue(ev1);
		};
		@SuppressWarnings("unused")
		Consumer<DPI> bs2 = qi -> {
			DSStartEndEvent ev1 = new DSStartEndEvent(DirSyncer.this, Event.NULL_SOURCE_TARGET, DSEventType.SCANNING,
				DirSyncer.this, qi.rd, null);
			// System.out.println(ev1.getEventType().getName() + "2 " + qi.rd);
		};
		Consumer<DPI> es = qi -> {
			DSStartEndEvent ev1 = new DSStartEndEvent(DirSyncer.this, Event.NULL_SOURCE_TARGET, DSEventType.ENDSCAN,
				DirSyncer.this, qi.rd, null);
			// System.out.println(ev1.getEventType().getName() + " " + qi.rd);
			this.evntprop.setValue(ev1);
		};
		Consumer<DPI> ckb = nci -> {
			if (nci.ops.size() > 0) {
				System.out.println(
					"skipping blocked dir " + nci.rd + " which has the following " + nci.ops.size() + " operations:");
				for (OpCode oc : nci.ops.keySet()) {
					for (DE de : nci.ops.get(oc)) {
						System.out.println("\t" + oc.name() + " " + (de != null ? de.toString() : ""));
					}
				}
			} else {
				System.out.println("skipping blocked dir " + nci.rd);
			}
		};

		Predicate<OpList> justDexi = new Predicate<OpList>() {
			public boolean test(OpList ol) {
				for (OpCode oc : ol.keySet()) {
					if (oc != OpCode.dExi) return false;
				}
				return true;
			}
		};

		dcnt = 0;

		fPath(ci.rd);
		if (DirSyncApp.it != null && DirSyncApp.it.cbLogAllScans.isSelected()) {
			dirMsg("is being scanned...");
		}
		if (ci.ops.size() > 0 && !justDexi.test(ci.ops)) {
			System.out.format("checking %s -> %s, %s\n", this.s.st.Fp().s, this.d.st.Fp().s, ci.rd);
			for (Map.Entry<OpCode, ArrayList<DE>> opil : ci.ops.entrySet()) {
				System.out.format("%s: %d items\n", opil.getKey().name(), opil.getValue().size());
			}
			System.out.format("%02d dirs %02d files\n",
				this.s.cc.dirsread.getV().longValue() + this.d.cc.dirsread.getV().longValue(),
				this.s.cc.filesread.getV().longValue() + this.d.cc.filesread.getV().longValue());
			System.out.format("cache %02d hits %02d misses\n", CHM.hits, CHM.misses);
		}
		bs1.accept(ci);

		if (!ci.blocked) {
			Exception ex = DSRT.isCancelled();
			if (Objects.nonNull(ex))
				return;

			ArrayList<DE> al = ci.ops.get(OpCode.dMis);
			if (al != null && al.size() > 0) {
				for (DE de : al) {
					RD nrd = new RD(DSubs.resolve(ci.rd.s, de.fname));
					scanDirPair(nrd, true);
					// DItem ncd1 = ci.cd1.SDir(de.fname);
					// DItem ncd2 = ci.cd2.SDir(new RD(de.fname));
					// DSubs.removeTree(ncd2.Fp().s);
					// dirMsg("deleted tree " + de.fname);
				}
				ci.ops.remove(OpCode.dMis);
			}

			al = ci.ops.get(OpCode.dCrt);
			if (al != null) {
				try {
					if (!DSubs.dir_exists(ci.cd2.Fp().s)) {
						Files.createDirectories(Paths.get(ci.cd2.Fp().s));
						ci.ops.modcnt += 1;
						this.dirsadded.setV((Long) this.dirsadded.getV() + 1L);
						fPath(new RD(DSubs.getParent(ci.rd.s)));
						dirMsg("added dir " + DSubs.getFileName(ci.rd.s));
						DSEvent ev1 = new DSEvent(this, Event.NULL_SOURCE_TARGET, DSEventType.CREATEDIR,
							new DSEData(new RD(DSubs.getParent(ci.rd.s)), new FN(DSubs.getFileName(ci.rd.s))));
						this.evntprop.setValue(ev1);
					}
				} catch (Exception ex2) {
					this.errorcnt.setV((Long) this.errorcnt.getV() + 1L);
					fPath(new RD(DSubs.getParent(ci.rd.s)));
					dirMsg("dir create failed: " + ex2.toString());
					DSErrorEvent ev1 = new DSErrorEvent(this, Event.NULL_SOURCE_TARGET, DSEventType.ERROR, this,
						new RD(DSubs.getParent(ci.rd.s)), new FN(DSubs.getFileName(ci.rd.s)), ex2);
					this.evntprop.setValue(ev1);
					exs.add(ex2);
				}
				ci.ops.remove(OpCode.dCrt);
			}

			al = ci.ops.get(OpCode.dNew);
			if (al != null && al.size() > 0) {
				for (DE de : al) {
					RD nrd = new RD(DSubs.resolve(ci.rd.s, de.fname));
					scanDirPair(nrd, true);
					// RD nrd = new RD(de.fname);
					// DItem ncd1 = ci.cd1.SDir(nrd);
					// DItem ncd2 = ci.cd2.SDir(nrd);
					// DSubs.mirrorTree(ncd1.Fp().s, ncd2.Fp().s);
					// dirMsg("mirrored tree " + de.fname);
				}
				ci.ops.remove(OpCode.dNew);
			}

			// boolean tmp = false;
			// al = ci.ops.get(OpCode.fMis);
			// if(al != null && al.size()>0) {
			// 	tmp = true;
			// }
			// al = ci.ops.get(OpCode.fNew);
			// if(al != null && al.size()>0) {
			// 	tmp = true;
			// }
			// al = ci.ops.get(OpCode.fMod);
			// if(al != null && al.size()>0) {
			// 	tmp = true;
			// }
			// if(tmp) {
			// 	DSubs.mirrorDir(ci.cd1.Fp().s, ci.cd2.Fp().s);
			// 	dirMsg("mirrored dir " + DSubs.getFileName(ci.cd1.Fp().s));
			// }

			al = ci.ops.get(OpCode.fMis);
			if (al != null && al.size() > 0) {
				for (DE de : al) {
					FP fp2 = new FP(DSubs.resolve(ci.cd2.Fp().s, de.fname));
					try {
						if (chkDeletable(fp2)) {
							DSubs.delete_file(fp2.s);
							ci.ops.modcnt += 1;
							this.bytesdeleted.setV((Long) this.bytesdeleted.getV() + de.size);
							this.filesdeleted.setV((Long) this.filesdeleted.getV() + 1L);
							fPath(ci.rd);
							dirMsg("deleted file " + de.fname.toUpperCase());
							DSMagEvent ev1 = new DSMagEvent(this, Event.NULL_SOURCE_TARGET, DSEventType.DELETEFILE, ci.rd,
								new FN(de.fname), de.size);
							this.evntprop.setValue(ev1);
						}
					} catch (Exception ex4) {
						this.errorcnt.setV((Long) this.errorcnt.getV() + 1L);
						fPath(new RD(DSubs.getParent(ci.rd.s)));
						dirMsg("file delete failed: " + ex4.toString());
						DSErrorEvent ev1 = new DSErrorEvent(this, Event.NULL_SOURCE_TARGET, DSEventType.ERROR, this, ci.rd,
							new FN(de.fname), ex4);
						this.evntprop.setValue(ev1);
						exs.add(ex4);
					}
				}
				ci.ops.remove(OpCode.fMis);
			}
			al = ci.ops.get(OpCode.fNew);
			if (al != null && al.size() > 0) {
				for (DE de : al) {
					FP fp1 = new FP(DSubs.resolve(ci.cd1.Fp().s, de.fname));
					FP fp2 = new FP(DSubs.resolve(ci.cd2.Fp().s, de.fname));
					if (chkCopyable(fp2)) {
						Try<Void, Exception> rv = DSubs.copy_file(fp1.s, fp2.s);
						if (rv instanceof Success) {
							ci.ops.modcnt += 1;
							this.bytescopied.setV((Long) this.bytescopied.getV() + de.size);
							this.filescopied.setV((Long) this.filescopied.getV() + 1L);
							fPath(ci.rd);
							dirMsg("copied file " + de.fname.toUpperCase());
							DSMagEvent ev1 = new DSMagEvent(this, Event.NULL_SOURCE_TARGET, DSEventType.COPYFILE, ci.rd,
								new FN(de.fname), de.size);
							this.evntprop.setValue(ev1);
						} else if (rv instanceof Failure) {
							Exception ex3 = rv.getE();
							this.errorcnt.setV((Long) this.errorcnt.getV() + 1L);
							fPath(new RD(DSubs.getParent(ci.rd.s)));
							dirMsg("file copy failed: " + ex3.toString());
							DSErrorEvent ev1 = new DSErrorEvent(this, Event.NULL_SOURCE_TARGET, DSEventType.ERROR, this, ci.rd,
								new FN(de.fname), ex3);
							this.evntprop.setValue(ev1);
							exs.add(ex3);
						}
					}
				}
				ci.ops.remove(OpCode.fNew);
			}
			al = ci.ops.get(OpCode.fMod);
			if (al != null && al.size() > 0) {
				for (DE de : al) {
					FP fp1 = new FP(DSubs.resolve(ci.cd1.Fp().s, de.fname));
					FP fp2 = new FP(DSubs.resolve(ci.cd2.Fp().s, de.fname));
					if (chkCopyable(fp2)) {
						Try<Void, Exception> rv = DSubs.copy_file(fp1.s, fp2.s);
						if (rv instanceof Success) {
							ci.ops.modcnt += 1;
							this.bytescopied.setV((Long) this.bytescopied.getV() + de.size);
							this.filescopied.setV((Long) this.filescopied.getV() + 1L);
							fPath(ci.rd);
							dirMsg("copied file " + de.fname.toUpperCase());
							DSMagEvent ev1 = new DSMagEvent(this, Event.NULL_SOURCE_TARGET, DSEventType.COPYFILE, ci.rd,
								new FN(de.fname), de.size);
							this.evntprop.setValue(ev1);
						} else if (rv instanceof Failure) {
							Exception ex3 = rv.getE();
							this.errorcnt.setV((Long) this.errorcnt.getV() + 1L);
							fPath(new RD(DSubs.getParent(ci.rd.s)));
							dirMsg("file copy failed: " + ex3.toString());
							DSErrorEvent ev1 = new DSErrorEvent(this, Event.NULL_SOURCE_TARGET, DSEventType.ERROR, this, ci.rd,
								new FN(de.fname), ex3);
							this.evntprop.setValue(ev1);
							exs.add(ex3);
						}
					}
				}
				ci.ops.remove(OpCode.fMod);
			}
			al = ci.ops.get(OpCode.dExi);
			if (cas && al != null && al.size() > 0) {
				for (DE de : al) {
					RD nrd = new RD(DSubs.resolve(ci.rd.s, de.fname));
					scanDirPair(nrd, cas);
				}
				ci.ops.remove(OpCode.dExi);
			}

			al = ci.ops.get(OpCode.dDel);
			if (al != null) {
				try {
					if (chkDeletable(ci.cd2.Fp())) {
						DSubs.remove_directory(ci.cd2.Fp().s);
						ci.ops.modcnt += 1;
						this.dirsdeleted.setV((Long) this.dirsdeleted.getV() + 1L);
						fPath(new RD(DSubs.getParent(ci.rd.s)));
						dirMsg("deleted dir " + DSubs.getFileName(ci.rd.s));
						DSEvent ev1 = new DSEvent(this, Event.NULL_SOURCE_TARGET, DSEventType.REMOVEDIR,
							new DSEData(new RD(DSubs.getParent(ci.rd.s)), new FN(DSubs.getFileName(ci.rd.s))));
						this.evntprop.setValue(ev1);
					}
				} catch (Exception ex5) {
					this.errorcnt.setV((Long) this.errorcnt.getV() + 1L);
					fPath(new RD(DSubs.getParent(ci.rd.s)));
					dirMsg("dir del failed: " + ex5.toString());
					DSErrorEvent ev1 = new DSErrorEvent(this, Event.NULL_SOURCE_TARGET, DSEventType.ERROR, this,
						new RD(DSubs.getParent(ci.rd.s)), new FN(DSubs.getFileName(ci.rd.s)), ex5);
					this.evntprop.setValue(ev1);
					exs.add(ex5);
					// return new Failure<>(exs);
				}
				ci.ops.remove(OpCode.dDel);
			}
		} else {
			ckb.accept(ci);
		}
		es.accept(ci);
		dClear();
	}

	private boolean chkDeletable(FP fp2) {
		Path p = Paths.get(fp2.s);
		if (Files.exists(p, LinkOption.NOFOLLOW_LINKS)) {
			return isWritable(fp2);
		}
		return false;
	}

	private boolean chkCopyable(FP fp2) {
		Path p = Paths.get(fp2.s);
		if (Files.exists(p, LinkOption.NOFOLLOW_LINKS)) {
			return isWritable(fp2);
		}
		return true;
	}

	private boolean isWritable(FP fp2) {
		Path p = Paths.get(fp2.s);
		if (!Files.isWritable(p)) {
			try {
				Files.setAttribute(p, "dos:readonly", false, LinkOption.NOFOLLOW_LINKS);
				Files.setAttribute(p, "dos:system", false, LinkOption.NOFOLLOW_LINKS);
				Files.setAttribute(p, "dos:hidden", false, LinkOption.NOFOLLOW_LINKS);
			} catch (IOException e) {
				e.printStackTrace();
			}
			return Files.isWritable(p);
		}
		return true;
	}

}
