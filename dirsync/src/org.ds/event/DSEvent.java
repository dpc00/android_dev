package org.ds.event;

import javafx.event.EventTarget;
import javafx.event.EventType;

public class DSEvent extends AEvent {
	/**
	 *
	 */
	private static final long serialVersionUID = -2430298929322323749L;

	public DSEvent(Object src, EventTarget tgt, EventType<AEvent> et, DSEData d) {
		super(src, tgt, et, d);
	}

//	public DSEvent(Object src, EventTarget tgt, EventType<AEvent> et) {
//		super(src, tgt, et);
//	}
}
