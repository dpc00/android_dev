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

	@Field(0)
	public WIN32_FIND_DATA dwFileAttributes(int dwFileAttributes) {
		this.io.setIntField(this, 0, dwFileAttributes);
		return this;
	}

	public final int dwFileAttributes_$eq(int dwFileAttributes) {
		dwFileAttributes(dwFileAttributes);
		return dwFileAttributes;
	}

	@Field(1)
	public int ctLow() {
		return this.io.getIntField(this, 1);
	}

	@Field(1)
	public WIN32_FIND_DATA ctLow(int ctLow) {
		this.io.setIntField(this, 1, ctLow);
		return this;
	}

	public final int ctLow_$eq(int ctLow) {
		ctLow(ctLow);
		return ctLow;
	}

	@Field(2)
	public int ctHigh() {
		return this.io.getIntField(this, 2);
	}

	@Field(2)
	public WIN32_FIND_DATA ctHigh(int ctHigh) {
		this.io.setIntField(this, 2, ctHigh);
		return this;
	}

	public final int ctHigh_$eq(int ctHigh) {
		ctHigh(ctHigh);
		return ctHigh;
	}

	@Field(3)
	public int latLow() {
		return this.io.getIntField(this, 3);
	}

	@Field(3)
	public WIN32_FIND_DATA latLow(int latLow) {
		this.io.setIntField(this, 3, latLow);
		return this;
	}

	public final int latLow_$eq(int latLow) {
		latLow(latLow);
		return latLow;
	}

	@Field(4)
	public int latHigh() {
		return this.io.getIntField(this, 4);
	}

	@Field(4)
	public WIN32_FIND_DATA latHigh(int latHigh) {
		this.io.setIntField(this, 4, latHigh);
		return this;
	}

	public final int latHigh_$eq(int latHigh) {
		latHigh(latHigh);
		return latHigh;
	}

	@Field(5)
	public int lwtLow() {
		return this.io.getIntField(this, 5);
	}

	@Field(5)
	public WIN32_FIND_DATA lwtLow(int lwtLow) {
		this.io.setIntField(this, 5, lwtLow);
		return this;
	}

	public final int lwtLow_$eq(int lwtLow) {
		lwtLow(lwtLow);
		return lwtLow;
	}

	@Field(6)
	public int lwtHigh() {
		return this.io.getIntField(this, 6);
	}

	@Field(6)
	public WIN32_FIND_DATA lwtHigh(int lwtHigh) {
		this.io.setIntField(this, 6, lwtHigh);
		return this;
	}

	public final int lwtHigh_$eq(int lwtHigh) {
		lwtHigh(lwtHigh);
		return lwtHigh;
	}

	@Field(7)
	public int nFileSizeHigh() {
		return this.io.getIntField(this, 7);
	}

	@Field(7)
	public WIN32_FIND_DATA nFileSizeHigh(int nFileSizeHigh) {
		this.io.setIntField(this, 7, nFileSizeHigh);
		return this;
	}

	public final int nFileSizeHigh_$eq(int nFileSizeHigh) {
		nFileSizeHigh(nFileSizeHigh);
		return nFileSizeHigh;
	}

	@Field(8)
	public int nFileSizeLow() {
		return this.io.getIntField(this, 8);
	}

	@Field(8)
	public WIN32_FIND_DATA nFileSizeLow(int nFileSizeLow) {
		this.io.setIntField(this, 8, nFileSizeLow);
		return this;
	}

	public final int nFileSizeLow_$eq(int nFileSizeLow) {
		nFileSizeLow(nFileSizeLow);
		return nFileSizeLow;
	}

	@Field(9)
	public int dwReserved0() {
		return this.io.getIntField(this, 9);
	}

	@Field(9)
	public WIN32_FIND_DATA dwReserved0(int dwReserved0) {
		this.io.setIntField(this, 9, dwReserved0);
		return this;
	}

	public final int dwReserved0_$eq(int dwReserved0) {
		dwReserved0(dwReserved0);
		return dwReserved0;
	}

	@Field(10)
	public int dwReserved1() {
		return this.io.getIntField(this, 10);
	}

	@Field(10)
	public WIN32_FIND_DATA dwReserved1(int dwReserved1) {
		this.io.setIntField(this, 10, dwReserved1);
		return this;
	}

	public final int dwReserved1_$eq(int dwReserved1) {
		dwReserved1(dwReserved1);
		return dwReserved1;
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

	public WIN32_FIND_DATA() {
		super();
	}

	public WIN32_FIND_DATA(Pointer<WIN32_FIND_DATA> pointer) {
		super(pointer);
	}

	public String fileName() {
		return cFileName().getStringAtOffset(0L, StringType.WideC, null);
	}
	public String altFileName() {
		return cAlternateFileName().getStringAtOffset(0L, StringType.WideC, null);
	}
}
