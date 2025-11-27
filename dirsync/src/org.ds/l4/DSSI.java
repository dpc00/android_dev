package org.ds.l4;

import org.ds.cn.ChangeRecord;
import org.ds.l3.CC;
import org.ds.types.ST;

public class DSSI {
	public final ST st;
	public final CC cc;

	public DSSI(ST st, CC cc, ChangeRecord ar) {
		this.st = st;
		if (cc == null) {
			cc = new CC(st, ar);
		}
		this.cc = cc;
	}

}
