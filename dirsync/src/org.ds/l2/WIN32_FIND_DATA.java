package org.ds.l2;

import org.bridj.BridJ;
import org.bridj.Pointer;
import org.bridj.Pointer.StringType;
import org.bridj.StructObject;
import org.bridj.ann.Array;
import org.bridj.ann.Field;

public class WIN32_FIND_DATA extends StructObject {
	static {
		BridJ.register();
	}

	@Field(0)
	public int dwFileAttributes() {
		return this.io.getIntField(this, 0);
	}

	@Field(1)
	public int ctLow() {
		return this.io.getIntField(this, 1);
	}

	@Field(2)
	public int ctHigh() {
		return this.io.getIntField(this, 2);
	}

	@Field(3)
	public int latLow() {
		return this.io.getIntField(this, 3);
	}

	@Field(4)
	public int latHigh() {
		return this.io.getIntField(this, 4);
	}

	@Field(5)
	public int lwtLow() {
		return this.io.getIntField(this, 5);
	}

	@Field(6)
	public int lwtHigh() {
		return this.io.getIntField(this, 6);
	}

	@Field(7)
	public int nFileSizeHigh() {
		return this.io.getIntField(this, 7);
	}

	@Field(8)
	public int nFileSizeLow() {
		return this.io.getIntField(this, 8);
	}

	@Field(9)
	public int dwReserved0() {
		return this.io.getIntField(this, 9);
	}

	@Field(10)
	public int dwReserved1() {
		return this.io.getIntField(this, 10);
	}

	/** C type : short[260] */
	@Array({ 260 })
	@Field(11)
	public Pointer<Short> cFileName() {
		return this.io.getPointerField(this, 11);
	}

	/** C type : short[14] */
	@Array({ 14 })
	@Field(12)
	public Pointer<Short> cAlternateFileName() {
		return this.io.getPointerField(this, 12);
	}

	public String fileName() {
		return cFileName().getStringAtOffset(0L, StringType.WideC, null);
	}
	public String altFileName() {
		return cAlternateFileName().getStringAtOffset(0L, StringType.WideC, null);
	}
}
