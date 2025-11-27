package org.ds.l4;

import java.util.concurrent.ConcurrentHashMap;

import org.ds.types.RD;

public class CNHM extends ConcurrentHashMap<RD, CNHM.Value> {
	public static class Value {
		public DSHS dsl;
		public FEHM fl;

		public Value(DSHS dsl, FEHM fl) {
			this.dsl = dsl;
			this.fl = fl;
		}
	}
	private static final long serialVersionUID = 3599913235505221873L;
}
