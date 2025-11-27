package org.ds.event;

import org.ds.l3.CC;
import org.ds.l4.DirSyncer;
import org.ds.types.FN;
import org.ds.types.RD;
import org.ds.types.RT;

public class DSEData {
	public DSEData(CC cc, RT rt, RD rd, long size) {
		this.rt = rt;
		this.rd = rd;
		this.size = size;
		this.cc = cc;
	}
	public DSEData(DirSyncer ds, RD rd, FN fn) {
		this.ds = ds;
		this.rd = rd;
		this.fn = fn;
	}
	public DSEData(DirSyncer ds, RD rd, FN fn, Throwable e) {
		this.ds = ds;
		this.rd = rd;
		this.fn = fn;
		this.e = e;
	}
	public DSEData(RD rd) {
		this.rd = rd;
	}
	public DSEData(RD rd, FN fn) {
		this.rd = rd;
		this.fn = fn;
	}
	public DSEData(RD rd, FN fn, long size) {
		this.rd = rd;
		this.fn = fn;
		this.size = size;
	}
	public DSEData(RD rd, FN fn, Throwable e) {
		this.rd = rd;
		this.fn = fn;
		this.e = e;
	}

	public DirSyncer ds;

	public RT rt;

	public RD rd;

	public FN fn;

	public long size;

	public Throwable e;

	public CC cc;
}
