package org.ds.l2;

import java.io.IOException;

import org.bridj.BridJ;
import org.bridj.CRuntime;
import org.bridj.Pointer;
import org.bridj.Pointer.StringType;
import org.bridj.ann.Library;
import org.bridj.ann.Ptr;
import org.bridj.ann.Runtime;

@Library("kernel32")
@Runtime(CRuntime.class)
public class Kernel32 {
	static {
		BridJ.register();
	}

	public static native int CancelIo(long h);

	public static native int CancelIoEx(long h, @Ptr long ol);

	public static native int CloseHandle(long h);

	public static native int CopyFileW(@Ptr long src, @Ptr long dst, boolean failIfExists);

	public static native long CreateFileW(@Ptr long fp, int da, int sm, @Ptr long sa, int cd, int fa, long htf);

	public static native int DeleteFileW(@Ptr long dst);

	public static native int FindClose(long h);

	public static native long FindFirstFileW(@Ptr long fspec, @Ptr long deso);

	public static native int FindNextFileW(long h, @Ptr long deso);

	public static native int FormatMessageW(int dwFlags, @Ptr long source, int gle, int langid, @Ptr long buffer, int bsize, @Ptr long args);

	public static native int GetFileAttributesW(@Ptr long fspec);

	public static native int GetLastError();

	public static native int ReadDirectoryChangesW(long h, @Ptr long buffer, int blen, boolean subtree, int nf,
		@Ptr long bret, @Ptr long ovl, @Ptr long cr);

	public static native int RemoveDirectoryW(@Ptr long dst);

	@SuppressWarnings("unchecked")
	public static int attributes(String fspec) {
		// System.out.println("fileExists " + fspec);
		Pointer<Short> fspec_native = (Pointer<Short>) Pointer.pointerToString(fspec, StringType.WideC, WC.CHARSET);
		// System.out.println(fspec_native);
		return GetFileAttributesW(Pointer.getPeer(fspec_native));
	}

	public static boolean isOther(int fa) {
		return (fa & (WC.FA_DEVICE | WC.FA_REPARSE_POINT)) != 0;
	}

	public static boolean file_exists(String fspec) {
		int fa = attributes(fspec);
		if (fa == WC.INVALID_FILE_ATTRIBUTES) {
			return false;
		}
		if (isOther(fa) || ((fa & WC.FA_DIRECTORY) != 0)) {
			return false;
		}
		return true;
	}

	public static boolean dir_exists(String fspec) {
		// System.out.println("dirExists " + fspec);
		int fa = attributes(fspec);
		if (fa == WC.INVALID_FILE_ATTRIBUTES) {
			return false;
		}
		if (isOther(fa) || ((fa & WC.FA_DIRECTORY) == 0)) {
			return false;
		}
		return true;
	}

	@SuppressWarnings("unchecked")
	public static int copy_file(String src, String dst) throws IOException {
		Pointer<Short> src_native = (Pointer<Short>)Pointer.pointerToString(src, StringType.WideC, WC.CHARSET);
		Pointer<Short> dst_native = (Pointer<Short>)Pointer.pointerToString(dst, StringType.WideC, WC.CHARSET);
		int rc = CopyFileW(Pointer.getPeer(src_native), Pointer.getPeer(dst_native), false);

		if (rc == 0) {
			int we = GetLastError();
			if (we != 0) {
				// if(we != WC.WE_FILE_NOT_FOUND) {
				throw new IOException("Windows Error: copy_file: " + we + " " + src + " to " + dst);
				// }
			}
		}
		return rc;
	}

	@SuppressWarnings("unchecked")
	public static int delete_file(String dst) throws IOException {
		Pointer<Short> dst_native = (Pointer<Short>)Pointer.pointerToString(dst, StringType.WideC, WC.CHARSET);
		int rc = DeleteFileW(Pointer.getPeer(dst_native));

		if (rc == 0) {
			int we = GetLastError();
			if (we != 0) {
				// if(we != WC.WE_FILE_NOT_FOUND) {
				throw new IOException("Windows Error: delete_file: " + we + " " + dst);
				// }
			}
		}
		return rc;
	}

	public static int remove_directory(String dst) throws IOException {
		@SuppressWarnings("unchecked")
		Pointer<Short> dst_native = (Pointer<Short>)Pointer.pointerToString(dst, StringType.WideC, WC.CHARSET);
		int rc = RemoveDirectoryW(Pointer.getPeer(dst_native));

		if (rc == 0) {
			int we = GetLastError();
			if (we != 0) {
				// if(we != WC.WE_FILE_NOT_FOUND) {
				throw new IOException("Windows Error: copy_file: " + we + " " + dst);
				// }
			}
		}
		return rc;
	}

	public static String format_message(int gle) {
		Pointer<Character> buffer = Pointer.allocateChars(256);
		int rv = FormatMessageW(WC.FORMAT_MESSAGE_FROM_SYSTEM, Pointer.getPeer(Pointer.NULL), gle, 0, Pointer.getPeer(buffer), (int) (buffer.getValidBytes()), Pointer.getPeer(Pointer.NULL));
		if(rv != 0) {
			return buffer.getCString().trim();
		}
		else {
			gle = GetLastError();
			Exception e = new Exception("format_message: " + gle);
			e.printStackTrace();
			return "";
		}
	}

}
