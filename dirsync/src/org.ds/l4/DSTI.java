package org.ds.l4;

import org.ds.l3.CC;
import org.ds.types.ST;

public class DSTI implements Comparable<DSTI> {
	public ST st;
	public DirSyncer ds;
	public DirSyncRunner runner;
	public final CC cc;

	public DSTI(ST st, CC cc) {
		this.st = st;
		if (cc == null) {
			cc = new CC(st, null);
		}
		this.cc = cc;
	}

	public int compareTo(DSTI that) {
		return this.st.Fp().s.compareTo(that.st.Fp().s);
	}

	@Override
	public boolean equals(Object o2) {
		return o2 instanceof DSTI && this.st.Fp().s.equals(((DSTI) o2).st.Fp().s);
	}

	@Override
	public int hashCode() {
		return this.st.Fp().s.hashCode();
	}
}
