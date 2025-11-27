package org.ds.event;

import javafx.event.Event;
import javafx.event.EventTarget;

public interface EventSource {
	void addEventTarget(EventTarget et);

	void fireEvent2(Event e);

	void subscribeTo(EventSource es);
}
