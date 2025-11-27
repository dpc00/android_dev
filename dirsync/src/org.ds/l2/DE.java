package org.ds.l2;

import java.io.IOException;
import java.io.Serializable;
import java.lang.ref.WeakReference;
import java.lang.reflect.Field;
import java.lang.reflect.InaccessibleObjectException;
import java.nio.ByteBuffer;
import java.nio.file.Files;
import java.nio.file.LinkOption;
import java.nio.file.Path;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.Collection;
import java.util.concurrent.TimeUnit;
import java.util.zip.CRC32;

//import org.ds.l2.WC;
//import org.ds.l1.WIN32_FIND_DATA;

public class DE implements Comparable<DE>, Serializable {
	private final static byte[] bytes = new byte[Long.BYTES * 2];
	private final static ByteBuffer bb = ByteBuffer.wrap(bytes);

	private DE(String fname, long mtime, long size, boolean isdir, boolean isfile) {
		this.fname = fname;
		this.mtime = mtime;
		this.size = size;
		this.isdir = isdir;
		this.isfile = isfile;
	}
	public final String fname;
	private final long mtime; // 8 bytes; in seconds
	public final long size; // 8
	public final boolean isdir;
	public final boolean isfile;

	public static long byteslist(Collection<DE> l1) {
		long tsize = 0;
		for (DE de : l1) {
			tsize += de.size;
		}
		return tsize;
	}

	public static long crc32list(Collection<DE> l1) {
		CRC32 x = new CRC32();
		for (DE de : l1) {
			x.update(de.fname.getBytes());
			synchronized (bb) {
				bb.rewind();
				bb.putLong(de.mtime);
				bb.putLong(de.size);
				bb.rewind();
				x.update(bb);
			}
		}
		return x.getValue();
	}

//	public DE(WIN32_FIND_DATA deso) { // from windows via WindowsScanDir (is faster)
//		fname = deso.fileName();
//		size = ((long) deso.nFileSizeHigh() << 32) | ((long) deso.nFileSizeLow() & 0xFFFFFFFFL);
//		int fa = deso.dwFileAttributes();
//		if (!(((fa & (WC.FA_DEVICE | WC.FA_REPARSE_POINT)) != 0) && (deso.dwReserved0() == WC.IO_REPARSE_TAG_SYMLINK))) {
//			isdir = ((fa & WC.FA_DIRECTORY) != 0);
//			isfile = ((fa & WC.FA_DIRECTORY) == 0);
//		}
//		mtime = ((((long) deso.lwtHigh() << 32) | ((long) deso.lwtLow() & 0xFFFFFFFFL))
//			- WC.HUNDREDNANOSECONDS_BETWEEN_EPOCHS) / 10000000L;
//		// System.out.println(fname + " " + mtime);
//	}

	public static DE fromDESO(WIN32_FIND_DATA deso) { // from windows via
																		// WindowsScanDir (is
		// faster)
		String fname = deso.fileName();
		long size = ((long) deso.nFileSizeHigh() << 32) | ((long) deso.nFileSizeLow() & 0xFFFFFFFFL);
		int fa = deso.dwFileAttributes();
		boolean b1 = (fa & (WC.FA_DEVICE | WC.FA_REPARSE_POINT)) != 0;
		boolean b2 = ((((long) deso.dwReserved1() << 32)
				| ((long) deso.dwReserved0() & 0xFFFFFFFFL)) == WC.IO_REPARSE_TAG_SYMLINK);
		boolean isdir = false;
		boolean isfile = false;
		if (!b1 && !b2) {
			isdir = (fa & WC.FA_DIRECTORY) != 0;
			isfile = (fa & WC.FA_DIRECTORY) == 0;
		}
		long mtime = ((((long) deso.lwtHigh() << 32) | ((long) deso.lwtLow() & 0xFFFFFFFFL))
				- WC.HUNDREDNANOSECONDS_BETWEEN_EPOCHS) / 100L;
		// System.out.println(fname + " " + mtime);
		return new DE(fname, mtime, size, isdir, isfile);
	}

	public static DE fromPath(Path p) {
		// System.out.println(rt.getClass().getName());
//			
//	static {
//		Package p1 = java.lang.Package.getPackage("sun.nio.fs.WindowsPath");
//		Package p2 = java.lang.Package.getPackage("sun.nio.fs.WindowsPath.WindowsPathWithAttributes");
//	}
// sun.nio.fs.WindowsPath.WindowsPathWithAttributes q;
		// q = (WindowsPath.WindowsPathWithAttributes)rt;
		// System.out.println(q.ref.getClass().getName());
		// System.out.println(q.ref.referrent.getClass().getName());
		// this should extract from variable rt itself which on Windows appears
		// to already have the data

		String fname = p.getFileName().toString();
		try {
			BasicFileAttributes bfa = null;
//			try {
//				Field f = p.getClass().getDeclaredField("ref");
//				f.setAccessible(true);
//				try {
//					WeakReference<BasicFileAttributes> bfar = (WeakReference<BasicFileAttributes>)f.get(p);
//					if (bfar.get() != null) {
//						bfa = bfar.get();
//					}
//				}
//				catch(IllegalAccessException e) {
////					e.printStackTrace();
//				}
//			}
//			catch(InaccessibleObjectException | NoSuchFieldException e) {
////				e.printStackTrace();
//			}
			if(bfa == null) {
//				System.out.println("calling usual Files.readAttributes");
				bfa = Files.readAttributes(p, BasicFileAttributes.class, LinkOption.NOFOLLOW_LINKS);
			}
			long size = bfa.size();
			long mtime = bfa.lastModifiedTime().to(TimeUnit.NANOSECONDS);
			boolean isdir = bfa.isDirectory();
			boolean isfile = bfa.isRegularFile();
			return new DE(fname, mtime, size, isdir, isfile);
		} catch (IOException e) {
			System.out.println(e.toString());
			return null;
		}
	}

	public int compareTo(DE o) {
		// System.out.println("compareTo called.");
		return this.fname.compareToIgnoreCase(o.fname);
	}

	public boolean equals(DE o) {
		return crc32() == o.crc32();
	}

	public int hashCode() {
		return this.fname.hashCode();
	}

	public boolean isUp2DateWith(Object o) {
		if (o instanceof DE) {
			// System.out.println("equals called.");
			DE de = (DE) o;
			boolean b1 = Math.abs(this.mtime - de.mtime) <= 2e9;
			if (!b1)
				return false;
			boolean b2 = this.size == de.size;
			if (!b2)
				return false;
		}
		return true;
	}

	public String toString() {
		String s = "\"" + this.fname + "\", ";
		s += this.mtime + ", ";
		s += this.size + ", ";
		s += (this.isdir ? "(dir)" : "");
		s += (this.isfile ? "(file)" : "");
		return s;
	}

	private long crc32() {
		CRC32 x = new CRC32();
		x.update(this.fname.getBytes());
		bb.rewind();
		bb.putLong(this.mtime);
		bb.putLong(this.size);
		bb.rewind();
		x.update(bb);
		return x.getValue();
	}
}
