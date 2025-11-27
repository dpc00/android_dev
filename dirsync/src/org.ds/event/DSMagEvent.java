package org.ds.event;

import org.ds.types.FN;
import org.ds.types.RD;

import javafx.event.EventTarget;
import javafx.event.EventType;

public class DSMagEvent extends DSEvent {
	/**
	 *
	 */
	private static final long serialVersionUID = 422110494996305207L;

//	public DSMagEvent(Object src, EventTarget tgt, EventType<AEvent> et) {
//		super(src, tgt, et);
//	}

	public DSMagEvent(Object src, EventTarget tgt, EventType<AEvent> et, RD rd, FN fn, long size) {
		super(src, tgt, et, new DSEData(rd, fn, size));
	}

}
