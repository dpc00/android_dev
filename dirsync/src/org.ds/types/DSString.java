package org.ds.types;

import java.util.stream.IntStream;

public abstract class DSString implements Comparable<DSString>, CharSequence {
	DSString(String s) {
		this.s = s;
	}

	public final String s;

	private int hash;

	@Override
	public char charAt(int index) {
		return this.s.charAt(index);
	}

	@Override
	public IntStream chars() {
		return this.s.chars();
	}

	@Override
	public IntStream codePoints() {
		return this.s.codePoints();
	}

	public int compareTo(DSString other) {
		return this.s.compareTo(other.s);
	}

	public boolean equals(Object o) {
		if (o instanceof DSString) {
			return this.s.equals(((DSString) o).s);
		}
		return false;
	}

	public int hashCode() {
		int h = this.hash;
		if (h == 0) {
			h = this.s.hashCode();
			this.hash = h;
		}
		return h;
	}

	@Override
	public int length() {
		return this.s.length();
	}

	@Override
	public CharSequence subSequence(int start, int end) {
		return this.s.substring(start, end);
	}

	@Override
	public String toString() {
		return this.s;
	}
}
