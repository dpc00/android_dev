package org.ds.l3;

import org.ds.l2.DosCmd;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.channels.FileChannel;
import java.nio.file.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.concurrent.Callable;
import java.util.concurrent.CancellationException;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Future;
import java.util.function.BiFunction;
import java.util.stream.Collectors;

//import org.ds.l1.KSubs;

// import javafx.util.Duration

public class DSubs {

	static class CFF {
		String name;
		BiFunction<String, String, Try<Void, Exception>> cff;

		CFF(String name, BiFunction<String, String, Try<Void, Exception>> cff) {
			this.name = name;
			this.cff = cff;
		}

		Try<Void, Exception> apply(String fp1, String fp2) {
			return this.cff.apply(fp1, fp2);
		}
	}

	public static FileSystem fs = FileSystems.getDefault();
	private static ArrayList<CFF> cfl = new ArrayList<>();

	static {
		cfl.add(new CFF("copy_file1", DSubs::copy_file1));
	}

	public static Try<Void, Exception> copy_file(String fp1, String fp2) {
		Try<Void, Exception> rv1 = null;
		for (CFF cffle : cfl) {
			Exception e2 = DSRT.isCancelled();
			if (e2 != null) {
				return new Failure<>(e2);
			}
			if (fp1.compareToIgnoreCase(fp2) == 0) {
				throw new IllegalArgumentException("files names are the same");
			}
			while (true) {
				Callable<Try<Void, Exception>> c = () -> {
					DSRT th = (DSRT) Thread.currentThread();
					th.clear();
					th.state = DSRT.State.Running;
					Try<Void, Exception> rv = cffle.apply(fp1, fp2);
					if (rv instanceof Success) {
						th.state = DSRT.State.Succeeded;
					} else {
						if (rv instanceof Failure) {
							Exception e21 = DSRT.isCancelled();
							if (rv.getE() instanceof InterruptedException
									|| (e21 != null && e21 instanceof InterruptedException)) {
								th.state = DSRT.State.Interrupted;
							} else {
								if (rv.getE() instanceof CancellationException
										|| (e21 != null && e21 instanceof CancellationException)) {
									th.state = DSRT.State.Cancelled;
								} else {
									th.state = DSRT.State.Failed;
								}
							}
						}
					}
					return rv;
				};
				Future<Try<Void, Exception>> f = DSRT.execService.submit(c);
				try {
					rv1 = f.get();
					if (rv1 instanceof Success) {
						return rv1;
					}
					DSRT th = (DSRT) Thread.currentThread();
					if (rv1.getE() instanceof InterruptedException) {
						th.state = DSRT.State.Interrupted;
						return rv1;
					}
					if (rv1.getE() instanceof CancellationException) {
						th.state = DSRT.State.Cancelled;
						return rv1;
					}
					break;
				} catch (InterruptedException | ExecutionException e3) {
					e3.getCause().printStackTrace();
				}
			}
		}
		return rv1;
	}

	public static boolean dir_exists(String fspec) {
		Path v1 = Paths.get(fspec);
		if (Files.exists(v1)) {
			return Files.isDirectory(v1);
		}
		return false;
	}

	public static boolean file_exists(String fspec) {
		Path v1 = Paths.get(fspec);
		if (Files.exists(v1)) {
			return Files.isRegularFile(v1);
		}
		return false;
	}

	public static String getFileName(String cd1) {
		Path v1 = Paths.get(cd1);
		return v1.getFileName().toString();
	}

	public static String getParent(String cd1) {
		Path p = Paths.get(cd1);
		Path parent = p.getParent();
		return parent == null ? "" : parent.toString();

	}

	public static boolean hasParent(String cd1) {
		Path p = Paths.get(cd1);
		if (p == null)
			return false;
		return !(p.getRoot().toString().length() == p.toString().length());
	}

