package org.ds.event;

import javafx.event.Event;
import javafx.event.EventTarget;
import javafx.event.EventType;

/**
 * @author libraryuser
 */

@SuppressWarnings("serial")
public class AEvent extends Event {
	AEvent(Object src, EventTarget tgt, EventType<AEvent> et) {
		super(src, tgt, et);
	}
	AEvent(Object src, EventTarget tgt, EventType<AEvent> et, DSEData d) {
		super(src, tgt, et);
		this.d = d;
	}

	public long etime = System.nanoTime();

	public DSEData d;

	public boolean isSubTypeOf(EventType<? extends Event> e) {
		EventType<? extends Event> type = getEventType();
		do {
			if (type.equals(e))
				return true;
			type = type.getSuperType();
		} while (type != null);
		return false;
	}
}
