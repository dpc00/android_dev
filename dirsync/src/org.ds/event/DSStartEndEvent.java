package org.ds.event;

import org.ds.l4.DirSyncer;
import org.ds.types.FN;
import org.ds.types.RD;

import javafx.event.EventTarget;
import javafx.event.EventType;

public class DSStartEndEvent extends DSEvent {
	/**
	 *
	 */
	private static final long serialVersionUID = -2787770666228576527L;

	public DSStartEndEvent(Object src, EventTarget tgt, EventType<AEvent> et, DirSyncer ds, RD rd, FN fn) {
		super(src, tgt, et, new DSEData(ds, rd, fn));
	}
}
