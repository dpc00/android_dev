package org.ds.types;

import org.ds.l3.DSubs;

public class RD extends PCString {
	public RD(RD rd, FN fn) {
		this(DSubs.resolve(rd.s, fn.s));
	}

	public RD(String s) {
		super(s);
	}
}
