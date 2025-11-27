package org.ds.l4;

import java.util.HashSet;

public class EHS extends HashSet<Throwable> {
	/**
	 *
	 */
	private static final long serialVersionUID = -6256053259532387554L;

	public EHS() {

	}

	public EHS(Throwable e) {
		if (e != null)
			add(e);
	}
}
