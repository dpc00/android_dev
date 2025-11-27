package org.ds.l4;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;
import java.util.function.Consumer;
import java.util.function.Predicate;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.ds.l2.DE;
import org.ds.l3.CC.Contents;
import org.ds.types.DItem;
import org.ds.types.FN;
import org.ds.types.FP;
import org.ds.types.RD;

public class DirScanner {
	public class DI {
		DItem sd;
		Contents c;
		int ii;
		int jj;
		boolean blocked;
		boolean x;

		public DI(DItem sd) {
			this.sd = sd;
			this.c = new Contents(sd);
			if (this.c.files.containsKey(".nosync") || this.sd.Rd().s.contains("$RECYCLE.BIN")
				|| this.sd.Rd().s.equals("System Volume Information")) {
				this.blocked = true;
			}
		}
	}

	public static class DIStack implements Iterable<DI> {
		ArrayList<DI> stk = new ArrayList<>();

		@Override
		public Iterator<DI> iterator() {
			return new Iterator<DI>() {
				@Override
				public boolean hasNext() {
					return !isEmpty();
				}
				@Override
				public DI next() {
					return pop();
				}
			};
		}

		public int size() {
			return this.stk.size();
		}

		void add(DI di) {
			this.stk.add(di);
		}

		boolean isEmpty() {
			return this.stk.size() == 0;
		}

		DI pop() {
			if (this.stk.size() > 0) {
				return this.stk.remove(0);
			}
			throw new IndexOutOfBoundsException("DI.pop");
		}

		void push(DI di) {
			this.stk.add(0, di);
		}
	}

	DItem sd;

	public DirScanner(DItem sd) {
		this.sd = sd;
	}

	public ArrayList<FP> find(String re) {
		DIStack stk = new DIStack();
		stk.add(new DI(this.sd));

		Pattern p = Pattern.compile(re);
		ArrayList<FP> fpl = new ArrayList<>();

		for (DI di : stk) {
			scanDir(di, stk, p, fpl::add);
		}
		return fpl;
	}

	public ArrayList<FP> find(Predicate<FP> ff) {
		DIStack stk = new DIStack();
		stk.add(new DI(this.sd));

//		Pattern p = Pattern.compile(re);
		ArrayList<FP> fpl = new ArrayList<>();

		for (DI di : stk) {
			scanDir(di, stk, ff, fpl::add);
		}
		return fpl;
	}

	public void scanDir(DI di, DIStack stk, Pattern p, Consumer<FP> f) {
		if (!di.blocked) {
			Collection<DE> dicf = di.c.files != null ? di.c.files.values() : null;
			if (dicf != null)
				for (DE de : dicf) {
					FN fn = new FN(de.fname);
					DItem nsd = this.sd.SFile(new RD(de.fname));
					FP fp1 = new FP(nsd.Fp().s);
					Matcher m = p.matcher(fp1);
					if (m.find())
						f.accept(fp1);
				}
			Collection<DE> dicd = di.c.dirs != null ? di.c.dirs.values() : null;
			if (dicd != null)
				for (DE de : dicd) {
					FN fn = new FN(de.fname);
					DItem nsd = this.sd.SDir(new RD(de.fname));
					FP fp1 = new FP(nsd.Fp().s);
					Matcher m = p.matcher(fp1);
					if (m.find())
						f.accept(fp1);
					stk.add(new DI(nsd));
				}
		}
	}

	public void scanDir(DI di, DIStack stk, Predicate<FP> ff, Consumer<FP> f) {
		if (!di.blocked) {
			for (DE de : di.c.files.values()) {
				DItem nsd = this.sd.SFile(new RD(de.fname));
				FP fp1 = new FP(nsd.Fp().s);
				if (ff.test(fp1))
					f.accept(fp1);
			}
			for (DE de : di.c.dirs.values()) {
				DItem nsd = this.sd.SDir(new RD(de.fname));
				FP fp1 = new FP(nsd.Fp().s);
				if (ff.test(fp1))
					f.accept(fp1);
				stk.add(new DI(nsd));
			}
		}
	}
}
