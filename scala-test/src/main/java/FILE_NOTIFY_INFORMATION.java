import org.bridj.Pointer;
import org.bridj.Pointer.StringType;
import org.bridj.StructObject;
// import org.bridj.StructUtils;
import org.bridj.ann.Array;
import org.bridj.ann.Field;

public class FILE_NOTIFY_INFORMATION extends StructObject {
	@Field(0)
	public int size() {
		return this.io.getIntField(this, 0);
	}

	@Field(1)
	public int action() {
		return this.io.getIntField(this, 1);
	}

	@Field(2)
	public int name_len() {
		return this.io.getIntField(this, 2);
	}

	@Array({ 1 })
	@Field(3)
	@SuppressWarnings("deprecation")
	public Pointer<Short> name() {
		Pointer<Short> rv = this.io.getPointerField(this, 3);
		return rv.withoutValidityInformation();
	}
	
	public static final int LENGTH = 6 + 32767*2 + 2;
	
	
	public String path() {
		Pointer<Short> pname = name();
		// pname.validElements(name_len() >> 1 + 1);
		long zsi = name_len() >> 1;
		short ss = pname.getShortAtIndex(zsi);
		pname.setShortAtIndex(zsi, (short)0);
		String rv = pname.getStringAtOffset(0L, StringType.WideC, null);
		pname.setShortAtIndex(zsi, ss);
		// pname.release();
		return rv;
	}
}
