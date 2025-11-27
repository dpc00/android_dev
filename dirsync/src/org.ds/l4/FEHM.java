package org.ds.l4;

import java.util.HashMap;

import org.ds.types.FN;

public class FEHM extends HashMap<FN, EHS> {
	/**
	 *
	 */
	private static final long serialVersionUID = 2326726139783343926L;

	public FEHM() {
	}

	public FEHM(FN fn) {
		if (fn != null)
			put(fn, new EHS());
	}

	public FEHM(FN fn, Throwable e) {
		if (fn != null)
			put(fn, new EHS(e));
	}
}
