package org.ds.l2;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.AccessDeniedException;
import java.nio.file.NotDirectoryException;

import org.bridj.Pointer;
import org.bridj.Pointer.StringType;

public class WindowsScanDir implements IScanDir {
	public long ffHandle;
	public static Pointer<WIN32_FIND_DATA> deso = Pointer.allocate(WIN32_FIND_DATA.class);

	public void findclose() {
		if (ffHandle != WC.INVALID_HANDLE_VALUE) {
			int ret = Kernel32.FindClose(ffHandle);
			if (ret == 0) {
				int we = Kernel32.GetLastError();
				// System.out.println("we: " + we);
				if (we == 0) {
					return;
				}
				else {
					Exception e = new IOException("unexpected WindowsError in findclose:" + we);
					e.printStackTrace();
				}
			}
			ffHandle = WC.INVALID_HANDLE_VALUE;
			// deso.release();
		}
		else {
			System.out.println("ffHandle INVALID in findclose");
		}
	}

	@SuppressWarnings("unchecked")
	public DE findfirst(String fspec) throws IOException {
		// System.out.println("fspec: " + fspec);
		String fspec2 = fspec;
		if (fspec2.endsWith(":") || fspec2.endsWith("\\")) {
			fspec2 += "*";
		} else {
			fspec2 += "\\*";
		}
		// System.out.println("fspec2: " + fspec2);
		Pointer<Short> fspec_native = (Pointer<Short>)Pointer.pointerToString(fspec2, StringType.WideC, WC.CHARSET);
		// System.out.println("fspec_native: " + fspec_native);
		synchronized(deso) {
			ffHandle = Kernel32.FindFirstFileW(Pointer.getPeer(fspec_native), Pointer.getPeer(deso));
			// System.out.println("ffHandle: " + ffHandle);
			if (ffHandle == WC.INVALID_HANDLE_VALUE) {
//				System.out.println("WC.INVALID_HANDLE_VALUE");
				int we = Kernel32.GetLastError();
//				System.out.println("we: " + we);
				if (we != 0) {
					if (we == WC.WE_FILE_NOT_FOUND ) {
						throw new FileNotFoundException(fspec);
					} else if(we == WC.WE_PATH_NOT_FOUND) {
						throw new NotDirectoryException(fspec);
					} else if(we == WC.WE_ACCESS_DENIED) {
						throw new AccessDeniedException(fspec);
					}
					else
						throw new IOException("unexpected WindowsError in findfirst(" + fspec + "):" + we);
				} else
					return null;
			}
			return DE.fromDESO(deso.get());
		}
	}

	public DE findnext() throws IOException {
		synchronized(deso) {
			int ret = Kernel32.FindNextFileW(ffHandle, Pointer.getPeer(deso));
			// System.out.println("ret: " + ret);
			if (ret == 0) {
				int we = Kernel32.GetLastError();
				// System.out.println("we: " + we);
				if (we == WC.WE_NO_MORE_FILES || we == 0) {
//					findclose();
					return null;
				}
				else throw new IOException("unexpected WindowsError in findnext:" + we);
			}
			return DE.fromDESO(deso.get());
		}
	}
}
