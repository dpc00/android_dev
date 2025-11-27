package org.ds.types;

import org.ds.l3.DSubs;

public class FP extends PCString {
	public FP(FP fp, FN fn) {
		this(new RT(fp.s), fn);
	}

	public FP(FP fp, RD rd) {
		this(new RT(fp.s), rd);
	}

	public FP(FP fp, RD rd, FN fn) {
		this(new RT(fp.s), rd, fn);
	}

	public FP(RT rt, FN fn) {
		super(DSubs.resolve(rt.s, fn.s));
	}

	public FP(RT rt, RD rd) {
		super(DSubs.resolve(rt.s, rd.s));
	}

	public FP(RT rt, RD rd, FN fn) {
		super(DSubs.resolve(DSubs.resolve(rt.s, rd.s), fn.s));
	}

	public FP(String s) {
		super(s);
	}
}
