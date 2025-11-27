package org.ds.event;

import org.ds.types.RD;

import javafx.event.EventTarget;
import javafx.event.EventType;

public class AREvent extends AEvent {
	/**
	 *
	 */
	private static final long serialVersionUID = 922786724137289100L;

	public AREvent(Object src, EventTarget tgt, EventType<AEvent> et) {
		super(src, tgt, et);
	}

	public AREvent(Object src, EventTarget tgt, EventType<AEvent> et, RD rd) {
		super(src, tgt, et, new DSEData(rd));
	}
}
