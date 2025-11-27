package org.ds.types;

import org.ds.l3.DSubs;

public class DItem {
	boolean isdir;
	ST st;
	RD rd;
	FP fp;
	RD rp;

	public DItem(boolean isdir, ST st, RD rd) {
		this.isdir = isdir;
		this.st = st;
		this.rd = rd;
	}

	public DItem SDir(RD rd) {
		return new DItem(true, this.st, new RD(DSubs.resolve(this.rd.s, rd.s)));
	}

	public DItem SFile(RD rd) {
		return new DItem(false, this.st, new RD(DSubs.resolve(this.rd.s, rd.s)));
	}

	public VL Vl() {
		return this.st.Vl();
	}

	public FP Fp() {
		if (this.fp == null) {
			this.fp = new FP(DSubs.resolve(this.st.Fp().s, this.rd.s));
		}
		return this.fp;
	}

	public RD Rp() {
		if (this.rp == null) {
			String v1 = this.st.Rp().s;
			String v2 = DSubs.resolve(v1, this.rd.s);
			if(v2.length() > 1) {
				String v3 = v2.substring(0,2);
				if(v3.equals("\\\\")) {
					v2 = v2.substring(1);
				}
			}
			this.rp = new RD(v2);
		}
		return this.rp;
	}

	public RD Rd() {
		return this.rd;
	}
	
	public DItem Parent() {
		String rd = DSubs.getParent(this.rd.s);
		return new DItem(true, this.st, new RD(rd));
	}
	public int compareTo(DItem o) {
		// System.out.println("compareTo called.");
		return this.Rp().s.compareToIgnoreCase(o.Rp().s);
	}
	public boolean equals(DItem o) {
		return this.Rp().s.equals(o.Rp().s);
	}
	@Override
	public int hashCode() {
		return (st.Vl().s + ":" + Rp().s).hashCode();
	}
}
