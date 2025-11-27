import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.file.Files;
import java.nio.file.LinkOption;
import java.nio.file.Path;
import java.nio.file.attribute.BasicFileAttributes;
import java.nio.file.attribute.FileTime;
import java.util.Set;
import java.util.concurrent.TimeUnit;
import java.util.zip.CRC32;

/* import org.bridj.BridJ;
import org.bridj.Pointer;
import org.bridj.StructObject;
import org.bridj.Pointer.StringType;
 */
 
public class DE implements Comparable<DE> {
	public String fname;
	public long mtime; // 8 bytes; in seconds
	public long size; // 8
	public boolean isdir;
	public boolean isfile;

	public int compareTo(DE o) {
		// System.out.println("compareTo called.");
		return fname.compareToIgnoreCase(o.fname);
	}

	public int hashCode() {
		return fname.hashCode();
	}

	public boolean equals(Object o) {
		if (o instanceof DE) {
			// System.out.println("equals called.");
			DE de = (DE) o;
			return fname.equalsIgnoreCase(de.fname) && size == de.size && de.mtime - mtime <= 2;
		}
		return false;
	}

	public String toString() {
		String s = fname + " ";
		s += mtime + " ";
		s += size + " ";
		s += isdir + " ";
		s += isfile;
		s += '\n';
		return s;
	}

	public DE(Path p) { // the java way to get file attributes; appears to be slower
//		System.out.println(p.getClass().getName());
//		sun.nio.fs.WindowsPath.WindowsPathWithAttributes q = (sun.nio.fs.WindowsPath.WindowsPathWithAttributes)p;
//		System.out.println(q.ref.getClass().getName());
//		System.out.println(q.ref.referrent.getClass().getName());
		
		fname = p.getFileName().toString();
		try {
			// this should extract from variable p itself which on Windows appears to already have the data
			BasicFileAttributes bfa = Files.readAttributes(p, BasicFileAttributes.class, LinkOption.NOFOLLOW_LINKS);
			size = bfa.size();
			isdir = bfa.isDirectory();
			isfile = bfa.isRegularFile();
			FileTime lmt = bfa.lastModifiedTime();
			mtime = lmt.to(TimeUnit.SECONDS);
		} catch (IOException e) {
			System.out.println(e.toString());
		}
	}

	public DE(WIN32_FIND_DATA deso) { // from windows via WindowsScanDir (is faster)
		fname = deso.fileName();
		size = ((long) deso.nFileSizeHigh() << 32) | ((long) deso.nFileSizeLow() & 0xFFFFFFFFL);
		int fa = deso.dwFileAttributes();
		if (!(((fa & (WC.FA_DEVICE | WC.FA_REPARSE_POINT)) != 0) && (deso.dwReserved0() == WC.IO_REPARSE_TAG_SYMLINK))) {
			isdir = ((fa & WC.FA_DIRECTORY) != 0);
			isfile = ((fa & WC.FA_DIRECTORY) == 0);
		}
		mtime = ((((long) deso.lwtHigh() << 32) | ((long) deso.lwtLow() & 0xFFFFFFFFL))
				- WC.HUNDREDNANOSECONDS_BETWEEN_EPOCHS) / 10000000L;
		// System.out.println(fname + " " + mtime);
	}

	public long crc32() {
		byte[] bytes = new byte[Long.BYTES + Long.BYTES];
		ByteBuffer bb = ByteBuffer.wrap(bytes);
		bb.putLong(mtime);
		bb.putLong(size);
		bb.rewind();
		CRC32 x = new CRC32();
		x.update(fname.getBytes());
		x.update(bb);
		return x.getValue();
	}

	public static long crc32list(Set<DE> l1) {
		byte[] bytes = new byte[l1.size() * Long.BYTES];
		ByteBuffer bb = ByteBuffer.wrap(bytes);
		for (DE de : l1) {
			long crc = de.crc32();
			bb.putLong(crc);
		}
		bb.rewind();
		CRC32 x = new CRC32();
		x.update(bb);
		long ret = x.getValue();
		return ret;
	}
}
