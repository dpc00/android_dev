package org.ds.event;

import org.ds.types.RD;

import javafx.event.EventTarget;
import javafx.event.EventType;

@SuppressWarnings("serial")
public class CNEvent extends AEvent {
	public CNEvent(Object src, EventTarget tgt, EventType<AEvent> et, RD rd) {
		super(src, tgt, et, new DSEData(rd));
	}
	public boolean isdir;

	public boolean isfile;
}
