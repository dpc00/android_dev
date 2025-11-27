import java.io.Closeable;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.function.Consumer;

import org.bridj.Pointer;
import org.bridj.Pointer.StringType;

public class ChangeNotifier implements Closeable {
	public CNI cni;
	public Consumer<CNI> cnf;
	public long hdir;
	public static final int nflags = WC.NF_FILE_NAME | WC.NF_DIR_NAME | WC.NF_ATTRIBUTES | WC.NF_SIZE | WC.NF_LAST_WRITE | WC.NF_CREATION | WC.NF_SECURITY;
	public String rt;
	public Thread cnt;

	public ChangeNotifier(String rt, Consumer<CNI> cnf) {
		this.rt = rt;
		this.cnf = cnf;
		this.cnt = new Thread(new Runnable() {
			public void run() {
				try {
					cns();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		});
		this.cnt.setDaemon(true);
		this.cnt.start();
	}

	public void close() {
		ch(hdir);
		cnt.interrupt();
	}

	public void chkWE(int rv, String name) {
		if(rv==0) {
			int gle = Kernel32.GetLastError();
			// System.out.println("gle: " + gle);
			if (gle != 0) {
				IOException e = new IOException(name + " error: " + gle + " " + Kernel32.format_message(gle));
				e.printStackTrace();
			}
		}
	}

	public void ch(long hdir) {
		if (hdir != WC.INVALID_HANDLE_VALUE) {
			int rv = Kernel32.CancelIo(hdir);
			chkWE(rv, "CancelIO");
			rv = Kernel32.CancelIoEx(hdir, Pointer.getPeer(Pointer.NULL));
			chkWE(rv, "CancelIoEx");
			rv = Kernel32.CloseHandle(hdir);
			chkWE(rv, "CloseHandle");
			hdir = WC.INVALID_HANDLE_VALUE;
		}
	}

	@SuppressWarnings({ "deprecation", "unchecked" })
	public void cns() throws IOException {
		Pointer<Integer> bret = Pointer.allocateInt();
		bret.setInt(0);
		Pointer<Short> buffer = Pointer.allocateShorts(FILE_NOTIFY_INFORMATION.LENGTH >> 1);
		// System.out.println("buffer: " + buffer + " " + buffer.getValidBytes()
		// + " bytes remaining");

		Pointer<Short> rt_native = (Pointer<Short>) Pointer.pointerToString(rt, StringType.WideC,
				StandardCharsets.US_ASCII);
		hdir = Kernel32.CreateFileW(Pointer.getPeer(rt_native), // file name
				WC.FILE_LIST_DIRECTORY, // desired access
				WC.FILE_SHARE_READ | WC.FILE_SHARE_WRITE | WC.FILE_SHARE_DELETE, // share mode
				Pointer.getPeer(Pointer.NULL), // security attributes
				WC.OPEN_EXISTING, // creation disposition
				WC.FILE_FLAG_BACKUP_SEMANTICS, // flags and attributes
				0L); // hTemplateFile
		if(hdir == WC.INVALID_HANDLE_VALUE) {
			chkWE(0, "CreateFileW");
		}
		else {
			Runtime.getRuntime().addShutdownHook(new Thread(new Runnable() {
				public void run() {
					close();
				}
			}));
			boolean aborted = false;
			while (!aborted) { // RDC loop
				// System.out.println("RDC loop");
				bret.setInt(0);
				// buffer.clearValidBytes();
				int rv = Kernel32.ReadDirectoryChangesW(hdir, Pointer.getPeer(buffer),
						(int) (buffer.getValidBytes() - 2), true, nflags, Pointer.getPeer(bret),
						Pointer.getPeer(Pointer.NULL), Pointer.getPeer(Pointer.NULL));
				// System.out.println("rv: " + rv);
 				if(rv == 0) {
 					chkWE(0, "ReadDirectoryChangesW");
					hdir = WC.INVALID_HANDLE_VALUE;
					aborted = true;
				}
				else {
					if (bret.getInt() > 0) {
						long coff = 0;
						boolean done = false;
						while (!done) { // Read file changes loop
							try {
								FILE_NOTIFY_INFORMATION fni = buffer.getNativeObjectAtOffset(coff, FILE_NOTIFY_INFORMATION.class);
								int action = fni.action();
								String path = fni.path();
								// System.out.println("action: " + action + " path: " + path + " off: " + off);
								cni = new CNI(action, path);
								String sfp = resolve(rt, path);
								if (Kernel32.dir_exists(sfp)) {
									cni.isdir = true;
								} else if (Kernel32.file_exists(sfp)) {
									cni.isfile = true;
								}
								cnf.accept(cni);
								int off = fni.size();
								if (off > 0) {
									coff += off;
								} else {
									done = true;
								}
							}
							catch(Exception e) {
								e.printStackTrace();
								done = true;
							}
						}
					}
				}
			}
			close();
		}
	}

	public String resolve(String cd2, String f1) {
		String fp2 = cd2;
		if (f1.length() > 0) {
			if (!fp2.endsWith("\\") && !fp2.endsWith("/")) {
				fp2 += "\\";
			}
			fp2 += f1;
		}
		return fp2;
	}

	public static class CNI {
		public int action;
		public String path;
		public boolean isdir;
		public boolean isfile;

		public CNI(int action, String path) {
			this.action = action;
			this.path = path;
		}
	}
}