package org.ds.l3;

public class Failure<T, E> extends Try<T, E> {
	public Failure(E ex) {
		this.ex = ex;
	}

	private final E ex;

	public T get() {
		return null;
	}

	public E getE() {
		return this.ex;
	}

	public boolean isFailure() {
		return true;
	}

	public boolean isSuccess() {
		return false;
	}
}
