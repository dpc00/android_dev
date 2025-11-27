package org.ds.event;

import org.ds.l4.DirSyncer;
import org.ds.types.FN;
import org.ds.types.RD;

import javafx.event.EventTarget;
import javafx.event.EventType;

public class DSErrorEvent extends DSEvent {
	/**
	 *
	 */
	private static final long serialVersionUID = -7278990265102047060L;

	public DSErrorEvent(Object src, EventTarget tgt, EventType<AEvent> et, DirSyncer ds, RD rd, FN fn, Throwable e) {
		super(src, tgt, et, new DSEData(ds, rd, fn, e));
	}

}