	public static String relativize(String cd1, String cd2) {
		Path v1 = Paths.get(cd1);
		Path v2 = Paths.get(cd2);
		return v1.relativize(v2).toString();
	}

	public static String resolve(String cd2, String f1) {
		String v1 = "";
		if (cd2.length() > 0 && f1.length() > 0) {
			v1 = cd2 + File.separatorChar + f1;
		} else if (cd2.length() > 0) {
			v1 = cd2;
		} else if (f1.length() > 0) {
			v1 = f1;
		}
		v1 = v1.replaceAll("\\\\\\\\", "\\\\");
		return v1;
	}

	private static Try<Void, Exception> copy_file2(String fp1, String fp2) {
		Try<DosCmd.RetV, DosCmd.RetV> rv = DosCmd.exec("copy " + fp1 + " " + fp2);
		if (rv.isFailure()) {
			DosCmd.RetV rv2 = rv.getE();
			return new Failure<>(new IOException(
					"dos cpy err " + rv2.ec + "\n" + rv2.stderr.stream().collect(Collectors.joining("\n")), rv2.ioe));
		}
		return new Success<>(null);
	}

	private static Try<Void, Exception> copy_file3(String fp1, String fp2) {
		try {
			Path tp = Files.copy(Paths.get(fp1), Paths.get(fp2), StandardCopyOption.REPLACE_EXISTING,
					StandardCopyOption.COPY_ATTRIBUTES);
			if (tp != null) {
				return new Success<>(null);
			}
			return new Failure<>(new IOException("copy_file3"));
		} catch (Exception e) {
			return new Failure<>(e);
		}
	}

