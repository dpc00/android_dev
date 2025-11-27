package org.ds.types;

import java.util.concurrent.atomic.AtomicReference;

import javafx.application.Platform;
import javafx.beans.value.WritableValue;

public class Updatable<T> {
	private T v;
	private AtomicReference<T> ar;
	public WritableValue<T> p;

	public Updatable(T v, WritableValue<T> p) {
		this.v = v;
		this.ar = new AtomicReference<>();
		this.p = p;
	}

	public void spawnEvent() {
		Runnable r = () -> {
			try {
				Updatable.this.p.setValue(Updatable.this.ar.getAndSet(null));
			} catch (Exception ex) {
				ex.printStackTrace();
			}
		};
		Platform.runLater(r);
	}

	public T getV() {
		return this.v;
	}

	public void setV(T v) {
		this.v = v;
		if (
			!this.p.getValue().equals(this.v) &&
				this.ar.getAndSet(v) == null
			) {
			spawnEvent();
		}
	}

	public boolean isDirty() {
		return this.p.getValue().equals(this.v);
	}

	public void update() {
		this.p.setValue(this.ar.getAndSet(null));
	}
}
