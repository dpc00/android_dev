package org.ds.l3;

public class Success<T, E> extends Try<T, E> {
	public Success(T value) {
		this.value = value;
	}

	private final T value;

	public T get() {
		return this.value;
	}

	public E getE() {
		return null;
	}

	public boolean isFailure() {
		return false;
	}

	public boolean isSuccess() {
		return true;
	}
}