	private static Try<Void, Exception> copy_file1(String fp1, String fp2) {
		int err = 0;
		File in;
		File out;
		FileInputStream fis = null;
		FileOutputStream fos = null;
		FileChannel inChannel = null;
		FileChannel outChannel = null;

		try {
			err = 1;
			in = new File(fp1);
			err = 2;
			out = new File(fp2);
			err = 3;
			fis = new FileInputStream(in);
			err = 4;
			fos = new FileOutputStream(out);
			err = 5;
			inChannel = fis.getChannel();
			err = 6;
			outChannel = fos.getChannel();
			err = 7;
			int maxCount = (64 * 1024 * 1024) - (32 * 1024);
			long size = inChannel.size();
			long position = 0;
			while (position < size) {
				position += inChannel.transferTo(position, maxCount, outChannel);
			}
			err = 8;
			fis.close();
			fis = null;
			err = 9;
			fos.close();
			fos = null;
			err = 10;
			inChannel.close();
			inChannel = null;
			err = 11;
			outChannel.close();
			outChannel = null;
			err = 12;
			Files.setLastModifiedTime(out.toPath(), Files.getLastModifiedTime(in.toPath()));
			return new Success<>(null);
		} catch (Exception e) {
			String[] emsg = new String[] { "", "new src file", "new dst file", "new src file input stream",
					"new dst file output stream", "fis getchannel", "fos getchannel", "copy", "fis close", "fos close",
					"inchannel close", "outchannel close", "set dst file time" };
			return new Failure<>(new IOException("copy_file4 error: " + emsg[err], e));
		} finally {
			if (fis != null)
				try {
					fis.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			if (fos != null)
				try {
					fos.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			if (inChannel != null)
				try {
					inChannel.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			if (outChannel != null)
				try {
					outChannel.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
		}
	}

	public static void delete_file(String fp2) throws IOException {
		Files.delete(Paths.get(fp2));
	}

	public static void remove_directory(String fp2) throws IOException {
		Files.delete(Paths.get(fp2));
	}

	private static Try<Void, Exception> copy_file5(String fp1, String fp2) {
		String fn1 = DSubs.getFileName(fp1);
		String fn2 = DSubs.getFileName(fp2);
		if (fn1.equals(fn2)) {
			String p1 = DSubs.getParent(fp1);
			String p2 = DSubs.getParent(fp2);
			String cs = "robocopy" + " " + p1 + " " + p2 + " " + fn1 + " " + "/W:3 /R:3 /MT /Z";
			Try<DosCmd.RetV, DosCmd.RetV> rv = DosCmd.exec(cs);
			if (rv.isFailure()) {
				DosCmd.RetV rv2 = rv.getE();
				return new Failure<>(new IOException(
						"robocopy err " + rv2.ec + "\n" + rv2.stdout.stream().collect(Collectors.joining("\n")) + "\n"
								+ rv2.stderr.stream().collect(Collectors.joining("\n")),
						rv2.ioe));
			}
			return new Success<>(null);
		}
		return new Failure<>(new IOException("file names don't match in copy_file5"));
	}

	public static void removeTree(String fp2) {
		if (fp2.contains(" ")) {
			if (!fp2.startsWith("\"")) {
				fp2 = "\"" + fp2;
			}
			if (!fp2.endsWith("\"")) {
				fp2 = fp2 + "\"";
			}
		}
		String cmd = "cmd /c rmdir /S /Q " + fp2;
		execcmd(cmd, dslog);
		// write2bat(opsbat, cmd);
	}

	public static final String dslog = "dirsync.log";
	public static final String opsbat = "dirsync_ops.bat";
	public static final String rcopts = "/MIR /MT /NFL /NDL /NJH /NP /R:0";

	public static void mirrorDir(String fp1, String fp2) {
		if (fp1.contains(" ")) {
			if (!fp1.startsWith("\"")) {
				fp1 = "\"" + fp1;
			}
			if (!fp1.endsWith("\"")) {
				fp1 = fp1 + "\"";
			}
		}
		if (fp2.contains(" ")) {
			if (!fp2.startsWith("\"")) {
				fp2 = "\"" + fp2;
			}
			if (!fp2.endsWith("\"")) {
				fp2 = fp2 + "\"";
			}
		}
		String cmd = "robocopy " + fp1 + " " + fp2 + " " + rcopts;
		execcmd(cmd, dslog);
		// write2bat(opsbat, cmd);
	}

	public static void mirrorTree(String fp1, String fp2) {
		if (fp1.contains(" ")) {
			if (!fp1.startsWith("\"")) {
				fp1 = "\"" + fp1;
			}
			if (!fp1.endsWith("\"")) {
				fp1 = fp1 + "\"";
			}
		}
		if (fp2.contains(" ")) {
			if (!fp2.startsWith("\"")) {
				fp2 = "\"" + fp2;
			}
			if (!fp2.endsWith("\"")) {
				fp2 = fp2 + "\"";
			}
		}
		String cmd = "robocopy " + fp1 + " " + fp2 + " /S " + rcopts;
		execcmd(cmd, dslog);
		// write2bat(opsbat, cmd);
	}

	public static void write2bat(String bat, String cmd) {
		try {
			Files.write(Paths.get(bat), Arrays.asList(cmd), StandardOpenOption.CREATE, StandardOpenOption.APPEND,
					StandardOpenOption.SYNC, StandardOpenOption.WRITE);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public static void execcmd(String cmd, String logfn) {
		ProcessBuilder builder = new ProcessBuilder();
		builder.command(cmd.split(" "));
		builder.inheritIO().redirectOutput(ProcessBuilder.Redirect.PIPE);
		Process process;
		try {
			process = builder.start();
			System.out.println(cmd);
			try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
				reader.lines().forEach(line -> {
					try {
						System.out.println(line);
						Files.write(Paths.get(logfn), Arrays.asList(line), StandardOpenOption.CREATE, StandardOpenOption.APPEND,
								StandardOpenOption.SYNC, StandardOpenOption.WRITE);
					} catch (IOException e) {
						e.printStackTrace();
					}
				});
			}
			process.waitFor();
		} catch (IOException | InterruptedException e) {
			e.printStackTrace();
		}

	}
}
