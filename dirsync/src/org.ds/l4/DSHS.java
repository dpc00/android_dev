package org.ds.l4;

import java.util.HashSet;

import org.ds.app.DirSyncApp;

public class DSHS extends HashSet<DirSyncer> {
	private static final long serialVersionUID = 1634476246444983516L;

	public DSHS() {
		for (DSTI dsti : DirSyncApp.it.dsl.d) {
			add(dsti.ds);
		}
	}

	public DSHS(DirSyncer ds) {
		add(ds);
	}
}
