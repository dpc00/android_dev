package org.ds.l3;

public abstract class Try<T, E> {
	Try() {
	}

	public abstract T get();

	public abstract E getE();

	public abstract boolean isFailure();

	public abstract boolean isSuccess();
}
