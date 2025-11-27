package org.ds.app;

import java.io.IOException;
import java.nio.file.FileStore;
import java.nio.file.FileSystem;
import java.nio.file.FileSystems;
import java.util.ArrayList;
import java.util.function.Consumer;
import java.util.function.Predicate;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.ds.types.DL;
import org.ds.types.VL;

public class ParamReader {
	public static FileSystem fsm = FileSystems.getDefault();

	public static class FSData {
		VL lbl;
		DL drv;
		int vsn;
		long tot;
		long free;
	}

	public void iterFS(Consumer<FSData> bcf) {
		for (FileStore fs : fsm.getFileStores()) {
			FSData fsd = new FSData();
			String s2 = fs.toString();
			Pattern p1 = Pattern.compile(".* \\(");
			Matcher m1 = p1.matcher(s2);
			if (m1.find()) {
				fsd.lbl = new VL(s2.substring(m1.start(), m1.end() - 2));
			}
			else fsd.lbl = new VL("");
			Pattern  p2 = Pattern.compile("\\([A-Za-z]:\\)");
			Matcher m2 = p2.matcher(s2);
			if (m2.find()) {
				fsd.drv = new DL(s2.substring(m2.start() + 1, m2.end() - 1));
			}
			else fsd.drv = new DL("");
			try {
				fsd.vsn = (int) fs.getAttribute("volume:vsn");
				fsd.tot = (long) fs.getAttribute("totalSpace");
				fsd.free = (long) fs.getAttribute("unallocatedSpace");

			} catch (IOException e) {
				e.printStackTrace();
			}
			bcf.accept(fsd);
		}
	}

	public ArrayList<RtData> rts = new ArrayList<>();

	public ParamReader() {

	}

	public static ArrayList<RtData> build(ArrayList<String> args) {
		ParamReader pr = new ArgsEnvReader(args);
		return pr.rts;
	}

	public ParamReader(ArrayList<String> args) {
	}

	@SafeVarargs
	public static ArrayList<RtData> build(Predicate<VL> ...vls) {
		ParamReader pr = new VLMatchReader(vls);
		return pr.rts;
	}
}
