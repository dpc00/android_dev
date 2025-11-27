package org.ds.event;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

//import com.sun.javafx.event.EventDispatchChainImpl;

import javafx.event.Event;
import javafx.event.EventDispatchChain;
import javafx.event.EventHandler;
import javafx.event.EventTarget;
import javafx.event.EventType;

public abstract class AbstractEventTarget<T extends Event> implements EventTarget, EventSource {
	private final Map<EventType<T>, Collection<EventHandler<T>>> handlers = new HashMap<>();

//	public EventDispatchChainImpl edci = new EventDispatchChainImpl();

	// EventSource implementation
	private ArrayList<EventTarget> etl = new ArrayList<>();

	public final void addEventHandler(final EventType<T> et, final EventHandler<T> eh) {
		Collection<EventHandler<T>> rv = this.handlers.computeIfAbsent(et, tEventType -> new ArrayList<>());
		rv.add(eh);
	}

	public void addEventTarget(EventTarget et) {
		if (!this.etl.contains(et)) {
			this.etl.add(et);
		} else {
			throw new IllegalArgumentException("excess event target addition");
		}
	}

	@Override
	public final EventDispatchChain buildEventDispatchChain(final EventDispatchChain tail) {
		return tail.prepend(this::dispatchEvent);
	}

	public void fireEvent2(Event e1) {
		for (EventTarget et : this.etl) {
			Event e2 = e1.copyFor(e1.getSource(), et);
			Event.fireEvent(e2.getTarget(), e2);
		}
	}

	public final void removeEventHandler(final EventType<T> eventType, final EventHandler<? super T> eventHandler) {
		this.handlers.computeIfPresent(eventType, (k, v) -> {
			v.remove(eventHandler);
			return v.isEmpty() ? null : v;
		});
	}

	public void subscribeTo(EventSource es) {
		es.addEventTarget(this);
	}
	// End EventSource implementation

	private Event dispatchEvent(Event event, @SuppressWarnings("unused") EventDispatchChain evdc) {
		// go through type hierarchy and trigger all handlers
		EventType<? extends Event> type = event.getEventType();
		do {
			handleEvent(event, this.handlers.get(type));
			type = type.getSuperType();
		} while (type != null);
		return event;
	}

	@SuppressWarnings("unchecked")
	private void handleEvent(final Event event, final Collection<EventHandler<T>> handlers) {
		if (handlers != null) {
			handlers.forEach(handler -> handler.handle((T) event));
		}
	}
}
